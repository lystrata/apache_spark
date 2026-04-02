# Architecture Decisions

## Resource Manager: YARN (not Spark Standalone, not Kubernetes)

YARN provides resource isolation, dynamic allocation, external shuffle service, and queue scheduling. YARN does not require HDFS — it runs with Ceph S3 (s3a://) as the storage layer. The Hadoop distribution is installed for YARN binaries only; no HDFS daemons run.

Spark Standalone was rejected: no resource isolation, no dynamic allocation, no preemption.
Kubernetes was rejected: adds container orchestration complexity unnecessary for this workload.

## Storage Model (v2)

- **SSDs (3× 480 GB)**: Proxmox OS only. 2 SSDs form a ZFS mirror; 1 is a hot spare. SSDs do not contribute to VM scratch or Ceph.
- **NVMe (8× 3.2 TB)**: Split between Ceph OSDs and local scratch.
  - Default 4 OSDs → Ceph (S3 + RBD). Provides 12.8 TB usable at rep=3, sufficient for 6+ days ingest at 2 TB/day. Only 1–2 days retention is required (daily from-scratch runs flushed to Snowflake).
  - Remaining 4 NVMe → local scratch passed through to worker VMs (6.4 TB per VM with 2 VMs/node).
- **VM images on Ceph RBD**: Enables Proxmox HA and live migration. If a node fails, VMs restart on surviving nodes automatically.

Previous v1 model used SSDs for VM scratch; this was changed to improve resilience and simplify the storage hierarchy.

## Replication: rep=3 (not Erasure Coding)

Erasure Coding was evaluated and rejected for 3-node cluster:
- Only safe EC profile is EC 2+1 (67% efficiency) — marginal improvement over rep=2 (50%).
- EC 4+2 needs 6 failure domains; unsafe with 3 nodes unless relaxed to per-OSD domains.
- Read penalty from EC chunk reassembly hurts Spark's parallel S3 read pattern.
- Data is transient (flushed to Snowflake daily), so capacity pressure is low.

Recommendation: rep=3 for RBD (VM images). rep=2 acceptable for S3 ingest pool if capacity needed.

## YARN Services VM

Single VM hosting: YARN ResourceManager, Spark History Server, Hive Metastore, PostgreSQL.
- 6 vCPUs, 16 GB RAM (configurable via calculator sliders).
- Runs on Node 1 by default; protected by Proxmox HA.
- Cost amortized ÷3 in the calculator's per-node budget model.

Full YARN RM HA (active/standby with ZooKeeper) was evaluated and deferred:
- Proxmox HA provides ~30–60 second failover (sufficient for daily batch ETL).
- YARN RM HA would consume ~7 vCPUs + 11 GB for ZooKeeper + standby RM.
- Can be revisited if workload moves to streaming or multi-tenant concurrent jobs.

## NodeManager Overhead

Each worker VM reserves 2 cores + 2 GB RAM for:
- 1 core: Guest OS + YARN ApplicationMaster
- 1 core: YARN NodeManager daemon
- 2 GB: NodeManager JVM heap

This is subtracted before executor sizing: executors_per_vm = floor((vCPUs − 2) / exec_cores).

## NUMA Pinning

Each worker VM pinned to one NUMA domain (32 cores, ~364 GB). 2 VMs per node = both NUMA domains utilized. Disabling NUMA pinning causes ~2× memory latency on ~50% of accesses.

## ExaBGP (not Keepalived)

ExaBGP announces RGW VIP via BGP to upstream routers. Each node runs ExaBGP with a health check against local RGW. Healthy nodes announce the VIP; failures withdraw. Upstream router does ECMP load balancing.

Advantages over Keepalived: no L2 adjacency requirement, works across subnets, faster convergence.

## Data Flow

```
Ingest:  User/ETL → S3 API (ExaBGP VIP :7480) → Ceph RGW → Ceph OSDs
Spark:   spark-submit → YARN RM (services VM) → NM allocates containers → executors read s3a://
Output:  Spark writes Parquet → S3 → Snowflake COPY INTO
```

## Ancillary Services Required

- YARN ResourceManager (services VM)
- YARN NodeManager (per worker VM, daemon inside VM)
- Spark History Server (services VM, port 18080)
- Hive Metastore (services VM, port 9083)
- PostgreSQL (services VM, metastore backend)
- ExaBGP (per Proxmox host, for RGW VIP)
- Ceph RGW (per Proxmox host, S3 gateway)
- Ceph MON (per Proxmox host, Paxos quorum)
