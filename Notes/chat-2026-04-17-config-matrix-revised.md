# Development Cluster — Revised Configuration Matrix
# 2026-04-17

## Context

Re-examination of the earlier configuration matrix (Table 1 & Table 2) originally computed under
the assumption that CSV ingest arrived from an external source and only Parquet output was stored on local Ceph. That assumption has been superseded — the remote Ceph cluster will not be available in time for the development cluster target date. CSV ingest now lands on local Ceph alongside Parquet output.

---

**Q: Re-examine the earlier config matrix given the assumption of no external storage — CSV ingest will land on local Ceph.**

---

## Updated Confirmed Inputs

| Input Parameter | Prior Assumption | Revised Value |
|---|---|---|
| Ceph stores | Parquet only (CSV external) | **CSV + Parquet + VM OS disks (all local)** |
| VM OS disk | Not sized | **80 GB/VM × 3 VMs (RHEL 9/10, RBD on Ceph)** |
| Dev max ingest | 5 TB | 5 TB (unchanged) |
| Shuffle amplification range | 3×–4× | 3×–4× (unchanged) |
| RAID controller | SR932i-p Gen11, 8 GB FBWC | Unchanged |
| NVMe/node | 7× 3.84 TB | Unchanged |
| Ceph replication | 3× | Unchanged |

---

## Revised Ceph Peak Usable Requirement

At peak, CSV ingest and Parquet output coexist on Ceph simultaneously until the Snowflake
COPY INTO is verified and both are deleted (one job lifetime retention).

| Storage Consumer | @ 4 TB Ingest | @ 5 TB Ingest |
|---|---|---|
| Raw CSV (S3/RGW) | 4.00 TB | 5.00 TB |
| Parquet output (5× compression) | 0.80 TB | 1.00 TB |
| Worker VM OS disks (3× 80 GB, 3× rep) | 0.24 TB | 0.24 TB |
| **Total usable needed** | **5.04 TB** | **6.24 TB** |

### OSD Adequacy

| OSD Configuration | Ceph Usable (TB) | @ 4 TB Ingest | @ 5 TB Ingest | Headroom @ 5 TB Peak |
|---|---|---|---|---|
| 1 OSD/node | 3.84 TB | **DISQUALIFIED** | **DISQUALIFIED** | — |
| **2 OSD/node** | **7.68 TB** | **OK** | **OK** | **+1.44 TB** |

**All 1-OSD/node configurations (A–E) are eliminated by Ceph capacity.** Only 2-OSD/node
configurations (F–J) are viable for local CSV staging at 4–5 TB ingest.

---

## Per-Node Scratch Requirement

Formula: `ingest × shuffle_amp × 2 ÷ 3 nodes`

| Ingest Scenario | Scratch Needed / Node |
|---|---|
| 5 TB @ 3× | 10.0 TB |
| 5 TB @ 4× | 13.3 TB |
| 7 TB @ 3× *(prod ref)* | 14.0 TB |
| 7 TB @ 4× *(prod ref)* | 18.7 TB |

---

## Table 1 — Capacity & Adequacy (revised)

Configs A–E shown struck through — disqualified by Ceph capacity.
Scratch adequacy columns suppressed for disqualified configs.

| Config ID | OSDs / Node | Scratch Drives | Scratch Protection | Scratch Usable / Node | Ceph Usable (TB) | Ceph Sufficient? | 5 TB @ 3× | 5 TB @ 4× | 7 TB @ 3× | 7 TB @ 4× |
|---|---|---|---|---|---|---|---|---|---|---|
| ~~A~~ | ~~1~~ | ~~6~~ | ~~JBOD~~ | ~~23.0 TB~~ | ~~3.84 TB~~ | **NO** | — | — | — | — |
| ~~B~~ | ~~1~~ | ~~6~~ | ~~RAIDZ1~~ | ~~19.2 TB~~ | ~~3.84 TB~~ | **NO** | — | — | — | — |
| ~~C~~ | ~~1~~ | ~~6~~ | ~~RAIDZ2~~ | ~~15.4 TB~~ | ~~3.84 TB~~ | **NO** | — | — | — | — |
| ~~D~~ | ~~1~~ | ~~6~~ | ~~HW RAID-5~~ | ~~19.2 TB~~ | ~~3.84 TB~~ | **NO** | — | — | — | — |
| ~~E~~ | ~~1~~ | ~~6~~ | ~~HW RAID-6~~ | ~~15.4 TB~~ | ~~3.84 TB~~ | **NO** | — | — | — | — |
| F | 2 | 5 | JBOD | 19.2 TB | 7.68 TB | YES | OK | OK | OK | OK |
| G | 2 | 5 | RAIDZ1 | 15.4 TB | 7.68 TB | YES | OK | OK | OK | **short** |
| H | 2 | 5 | RAIDZ2 | 11.5 TB | 7.68 TB | YES | OK | **short** | **short** | **short** |
| **I** | **2** | **5** | **HW RAID-5** | **15.4 TB** | **7.68 TB** | **YES** | **OK** | **OK** | **OK** | **short** |
| J | 2 | 5 | HW RAID-6 | 11.5 TB | 7.68 TB | YES | OK | **short** | **short** | **short** |

---

## Table 2 — Resiliency & Performance (viable configs only)

| Config ID | Scratch Protection | Drives Tolerated Lost | Failure Mode | Throughput vs JBOD | Spark CPU Overhead | Throughput on Failure | Job Time Impact (Normal) |
|---|---|---|---|---|---|---|---|
| F | JBOD (5d) | **0** | Data loss, job fails | 100% baseline | 0 cores | — | 0% baseline |
| G | RAIDZ1 (5d) | 1 drive | Degraded, job continues | ~92% | ~0.5–1 core | ~40–60% read | +2–4% |
| H | RAIDZ2 (5d) | 2 drives | Degraded, still protected at 1 fail | ~87% | ~1–2 cores | ~80–90% (1 fail) / ~40–60% (2 fail) | +4–7% |
| **I** | **HW RAID-5 (5d)** | **1 drive** | **Degraded, job continues** | **~99%** | **~0% (ASIC+FBWC)** | **~40–60% read** | **+0–1%** |
| J | HW RAID-6 (5d) | 2 drives | Degraded, still protected at 1 fail | ~98% | ~0% (ASIC+FBWC) | ~80–90% (1 fail) / ~40–60% (2 fail) | +1–2% |

---

## Updated Summary

| Use Case | Config ID | Key Reason |
|---|---|---|
| Max capacity, no protection | F | JBOD 5-drive, 19.2 TB scratch — zero overhead, zero fault tolerance |
| **Fault tolerance, recommended** | **I** | **HW RAID-5 on 5 drives, 15.4 TB scratch, FBWC, ~0% CPU cost, 1-drive fault tolerance** |
| 2-drive fault tolerance | J | HW RAID-6 on 5 drives, 11.5 TB scratch — short at 5 TB @ 4× shuffle |

---

## Recommended Configuration — Config I

| Configuration Item | Selected Value |
|---|---|
| NVMe drives/node | 7 total |
| OSDs/node | 2 (Ceph BlueStore) |
| Scratch drives/node | 5 (HW RAID-5 via SR932i-p Gen11 + 8 GB FBWC) |
| Ceph usable | 7.68 TB |
| Scratch usable/node | 15.4 TB |
| CPU overhead | ~0% (parity on controller ASIC) |
| Drive fault tolerance | 1 scratch drive |
| Worker VM OS | RHEL 9/10, 80 GB RBD disk on Ceph |

**Config I is the updated recommendation.** Config D (previously recommended) required only
1 OSD/node and is now eliminated by the revised Ceph requirement. Config I carries the same
SR932i-p RAID controller and FBWC advantages, covers the full 4–5 TB dev ingest range at
all shuffle amplifications, and provides single-drive fault tolerance with negligible
performance impact.

> **Config J caveat:** Provides 2-drive fault tolerance but 11.5 TB scratch falls short
> at 5 TB @ 4× shuffle amplification (13.3 TB required). Viable only if shuffle amplification
> stays at 3× or below.
