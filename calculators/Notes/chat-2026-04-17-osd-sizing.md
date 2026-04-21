# Development Cluster — Ceph OSD Sizing Report
# 2026-04-17

## Cluster Hardware (Development)

| Hardware Item | Specification |
|---|---|
| Nodes | 3 |
| Cores/node | 32 (single socket) |
| RAM/node | 384 GB (12× 32 GB DIMMs) |
| NVMe/node | 7× 3.84 TB |
| SSD/node | 3× 480 GB (Proxmox OS — ZFS mirror + hot spare) |
| Ceph replication | 3× |

---

**Q: Did we previously discuss the total number of OSDs required for VMs, ingest, and Parquet output for the development cluster at 4–5 TB ingest?**

We had covered Parquet-only Ceph sizing (assuming CSV arrived from an external source) but had not yet sized VM disk storage on Ceph RBD. That gap was identified and addressed in this session.

---

**Q: External ingest flat file storage is taken out of the equation — the remote Ceph cluster will not be available in time. CSV ingest will land on local Ceph.**

This changes the Ceph sizing significantly. At peak, both the raw CSV ingest **and** the Parquet
output coexist on local Ceph simultaneously — until the Snowflake COPY INTO is verified and both are deleted (one job lifetime retention).

**Revised peak Ceph usable requirement:**

| Single Job Ingest Size | Raw CSV (S3/RGW) | Parquet Output (5× compress) | Peak S3 Required |
|---|---|---|---|
| 4 TB | 4.0 TB | 0.8 TB | **4.8 TB** |
| 5 TB | 5.0 TB | 1.0 TB | **6.0 TB** |

1 OSD/node (3.84 TB usable) is no longer sufficient at any ingest size in the 4–5 TB range.
**2 OSD/node is the minimum.**

---

**Q: Size the VM disks on Ceph to confirm whether 2 OSD/node holds.**

**Q: The calculator shows 1 worker VM per node (3 total). OS will be RHEL 9 or 10. Estimate disk size with 10% headroom. The 3× 480 GB SSDs are Proxmox OS only.**

### Worker VM Configuration (from calculator screenshot)

| VM Setting | Configured Value |
|---|---|
| VMs per node | 1 |
| Total worker VMs | 3 |
| vCPUs per VM | 14 |
| RAM per VM | 256 GB |
| Optional services | All OFF — remote service host |
| YARN RM | Always reserved, amortized ÷3 |

### Spark Worker VM OS Disk Estimate (RHEL 9/10)

| Software / Storage Item | Allocated Size |
|---|---|
| RHEL 9/10 Server (no GUI) | ~10–12 GB |
| Red Hat subscription manager + Insights client | ~1 GB |
| JDK 17 (Spark requirement) | ~500 MB |
| Spark + YARN binaries | ~2 GB |
| Python 3 + PySpark + dependencies | ~3 GB |
| YARN + Spark log space (rotated) | ~25 GB |
| /tmp + working space | ~15 GB |
| **Subtotal** | **~57 GB** |
| **+10% headroom** | **~63 GB → 80 GB** |

RHEL 9/10 adds ~2–3 GB over community distributions due to enterprise subscription tooling
and Red Hat Insights client. This is absorbed within the 10% headroom. **80 GB per VM.**

> **Note:** RHEL 9/10 requires active subscription for updates and security patches. If nodes
> have restricted outbound access, a local Red Hat Satellite server or subscription proxy will
> be required. No disk impact but confirm with RHEL admin before deployment.

### VM Disk Ceph Consumption

| Disk Allocation | Raw Ceph Consumed | Ceph Usable (TB) |
|---|---|---|
| 3 VMs × 80 GB OS disk | 240 GB logical × 3× replication = 720 GB raw | **0.24 TB** |

---

## Total Ceph Usable Required — 4–5 TB Ingest Range

| Storage Consumer | @ 4 TB Ingest | @ 5 TB Ingest |
|---|---|---|
| Raw CSV (S3/RGW) | 4.00 TB | 5.00 TB |
| Parquet output (5× compression) | 0.80 TB | 1.00 TB |
| Worker VM OS disks (3× 80 GB, 3× rep) | 0.24 TB | 0.24 TB |
| **Total usable needed** | **5.04 TB** | **6.24 TB** |

---

## OSD Configuration Verdict

| OSD Config | Ceph Usable (TB) | @ 4 TB Ingest | @ 5 TB Ingest | Headroom @ 5 TB Peak |
|---|---|---|---|---|
| 1 OSD/node (3.84 TB usable) | 3.84 TB | short | short | — |
| **2 OSD/node (7.68 TB usable)** | **7.68 TB** | **OK** | **OK** | **+1.44 TB** |
| 3 OSD/node (11.52 TB usable) | 11.52 TB | OK | OK | +5.28 TB |

**2 OSD/node is confirmed sufficient** for the full 4–5 TB ingest range including VM OS disks,
with 1.44 TB headroom at the 5 TB ceiling.

---

## Scratch Drive Impact (7 NVMe − 2 OSD = 5 scratch drives/node)

Per-node scratch requirement formula: `ingest × shuffle_amp × 2 ÷ 3 nodes`

| Ingest Scenario | Scratch Needed / Node |
|---|---|
| 4 TB @ 3× | 8.0 TB |
| 4 TB @ 4× | 10.7 TB |
| 5 TB @ 3× | 10.0 TB |
| 5 TB @ 4× | 13.3 TB |

| Scratch Configuration | Scratch Usable / Node | 4 TB @ 4× | 5 TB @ 3× | 5 TB @ 4× |
|---|---|---|---|---|
| JBOD (5-drive) | 19.2 TB | OK | OK | OK |
| **HW RAID-5 (5-drive)** | **15.4 TB** | **OK** | **OK** | **OK** |
| HW RAID-6 (5-drive) | 11.5 TB | OK | OK | **short** |

---

## Recommended Configuration

**2 OSD/node + HW RAID-5 on 5 scratch drives**

| Configuration Item | Selected Value |
|---|---|
| NVMe drives/node | 7 total |
| OSDs/node | 2 (Ceph BlueStore) |
| Scratch drives/node | 5 (HW RAID-5 via SR932i-p Gen11) |
| Ceph usable | 7.68 TB |
| Scratch usable/node | 15.4 TB |
| Write cache | 8 GB FBWC (Flash-Backed Write Cache) |
| CPU overhead | ~0% (parity on controller ASIC) |
| Drive fault tolerance | 1 drive |
| Worker VM OS | RHEL 9 or 10, 80 GB RBD disk on Ceph |

Covers full 4–5 TB ingest range at all shuffle amplifications with single-drive fault tolerance
and negligible performance overhead from RAID parity.
