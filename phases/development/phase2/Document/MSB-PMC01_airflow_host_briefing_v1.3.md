# MSB-PMC01 Cluster & Airflow Target Node Briefing

_For: Ksolves implementation team_
_Prepared by: fqdn infrastructure (cluster owner)_
_Version 1.3 · 2026-05-11_
_Subject: Hardware and infrastructure context for P1.0 (Remote Airflow Server provisioning), plus DAG behavior expectations carried over from the Ksolves Spark/YARN Config v1.0 baseline · v1.3 captures the 2026-05-11 msb-pmc01 retirement decision and the msb-pmc04 commitment as Airflow's successor host_

> **SUPERSESSION NOTICE (v1.3, 2026-05-11):** This briefing is being phased out. Per the Vendor Access Isolation Framework v0.2 (`security/Document/Vendor_Access_Isolation_Framework_v0.2.md`, circulated 2026-05-11), **msb-pmc01 is being retired from the Spark fabric, and msb-pmc04 is committed as the successor host** for Airflow + ancillary services (Grafana / Prometheus / Loki, Bastion, Ansible source) + additive Ceph + CephFS / RGW frontend gateways. Until migration completes, the hardware / network / storage context below remains operationally accurate for the interim msb-pmc01-04 deployment. Once msb-pmc04 specs and inventory land, a **successor briefing** (new basename, e.g. `MSB-PMC04_airflow_host_briefing_v1.0.md`) will replace this document. Treat new provisioning decisions as targeting msb-pmc04, not msb-pmc01-04.
>
> See:
> - `security/Document/Vendor_Access_Isolation_Framework_v0.2.md` — the formalized retirement / commitment decision
> - `Phases_Critical_Path_Development_v1.5.md` § BLOCKER.4 § msb-pmc04 third-cluster — committed 2026-05-11
> - `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Status (2026-05-11 — framework v0.2 circulated)

---

## 1. Purpose

This briefing provides Ksolves with the hardware, storage, and network context required to provision the remote Airflow server VM (P1.0) on the MSB-PMC01 Proxmox cluster. The cluster is fqdn-managed; this document is the working reference Ksolves should use for VM placement, sizing, and storage allocation decisions during P1.0.

MSB-PMC01 runs Proxmox VE (kernel `6.8.12-20-pve`) in a hyperconverged Ceph configuration. Ksolves' provisioning activities will land VMs into this cluster but will not modify cluster, Ceph, or networking infrastructure — those remain fqdn-managed.

**v1.1 update (2026-05-05):** Section 6 finalized in light of decisions captured in `Phases_Critical_Path_Development_v1.5.md` (3-node cluster posture, 1 concurrent Spark job, Azure Blob staging confirmed). Added § 5.1 — Airflow DAG behavior expectations carried over from `Ksolves_Spark_YARN_Config_v1.0.pdf` (table ordering, runtime repartition parameter injection, retry handling, placeholder-table size-check gate).

**v1.2 update (2026-05-07):** Restores **Nginx as an in-scope install task** on the Airflow VM. Earlier "no HA → no Nginx" reasoning (used during the v1.3/v1.4 main-CP cycle) was incorrect — the single YARN ResourceManager confirms there is no HA stable-endpoint requirement, but stable-endpoint-for-HA is only one of several potential Nginx roles. Nginx **install** is in scope; **server activation / functional configuration is TBD by Ksolves** post-install. Candidate roles (any subset, Ksolves' decision):
- Reverse proxy for the YARN ResourceManager UI and other Spark/Airflow web UIs (consistent UI surface)
- TLS termination
- SSO front-door (Okta) routing
- URL rewriting
- IP allowlisting (defense-in-depth ingress filter)
- Access logging (audit + ePHI logging surface for the HIPAA audit-logging gate, P2.9 in main CP)

This briefing pairs with `Phases_Critical_Path_Development_v1.5.md` § P1.0 — see that section's Nginx scope note for the equivalent text in the main CP.

**Update 2026-05-08 (non-blocking) — msb-pmc04 third-cluster under consideration:** A third Proxmox cluster (msb-pmc04) is under consideration to add to the Spark cluster infrastructure, with the explicit goal of **removing msb-pmc01 from the security equation** (per the Isolation sub-project / BLOCKER.4 design work). If pursued, this would shift orchestration / Airflow / monitoring services from msb-pmc01-04 onto msb-pmc04, leaving msb-pmc01 entirely outside the vendor-allowed surface. The contents of this briefing would migrate to a successor briefing for the new host. **Status: non-blocking — captured for reference; track decision as it crystallizes.** Cross-references: CP v1.5 § BLOCKER.4 (msb-pmc04 third-cluster note) + `security/Notes/vendor-access-isolation-plan_2026-05-06.md`.

---

## 2. Cluster Overview — MSB-PMC01

The cluster comprises **four physical nodes**, all running Proxmox VE with hyperconverged Ceph. Hardware is heterogeneous, with two distinct CPU tiers.

### 2.1 Node Specifications

| Node | CPU model | Sockets × Cores × Threads | Logical CPUs | RAM | NUMA nodes | Role |
|---|---|---|---|---|---|---|
| msb-pmc01-01 | Intel Xeon Gold 6136 @ 3.00 GHz | 1 × 12 × 2 | 24 | 130 GB | 1 | Unassigned |
| msb-pmc01-02 | Intel Xeon Silver 4210R @ 2.40 GHz | 2 × 10 × 2 | 40 | 162 GB | 2 | Monitoring |
| msb-pmc01-03 | Intel Xeon Silver 4210R @ 2.40 GHz | 2 × 10 × 2 | 40 | 162 GB | 2 | Monitoring |
| **msb-pmc01-04** | **Intel Xeon Gold 6136 @ 3.00 GHz** | **1 × 12 × 2** | **24** | **130 GB** | **1** | **Airflow target (P1.0)** |

**Hardware tiers:**

- **Tier A (Gold 6136) — msb-pmc01-01, msb-pmc01-04:** single-socket, single-NUMA, higher clock (3.0 GHz base / 3.7 GHz boost). Lower core count, less RAM.
- **Tier B (Silver 4210R) — msb-pmc01-02, msb-pmc01-03:** dual-socket, dual-NUMA, lower clock (2.4 GHz base / 3.2 GHz boost). Higher core count and RAM. Currently dedicated to monitoring services.

The Airflow VM has been deliberately placed on Tier A (msb-pmc01-04) to benefit from higher single-thread clock speed, which favors Airflow's scheduler and Postgres metadata DB.

### 2.2 Ceph Storage Topology

The cluster runs hyperconverged Ceph with **two OSD device classes**:

| Device class | Purpose | Per-node OSDs | Approximate raw capacity |
|---|---|---|---|
| `hdd` | Bulk Ceph storage (default pool) | 3× 838 GiB + 1× 1.1 TiB | ~ 3.6 TiB / node |
| `rbd_ssd` | Dedicated SSD pool for VM block storage (RBD volumes) | 2× 894 GiB | ~ 1.8 TiB / node |

**Total cluster capacity:** 21 TiB raw, currently 11.43% used (~ 2.5 TiB consumed cluster-wide).

Boot drives on each node — 2× 447 GiB SSDs in a Proxmox ZFS mirror — are separate from Ceph and not part of any pool.

**Implication for P1.0:** The Airflow VM's 500 GB volume will be carved from the `rbd_ssd` pool, not from local storage.

### 2.3 Cluster Management Boundary

- The cluster is **fqdn-managed**. The user has direct on-site console access to all four nodes.
- Ksolves' scope for P1.0 is **VM-level provisioning** (creation, OS installation, application stack, configuration) inside MSB-PMC01.
- **Out of Ksolves' scope:** Ceph configuration, OSD layout, Proxmox cluster membership, hardware changes, network/firewall changes.
- Access is granted under BLOCKER.1 Phase 1A (Webex desktop sharing, active as of 2026-04-29). VDI (Phase 1B) remains in approval; non-blocking.

---

## 3. Airflow Target Node — msb-pmc01-04

### 3.1 Hardware Fingerprint

| Attribute | Value |
|---|---|
| Hostname | `msb-pmc01-04` |
| Kernel | Linux `6.8.12-20-pve` (Proxmox VE) |
| CPU model | Intel Xeon Gold 6136 @ 3.00 GHz (Skylake-SP) |
| Sockets | 1 |
| Cores per socket | 12 |
| Threads per core | 2 |
| Logical CPUs | 24 |
| Max boost clock | 3.7 GHz |
| NUMA nodes | 1 (CPUs 0–23, single domain) |
| L3 cache | 24.8 MiB (1 instance) |
| Total RAM | 130 GB |
| Memory block size | 2 GB |
| Virtualization | VT-x supported |

### 3.2 Storage Layout (lsblk)

| Device | Size | Role |
|---|---|---|
| sda | 447 GiB | Proxmox ZFS boot mirror (member 1) |
| sdb | 447 GiB | Proxmox ZFS boot mirror (member 2) |
| sdc | 894 GiB | Ceph OSD (`rbd_ssd` class) — osd.18 |
| sdd | 894 GiB | Ceph OSD (`rbd_ssd` class) — osd.19 |
| sde | 838 GiB | Ceph OSD (`hdd` class) — osd.22 |
| sdf | 838 GiB | Ceph OSD (`hdd` class) — osd.21 |
| sdg | 838 GiB | Ceph OSD (`hdd` class) — osd.20 |
| sdh | 1.1 TiB | Ceph OSD (`hdd` class) — osd.23 |
| sdi | (empty) | Reserved drive bay (no disk present) |
| sdj | 512 MiB read-only | Virtual media (likely BMC / iLO mount) |
| zd0 | 64 GiB | Proxmox-internal ZFS volume |

**OSD count on this node: 6**, consistent with the rest of the cluster.

### 3.3 Current Workload

No production VMs currently run on msb-pmc01-04. The host runs only Proxmox VE and Ceph daemons (MON, MGR, OSDs) at this time. The 64 GiB `zd0` ZFS volume is Proxmox-internal infrastructure, not a user VM.

This means msb-pmc01-04 has full host capacity available for the Airflow VM and any future co-tenants the user assigns.

### 3.4 Recommended Airflow VM Configuration

Per the P1.0 specification (6 vCPU / 24 GB RAM / 500 GB SSD, RHEL 9.4):

| Proxmox parameter | Value | Rationale |
|---|---|---|
| Sockets | **1** | Host is single-socket; no NUMA boundary to consider |
| Cores | **6** | Fits inside the 12-core socket without contention |
| RAM | 24 GB | ~ 18% of host's 130 GB |
| Disk | 500 GB | Allocated from Ceph `rbd_ssd` pool |
| OS | RHEL 9.4 | Per Phase 1 standardization |
| Network | Bridge to LAN routable to MSB-PMC03 | See § 4 |
| Hostname | `airflow-prod-01` (suggested) | Confirmed during provisioning by fqdn |

**NUMA pinning** is not required. The host is single-NUMA, so the Proxmox `numa: 0` default is appropriate.

---

## 4. Network Prerequisites (P0.7 Gate)

Before the Airflow VM can be provisioned and tested, the fqdn network team must verify connectivity between MSB-PMC01 (Airflow host cluster) and MSB-PMC03 (Spark cluster):

| Direction | Required ports |
|---|---|
| MSB-PMC01 → MSB-PMC03 nodes | TCP 8032 (YARN RM submission), 8088 (YARN UI), 22 (SSH), 9095 (JMX, if monitoring is enabled) |
| MSB-PMC03 nodes → MSB-PMC01 | Return traffic on the same ports |

**Latency target:** < 10 ms ping between MSB-PMC01 and any MSB-PMC03 worker node (same-datacenter assumption).

**Verification artifacts:** `nc -zv <node> 8032` and `nc -zv <node> 8088` succeed against all three MSB-PMC03 worker nodes. Network team confirms in change ticket.

This gate must close before Ksolves begins VM provisioning. Status tracking is in `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.5.md` § P0.7.

---

## 5. Provisioning Inputs Ksolves Will Need from fqdn

| Input | Owner | Purpose |
|---|---|---|
| Proxmox access (Webex desktop session, then VDI when available) | fqdn (user) | VM creation, configuration |
| IP allocation for the Airflow VM | fqdn Network Team | VM network configuration |
| Final hostname assignment | fqdn | DNS / systemd hostname |
| RHEL 9.4 ISO and subscription credentials | fqdn (provided per BLOCKER.2) | OS installation, package access |
| Okta tenant OIDC client ID and secret | fqdn (Okta admin) | Airflow SSO integration |
| SSH access patterns to all three MSB-PMC03 worker nodes | fqdn | Ansible control + Spark submission |
| Ceph RGW S3 endpoint URL and access keys | fqdn (provisioned in P0.0) | `s3a://` connector for Spark/Airflow operations |

### 5.1 Airflow DAG Behavior Expectations (added v1.1, 2026-05-05)

The vendor's authoritative configuration document (`Ksolves_Spark_YARN_Config_v1.0.pdf`) was delivered 2026-05-04 and is built around an actual measurement of the DEV environment (`csv_file_sizes.xlsx`: 800 tables, 359 with data, 12,214 files, ~1.52 TB total compressed). It implies several DAG-level expectations that affect how Ksolves should structure Airflow's orchestration of Spark submissions.

| Expectation | Source | Detail |
|---|---|---|
| **Table ordering — large-first** | Vendor § 1.3 SLA Risk Summary | At 3 nodes with 1 concurrent Spark job, the SLA is feasible-but-zero-buffer. The mitigation is to order the daily DAG to schedule the **12 largest tables first** (top-12 = 79.29 % of total daily volume). Long-tail small tables run after the SLA-critical bulk volume is already complete. |
| **Placeholder-table size-check gate** | Vendor § 1.1 (table inventory) + 3-node decision (2026-05-05) | 184 of the 800 tables are placeholders / empty. Airflow should pre-flight each table with a size check (RGW HEAD or list-objects) and **skip empty/placeholder tables** rather than dispatch a no-op Spark job. Saves cluster time materially over a 800-table sweep. |
| **Per-table repartition parameter injection** | Vendor § 7.2 (repartition formula) | For every compressed CSV table the DAG should compute and pass `--conf spark.sql.shuffle.partitions=<N>` (or pass `target_partitions` to the job) using the formula `target_partitions = max(24, ceil(compressed_csv_mb / 50))`. The DAG looks up `compressed_csv_mb` per table at runtime (RGW object size) and injects it into the Spark submission. |
| **Static reference for shuffle partitions** | Vendor § 4 / § 7.2 | If a per-table override is not supplied, the cluster default is `spark.sql.shuffle.partitions = 4096`. This is a useful fallback but not a substitute for the per-table formula above on small tables, where it would create thousands of tiny shuffle files. |
| **Retry handling lives in Airflow, not Spark** | Conventional Airflow + decision 2026-05-05 | Spark job retries are owned by the **Airflow task** (`retries`, `retry_delay`, `retry_exponential_backoff`), not by Spark's internal stage retries. This keeps every retry visible in the Airflow UI / metadata DB and prevents Spark from silently re-running on the cluster while Airflow believes the job has finished. Configure Spark itself for fast-fail. |
| **Single concurrent Spark job** | 3-node cluster decision, 2026-05-05 | The cluster is sized to run **one Spark job at a time**. The Airflow DAG must serialize Spark submissions with a `max_active_runs=1` (DAG-level) or a pool-of-1 covering the Spark-submission task; otherwise Spark jobs will queue inside YARN and lose the timing guarantee that the large-first ordering above is meant to provide. |

These expectations are not P1.0 sizing inputs — they are DAG-design inputs for P2.2 (Airflow installation + DAG bring-up). Captured here in the host-briefing so the team that provisions the host has the full operational context, not just the vCPU/RAM numbers.

---

## 6. Open Items Affecting Final Sizing

The following items, previously open in v1.0, were resolved on 2026-05-05 alongside the vendor configuration baseline rollover. They are kept here for traceability:

| Item | State | Effect on Airflow VM |
|---|---|---|
| Max concurrent Spark jobs | **Closed 2026-05-05 — 1** (3-node cluster decision) | Airflow DAG serializes Spark submissions (`max_active_runs=1` or pool-of-1). Celery worker count and broker (Redis/RabbitMQ) sizing scoped to a single concurrent submission flow; current 6c/24GB has comfortable headroom. |
| Cloud staging target | **Closed 2026-05-05 — Azure Blob** (vendor § 1.1 Pipeline) | `s3a://` connector points to the on-cluster Ceph RGW endpoint; outbound batch-transfer to Azure Blob via SAS token / managed identity is a separate operator stage downstream of the Spark job. |
| Cluster outbound network path (MPLS vs DIA-direct vs DIA+VPN) | Still open with fqdn networking | Determines WAN egress profile for the Azure Blob batch transfer; does not block Airflow VM provisioning. |

The remaining open item (outbound network path) does not block the start of provisioning but should be resolved before production cutover.

---

## 7. Source Data and References

This briefing draws from the following authoritative artifacts in the fqdn project repository:

- **Host inventory (lscpu, lsblk, lsmem) for all four MSB-PMC01 nodes:**
  `phases/development/phase2/Document/MSB-PMC01_cluster_host_inventory.md`
- **Ceph OSD tree (`ceph osd df tree` output):**
  `phases/development/phase2/Incoming/PMC01_OSD_Tree/PMC01_OSD_Tree.md`
- **Phase 2 critical path with P1.0 specification:**
  `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.5.md` § P1.0, P0.7
- **Vendor Spark/YARN configuration baseline (delivered 2026-05-04):**
  `phases/development/phase2/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1 (table inventory), § 1.3 (SLA risk summary), § 4 (Spark defaults), § 7.2 (repartition formula)
- **HIPAA compliance sub-project critical path:**
  `phases/development/phase2/Document/CP_HIPAA_Compliance_v1.1.md`
- **Phase 1 report (delivered 2026-04-24):**
  `phases/development/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf`

---

_End of briefing._
