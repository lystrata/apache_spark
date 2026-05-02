# MSB-PMC01 Cluster & Airflow Target Node Briefing

_For: Ksolves implementation team_
_Prepared by: fqdn infrastructure (cluster owner)_
_Version 1.0 · 2026-04-29_
_Subject: Hardware and infrastructure context for P1.0 (Remote Airflow Server provisioning)_

---

## 1. Purpose

This briefing provides Ksolves with the hardware, storage, and network context required to provision the remote Airflow server VM (P1.0) on the MSB-PMC01 Proxmox cluster. The cluster is fqdn-managed; this document is the working reference Ksolves should use for VM placement, sizing, and storage allocation decisions during P1.0.

MSB-PMC01 runs Proxmox VE (kernel `6.8.12-20-pve`) in a hyperconverged Ceph configuration. Ksolves' provisioning activities will land VMs into this cluster but will not modify cluster, Ceph, or networking infrastructure — those remain fqdn-managed.

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

This gate must close before Ksolves begins VM provisioning. Status tracking is in `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md` § P0.7.

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

---

## 6. Open Items Affecting Final Sizing

These items remain open and may refine the P1.0 sizing before provisioning begins:

| Item | Current state | Effect on Airflow VM |
|---|---|---|
| Max concurrent Airflow task slots | Open question with fqdn stakeholders | Drives Celery worker count and broker (Redis/RabbitMQ) sizing; current 6c/24GB has headroom for a 2-job concurrent baseline but should be re-checked once concurrency target is finalized |
| Cluster outbound network path (MPLS vs DIA-direct vs DIA+VPN) | Open with fqdn networking | Determines WAN egress profile and feasible cloud staging target (Azure Blob vs AWS S3) |
| Cloud staging target | Azure Blob leading candidate, not finalized | Influences `s3a://` configuration in Airflow operators |

These do not block the start of provisioning but should be resolved before production cutover.

---

## 7. Source Data and References

This briefing draws from the following authoritative artifacts in the fqdn project repository:

- **Host inventory (lscpu, lsblk, lsmem) for all four MSB-PMC01 nodes:**
  `phases/phase2/development/Document/MSB-PMC01_cluster_host_inventory.md`
- **Ceph OSD tree (`ceph osd df tree` output):**
  `phases/phase2/development/Incoming/PMC01_OSD_Tree/PMC01_OSD_Tree.md`
- **Phase 2 critical path with P1.0 specification:**
  `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md` § P1.0, P0.7
- **Phase 1 report (delivered 2026-04-24):**
  `phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf`

---

_End of briefing._
