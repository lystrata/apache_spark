## Proxmox / Spark Production Cluster Calculator — User Guide

### Hardware Constants (top bar)

These are fixed values describing your physical hardware. They are not adjustable — the calculator is built around this specific 3-node production configuration.

- **Physical nodes**: 3 Proxmox hosts
- **Cores / node**: 64 (2× 32-core CPUs)
- **NUMA domains / node**: 2 (each CPU is its own memory domain, ~364 GB each)
- **RAM / node**: 728 GB
- **SSDs / node**: 3× 480 GB (Proxmox OS as ZFS mirror + 1 hot spare)
- **NVMe / node**: 8× 3.2 TB (split between Ceph OSDs/RBD and local scratch)

SSDs are dedicated to the Proxmox host OS and are not used for VM scratch or Ceph storage. Two SSDs form a ZFS mirror for OS resilience; the third serves as a hot spare. All VM images are stored on Ceph RBD (backed by NVMe OSDs) to enable Proxmox HA and live migration. Scratch storage for Spark shuffle spill comes exclusively from NVMe drives not assigned to Ceph.

---

### Infrastructure Parameters (left card)

These control how each physical node's resources are carved up into VMs.

**VMs per node** (1–2, default: 2)
How many Spark worker VMs run on each physical node. With NUMA pinning enabled, 2 VMs is ideal — one pinned to each NUMA domain for optimal memory locality. Setting this to 1 wastes half the NUMA bandwidth.

*Impacts:* Total worker VMs (×3 nodes), executor count, free cores/RAM per node, scratch disk per VM.

**vCPUs per worker VM** (8–32, default: 24)
Virtual cores assigned to each worker VM. Capped at 32 because that's one NUMA domain. The "Effective max" row in the overhead table shows the real ceiling after infrastructure reservations — typically lower than 32. The default of 24 is chosen to avoid core overcommit with the default OSD and services VM settings.

*Impacts:* Executors per VM (more vCPUs = more executors), core budget (may overcommit if set too high), free cores.

**RAM per worker VM** (64–380 GB, default: 320)
Memory assigned to each worker VM. Inside the VM, 2 GB is reserved for the YARN NodeManager daemon, and the rest is divided among executors.

*Impacts:* Executor memory (more RAM = larger `spark.executor.memory`), OOM margin, RAM budget.

**NVMe drives → Ceph OSDs** (4–8 per node, default: 4)
How many of the 8 NVMe drives per node are used as Ceph storage (S3 object store + RBD for VM images). The remaining drives become local scratch for worker VMs (shuffle spill, temp data).

With the default of 4 OSDs and rep=3, usable Ceph capacity is 12.8 TB — sufficient for 6+ days of ingest at 2 TB/day, well above the 1–2 day retention requirement. The remaining 4 NVMe drives provide 6.4 TB of scratch per VM (with 2 VMs/node), which comfortably exceeds worst-case shuffle data.

*Impacts:* Ceph usable capacity and days-of-ingest (more OSDs = more S3 storage), scratch per VM (fewer OSDs = more scratch), Ceph core/RAM overhead (1 core + 3 GB per OSD).

This is the primary trade-off in the calculator — **S3/RBD capacity vs. shuffle scratch space**.

**Ceph replication factor** (2–3, default: 3)
Number of copies Ceph stores for each object.

- **3×**: Survives 2 simultaneous OSD failures. Uses 33% of raw capacity.
- **2×**: Survives 1 failure. Uses 50% of raw — 50% more usable space.

*Impacts:* Ceph usable capacity, days of ingest. Since ingest data is transient (flushed to Snowflake daily), rep=2 may be acceptable for the S3 data pool. However, the RBD pool backing VM images should remain at rep=3 for resilience — Ceph allows per-pool replication settings.

**NUMA pinning** (toggle, default: on)
When enabled, each VM is pinned to a single NUMA domain so all its memory accesses are local. Disabling it allows the hypervisor to schedule memory across both NUMA domains, adding ~2× latency on roughly half of memory accesses.

*Impacts:* No numeric impact on the calculator, but fires a warning when disabled. Always leave this on.

**AQE enabled** (toggle, default: on)
Assumes Spark 3.x Adaptive Query Execution is active. AQE auto-tunes shuffle partitions at runtime, coalesces small partitions after shuffles, and rewrites skew joins — all without manual tuning.

- **On**: `spark.sql.shuffle.partitions` is set to a high ceiling (`max(2000, calculated)`), trusting AQE to coalesce down. Three `spark.sql.adaptive.*` params are set to `true`.
- **Off**: Partition count is the raw calculated value, which you'd need to manually tune per job. Fires a warning.

*Impacts:* Shuffle partition count formula, three adaptive config params. Leave on unless running Spark 2.x.

**YARN services VM** (toggle, default: on)
Whether to account for a dedicated services VM hosting the YARN ResourceManager, Spark History Server, and Hive Metastore + PostgreSQL. This VM runs on one physical node and its cost is amortized (÷3) across the per-node budget model.

- **Services VM vCPUs** (4–8, default: 6)
- **Services VM RAM** (8–24 GB, default: 16)

*Impacts:* Adds amortized per-node overhead to the reservation budget. Reducing these values frees resources for worker VMs but risks under-provisioning the ResourceManager under heavy scheduling load.

**Resilience note:** Because VM images reside on Ceph RBD, the services VM is protected by Proxmox HA. If the hosting node fails, Proxmox automatically restarts the services VM on a surviving node within ~30–60 seconds. YARN's `spark.yarn.maxAppAttempts` setting handles in-flight job recovery. For daily batch ETL workloads, this provides sufficient resilience without the complexity of a full YARN ResourceManager HA (active/standby) deployment.

---

### Spark Executor Parameters (right card)

These control how each worker VM's resources are divided into Spark executor containers. Inside every worker VM, 2 cores and 2 GB RAM are first reserved for the guest OS and YARN NodeManager daemon; the remainder is divided among executors.

**spark.executor.cores** (2–10, default: 5)
Cores per executor. Each executor runs this many concurrent tasks. The canonical recommendation for S3-backed workloads is 5 — enough parallelism for concurrent S3 reads without excessive GC pressure from too many threads sharing one heap.

*Impacts:* Executors per VM = `floor((vCPUs − 2) / this)`. Lower values = more executors with less parallelism each. Higher values = fewer, wider executors.

**Overhead fraction** (8–20%, default: 10%)
JVM memory overhead as a percentage of `spark.executor.memory`. Covers thread stacks, NIO direct buffers, class metadata, JIT code cache. Maps directly to `spark.executor.memoryOverheadFactor`.

The calculator uses this to compute how much heap fits within each executor's memory slot:
`executor.memory = floor((slot − offheap) / (1 + overhead) × 0.95)`

*Impacts:* Directly reduces `executor.memory` (higher overhead = less heap). Increase to 15–20% for PySpark workloads where Python worker processes and Arrow serialization buffers consume overhead space.

**Off-heap size** (0–16 GB, default: 6)
Memory allocated outside the JVM heap for Spark's internal use — Parquet/ORC columnar decoding, Tungsten serialization buffers. Maps to `spark.memory.offHeap.size`.

*Impacts:* Subtracted from the slot before `executor.memory` is computed. Set to 0 if not using off-heap; increase if working with wide Parquet schemas or heavy serialization.

**Daily data volume** (1–8 TB, default: 2)
Expected daily ingest volume into Ceph S3.

*Impacts:* Days of ingest (Ceph capacity ÷ this), shuffle data estimate, scratch disk adequacy check, shuffle partition count.

**Shuffle amplification** (1–4×, default: 2)
How much intermediate data Spark generates relative to input during shuffles (joins, aggregations, sorts). A 2 TB input with 2× amplification produces ~4 TB of shuffle I/O that must fit on scratch disks.

*Impacts:* Scratch disk adequacy warning, shuffle partition count. Increase if your jobs have many wide joins or exploding group-bys.

**Target partition size** (64–512 MB, default: 200)
Desired size of each shuffle partition. Smaller partitions = more parallelism but more scheduling overhead. 128–256 MB is the typical sweet spot.

*Impacts:* `spark.sql.shuffle.partitions` = `ceil(daily_TB × shuffle_amp × 1048576 / this)`. With AQE on, this is a starting ceiling that gets coalesced down automatically.

---

### Output Panels

**Fixed Overhead Reservations** — Shows exactly where each core and GB of RAM goes before VMs are sized. Rows cover Proxmox hypervisor, Ceph OSDs (scales with OSD slider), Ceph RGW, Ceph MON, and the YARN services VM (amortized ÷3). The "Available for VMs" row shows what remains, and the "Effective max / VM" row is the true ceiling for the vCPU and RAM sliders.

**Resource Budget (per node)** — Stacked bar charts showing per-node core and RAM allocation across four categories: Proxmox OS, Ceph+RGW, Spark VMs, and Unallocated. Legend values update dynamically with actual counts. When VMs claim more than what's available, the free segment turns red and the legend reads "OVERCOMMIT."

**Executor Math** — Executors per VM, total executors cluster-wide, and total executor cores (the parallelism ceiling). Below is a memory breakdown bar showing how each executor slot is divided: `executor.memory` (heap), JVM overhead, and off-heap. Three metrics show the slot size, computed `executor.memory`, and OOM risk (based on how much margin remains after fitting heap + overhead + off-heap into the slot).

**Storage Layout (per node)** — Visual mapping of all SSDs and NVMe drives to their roles. SSDs are shown as a ZFS mirror pair for the Proxmox OS plus a hot spare. NVMe drives are split between Ceph OSDs (labeled "S3 + RBD" since they back both the S3 object store and VM images) and local scratch passed through to worker VMs. Three metrics show Ceph usable capacity, days of ingest at current daily volume, and scratch space per VM. A chip diagram shows the OSD/scratch split across all 3 nodes.

**Spark Configuration (spark-defaults.conf)** — Spark configuration parameters relevant to this cluster topology. The panel contains two categories of parameters:

*Derived from slider/toggle values:*
- `spark.master` → fixed to `yarn` (implied by the YARN services VM architecture)
- `spark.submit.deployMode` → fixed to `cluster` (driver runs inside a YARN container)
- `spark.executor.cores` → direct from executor cores slider
- `spark.executor.memory` → **computed** from RAM/VM, executors/VM, overhead fraction, and off-heap size
- `spark.executor.memoryOverheadFactor` → direct from overhead fraction slider
- `spark.memory.offHeap.enabled` → `true` if off-heap slider > 0, `false` otherwise
- `spark.memory.offHeap.size` → direct from off-heap slider
- `spark.executor.instances` → **computed** from VMs per node, vCPUs per VM, executor cores, and node count
- `spark.default.parallelism` → **computed** as total executor cores × 2
- `spark.sql.shuffle.partitions` → **computed** from daily volume, shuffle amplification, target partition size, and AQE toggle
- `spark.sql.adaptive.enabled` → direct from AQE toggle
- `spark.sql.adaptive.coalescePartitions.enabled` → direct from AQE toggle
- `spark.sql.adaptive.skewJoin.enabled` → direct from AQE toggle

*Static best-practice defaults (not tied to any slider):*
- `spark.sql.parquet.compression.codec` → always `snappy` (Snowflake compatibility)
- `spark.hadoop.fs.s3a.endpoint` → placeholder for your Ceph RGW address (e.g., `https://<rgw-vip>:7480`)
- `spark.hadoop.fs.s3a.path.style.access` → always `true` (required for Ceph RGW / non-AWS S3)

**Diagnostics & Warnings** — Context-aware alerts that fire based on current settings: core/RAM overcommit errors, executor OOM risk, NUMA boundary violations, low executor density, Ceph capacity alerts, scratch disk insufficiency, and a green "Configuration looks healthy" indicator when all checks pass.
