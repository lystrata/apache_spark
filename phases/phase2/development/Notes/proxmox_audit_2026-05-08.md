# Proxmox / Ceph Cluster Audit — 2026-05-08

**Source:** Bash audit script run by Rohn (fqdn) on the dev cluster after Ksolves' installation and configuration work.
**Vantage point:** `msb-pmc03-01.corp.fqdn` (Node01) — cluster-wide state captured from this node.
**Run timestamp:** Fri May 8 12:23:49 PM MDT 2026
**Raw output:** `phases/phase2/development/Incoming/proxmox_audit.md` (gitignored — contains auth keys)
**This document:** sanitized, formatted, redacted version safe for git tracking and review.

---

## Executive Summary

| Aspect | Status |
|---|---|
| Overall health | ✅ HEALTH_OK |
| MON quorum | ✅ 3/3 in quorum (epoch 336) |
| MGR availability | ✅ 1 active + 2 standby |
| OSD state | ✅ 9 / 9 up + in (epoch 118) |
| RGW | ✅ 1 daemon active (1 host, 1 zone) |
| CephFS MDS | ⚠️ Both MDS daemons in STANDBY; no active MDS reported |
| Total raw capacity | 31 TiB across 9 OSDs (~3.5 TiB each) |
| Used / available | 310 MiB used / 31 TiB avail (essentially empty) |
| Pools | 8 total, 209 PGs all `active+clean` |
| Insecure global-id reclaim | ✅ Disabled (`auth_allow_insecure_global_id_reclaim = false`) |
| Ceph version | **19.2.3 (Squid)** — see version-drift note below |

### Key findings worth flagging

1. **Ceph version drift from vendor baseline.** The vendor configuration document (`Ksolves_Spark_YARN_Config_v1.0.pdf`) calls for **Ceph Reef 18.2.x**. The deployed version is **19.2.3 (Squid)** — the next major release. This may be a deliberate upgrade decision by Ksolves or a drift from the baseline. **Action item: confirm with vendor whether the Squid upgrade was intentional and what testing has been done against Spark 3.5.3 + Hadoop 3.4.1.** Tracked in TODO follow-ups.
2. **No active CephFS MDS.** Both MDS daemons (`msb-pmc03-01-cephFS`, `msb-pmc03-03-cephFS`) are in STANDBY state. No active MDS is reported, which means **no CephFS filesystem is currently mounted/active**. This may be intentional (no CephFS provisioned yet) or a configuration gap. **Action item: confirm with vendor whether CephFS is expected to be active at this stage of Phase 2.**
3. **OSD device class is `ssd`, not `nvme`.** All 9 OSDs are tagged with class `ssd`. Since the dev cluster's drives 1–3 per node are NVMe (per `CLAUDE.md § Hardware Reference`), this is a Ceph classification choice. **Implication:** mclock IOPS tuning calibrated to SSD profiles (see Ceph Config Diff section). If NVMe-specific tuning is desired (different `osd_op_queue` parameters), the device class would need to be reclassed.
4. **Pool naming reveals HIPAA-aware production-readiness intent.** The pools `phi-data`, `audit-logs`, and `vm-disks` are named in a production-style aligned with HIPAA scope. `phi-data` ties to BLOCKER.3 (HIPAA encryption); `audit-logs` ties to P2.9 (centralized audit logging). **Implication:** the vendor's Phase 2 work has set up pool topology that anticipates production usage patterns; SSE / encryption-at-rest configuration on these pools should be verified during BLOCKER.3a review.
5. **Cluster is essentially empty.** 310 MiB used of 31 TiB available (200 objects, 582 KiB data). Phase 2 has provisioned the storage layer but no actual workload data has landed yet — consistent with VMs being created but RHEL OS not yet installed (P0.1b open).

---

## 1. Ceph Version

```
ceph version 19.2.3 (d74d168b1c80fb01e1a30d5e4ca9a45b12bc145b) squid (stable)
```

| Field | Value |
|---|---|
| Major / minor / patch | 19.2.3 |
| Codename | Squid (stable) |
| Vendor baseline (`Ksolves_Spark_YARN_Config_v1.0.pdf`) | **Reef 18.2.x** |
| Deployed | **Squid 19.2.3** |
| Drift | One major release ahead |

---

## 2. Cluster Status

```
cluster:
  id:     fae5c441-0dab-4936-8473-723ab4b24287
  health: HEALTH_OK
```

| Service | Count | Detail |
|---|---|---|
| MON | 3 daemons | Quorum: msb-pmc03-01, msb-pmc03-02, msb-pmc03-03 (age 2d) |
| MGR | 1 active + 2 standby | Active: msb-pmc03-01 (since 2d); standbys: msb-pmc03-02, msb-pmc03-03 |
| OSD | 9 total | 9 up (since 3h), 9 in (since 3h) |
| RGW | 1 daemon active | 1 host, 1 zone |

| Data metric | Value |
|---|---|
| Pools | 8 |
| Placement groups | 209 |
| Objects | 199 |
| Object data | 582 KiB |
| Used | 310 MiB |
| Available | 31 TiB |
| Total capacity | 31 TiB |
| PG state | 209 active+clean |

---

## 3. Health Detail

```
HEALTH_OK
```

No warnings, no errors. Cluster is in nominal state.

---

## 4. Monitor Quorum

| Field | Value |
|---|---|
| Map epoch | e3 |
| Election epoch | 336 |
| Leader | `msb-pmc03-01` (rank 0) |
| Quorum members | 0, 1, 2 → msb-pmc03-01, msb-pmc03-02, msb-pmc03-03 |
| Removed ranks | (none) |
| Disallowed leaders | (none) |

| MON | Address (v2 / msgr2) | Address (v1 / legacy) |
|---|---|---|
| msb-pmc03-01 | `10.1.37.31:3300/0` | `10.1.37.31:6789/0` |
| msb-pmc03-02 | `10.1.37.32:3300/0` | `10.1.37.32:6789/0` |
| msb-pmc03-03 | `10.1.37.33:3300/0` | `10.1.37.33:6789/0` |

These IPs match the documented dev-cluster Spark node management IPs (`security/Notes/vendor-access-isolation-plan_2026-05-06.md` Known Endpoints).

---

## 5. Manager Status

| Field | Value |
|---|---|
| Epoch | 87 |
| Available | true |
| Active manager | `msb-pmc03-01` |
| Standby count | 2 |

---

## 6. OSD Tree

| ID | Class | Weight (TiB) | Type | Name | Status | Reweight | Primary Affinity |
|---|---|---|---|---|---|---|---|
| -1 | — | 31.43779 | root | default | — | — | — |
| -3 | — | 10.47926 | host | msb-pmc03-01 | — | — | — |
| 0 | ssd | 3.49309 | osd | osd.0 | up | 1.00000 | 1.00000 |
| 1 | ssd | 3.49309 | osd | osd.1 | up | 1.00000 | 1.00000 |
| 2 | ssd | 3.49309 | osd | osd.2 | up | 1.00000 | 1.00000 |
| -5 | — | 10.47926 | host | msb-pmc03-02 | — | — | — |
| 3 | ssd | 3.49309 | osd | osd.3 | up | 1.00000 | 1.00000 |
| 4 | ssd | 3.49309 | osd | osd.4 | up | 1.00000 | 1.00000 |
| 5 | ssd | 3.49309 | osd | osd.5 | up | 1.00000 | 1.00000 |
| -7 | — | 10.47926 | host | msb-pmc03-03 | — | — | — |
| 6 | ssd | 3.49309 | osd | osd.6 | up | 1.00000 | 1.00000 |
| 7 | ssd | 3.49309 | osd | osd.7 | up | 1.00000 | 1.00000 |
| 8 | ssd | 3.49309 | osd | osd.8 | up | 1.00000 | 1.00000 |

**Topology:** 3 OSDs per node × 3 nodes = 9 OSDs total. Even distribution; weights uniform at 3.49309 TiB / OSD; reweight all 1.00000 (balanced).

**Note:** Class `ssd` for all OSDs. Per `CLAUDE.md § Hardware Reference`, the dev cluster's drives 1–3 per node are 3.84 TB NVMe; Ceph has classified them as `ssd` (not `nvme`). See finding #3 above.

---

## 7. OSD Capacity & Utilization (`ceph osd df`)

| OSD | Class | Weight | Reweight | Size | Raw Use | Data | OMAP | META | Avail | %Use | VAR | PGs | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 32 MiB | 1.2 MiB | 1 KiB | 30 MiB | 3.5 TiB | 0 | 0.92 | 73 | up |
| 1 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.2 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.03 | 80 | up |
| 2 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.7 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.05 | 56 | up |
| 3 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.7 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.05 | 72 | up |
| 4 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 32 MiB | 1.2 MiB | 1 KiB | 30 MiB | 3.5 TiB | 0 | 0.92 | 69 | up |
| 5 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.2 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.03 | 68 | up |
| 6 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.2 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.03 | 65 | up |
| 7 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 32 MiB | 1.7 MiB | 1 KiB | 30 MiB | 3.5 TiB | 0 | 0.93 | 66 | up |
| 8 | ssd | 3.49309 | 1.00000 | 3.5 TiB | 36 MiB | 1.2 MiB | 1 KiB | 34 MiB | 3.5 TiB | 0 | 1.03 | 78 | up |
| **TOTAL** | — | — | — | **31 TiB** | **310 MiB** | **12 MiB** | **14 KiB** | **298 MiB** | **31 TiB** | **0** | — | — | — |

**Distribution metrics:**

| Metric | Value |
|---|---|
| MIN VAR | 0.92 |
| MAX VAR | 1.05 |
| STDDEV | 0 |
| PG distribution | 56 – 80 (range 24, mean ~70) |

PG distribution is even within ±20% of the mean. No re-balancing needed at this point.

---

## 8. Pools

| ID | Name | Replication | Min size | PG num | PGP num | Autoscale | Application | Read-balance score | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `.mgr` | 3 | 2 | 1 | 1 | on | mgr | 9.09 | Manager pool |
| 2 | `phi-data` | 3 | 2 | 32 | 32 | on | rgw | 1.69 | **HIPAA scope — ePHI** |
| 3 | `vm-disks` | 3 | 2 | 32 | 32 | on | rbd | 1.69 | RBD volumes for VM disks |
| 4 | `audit-logs` | 3 | 2 | 16 | 16 | on | rgw | 2.25 | **Ties to P2.9 — centralized audit logging** |
| 5 | `.rgw.root` | 3 | 2 | 32 | 32 | on | rgw | 1.69 | RGW infrastructure |
| 6 | `default.rgw.log` | 3 | 2 | 32 | 32 | on | rgw | 1.41 | RGW infrastructure |
| 7 | `default.rgw.control` | 3 | 2 | 32 | 32 | on | rgw | 2.25 | RGW infrastructure |
| 8 | `default.rgw.meta` | 3 | 2 | 32 | 32 | on | rgw | 1.41 | RGW infrastructure (autoscale bias 4) |

**Pool composition observations:**

- All pools are 3× replicated (size=3, min_size=2) — vendor-recommended posture per CP v1.5 (P0.0 Ksolves Actions).
- Three "named-for-purpose" pools: **`phi-data`** (ePHI workload), **`audit-logs`** (HIPAA audit-trail destination), **`vm-disks`** (VM block storage). The `audit-logs` pool naming is meaningful — it suggests Ksolves has provisioned the storage substrate for the centralized audit logging task (P2.9) we added in v1.5; need to confirm the connection.
- Standard RGW infrastructure pools (`.rgw.root`, `default.rgw.log`, `default.rgw.control`, `default.rgw.meta`) — expected.
- All pools use `rjenkins` object hashing and have `autoscale_mode=on` — standard.

**Action items derived:**

- Verify SSE (server-side encryption) configuration on `phi-data` (HIPAA § 8.2 requirement)
- Confirm whether `audit-logs` pool will be the destination for P2.9 centralized audit logging (and what WORM / retention policy is configured if so)
- Confirm `vm-disks` pool is the rbd_ssd-equivalent surface for production-style VM block storage

---

## 9. Placement Groups

```
209 pgs: 209 active+clean; 582 KiB data, 310 MiB used, 31 TiB / 31 TiB avail
```

All 209 PGs are in `active+clean` state. No degraded, undersized, recovering, or backfilling PGs reported.

---

## 10. CephFS Status

```
STANDBY MDS:
  msb-pmc03-01-cephFS
  msb-pmc03-03-cephFS

MDS version: ceph version 19.2.3 (d74d168b1c80fb01e1a30d5e4ca9a45b12bc145b) squid (stable)
```

| Daemon | Host | Role | State |
|---|---|---|---|
| `msb-pmc03-01-cephFS` | msb-pmc03-01 | MDS | STANDBY |
| `msb-pmc03-03-cephFS` | msb-pmc03-03 | MDS | STANDBY |
| (none) | — | MDS | (no ACTIVE MDS reported) |

**⚠️ Finding (re-stated from Executive Summary):** No CephFS filesystem appears to be currently active. Either:

- Two MDS daemons have been deployed but no CephFS filesystem has been created yet, OR
- A filesystem exists but no MDS is rank-0 active

**Action items:**

- Verify with vendor whether CephFS is in scope for the dev cluster (vendor doc § 1.1 Pipeline shows Spark → Ceph RGW S3, not CephFS — so CephFS may be out of scope for the data path)
- Confirm MDS-on-msb-pmc03-02 status (only -01 and -03 reported)
- If CephFS is intended for production, confirm filesystem creation timing

---

## 11. Ceph Config (Diff from Defaults)

Only non-default config values are reported here.

| Who | Mask | Level | Option | Value | RO |
|---|---|---|---|---|---|
| mon | — | advanced | `auth_allow_insecure_global_id_reclaim` | **false** | (RW) |
| osd.1 | — | basic | `osd_mclock_max_capacity_iops_ssd` | 70851.449262 | (RW) |
| osd.2 | — | basic | `osd_mclock_max_capacity_iops_ssd` | 78995.761640 | (RW) |
| osd.3 | — | basic | `osd_mclock_max_capacity_iops_ssd` | 79192.592452 | (RW) |
| osd.5 | — | basic | `osd_mclock_max_capacity_iops_ssd` | 79819.178697 | (RW) |
| osd.8 | — | basic | `osd_mclock_max_capacity_iops_ssd` | 73021.914826 | (RW) |

**Observations:**

- **`auth_allow_insecure_global_id_reclaim = false`** — secure posture. This guards against CVE-2021-20288 (insecure `global_id` reclaim in pre-Pacific Ceph clients). Good.
- **mclock IOPS calibration** — Ceph 18+/19 uses mclock as the default OP scheduler; calibrated IOPS values were measured for OSDs 1, 2, 3, 5, and 8. **OSDs 0, 4, 6, 7 are missing from this list** — either they didn't get calibrated, or they ran but produced no diff value. **Action item: re-run calibration on the missing OSDs to ensure consistent mclock behavior across the cluster, or confirm with vendor that the missing values are intentional.**
- **Vendor § 6.4 RGW tuning not visible.** Vendor's recommended `rgw_thread_pool_size 512` and `rgw_max_concurrent_requests 1024` (per CP v1.5 § P0.6) are NOT present in this config diff. Either P0.6 hasn't been applied yet, or the values are at defaults that match what the vendor doc recommends. **Action item: verify P0.6 RGW server-side tuning is in place — this is on the cluster sign-over verification checklist.**

---

## 12. Authentication Keys

**Section redacted.** The raw output contains all cluster auth keys (MDS, OSD, client.admin, etc.) with full caps. Those keys are real cluster credentials — they belong only in the gitignored `Incoming/` raw file, not in any tracked document.

For audit purposes, the **structure** of the keys is captured here without secrets:

| Entity | Keys present | Capabilities (caps) |
|---|---|---|
| `mds.msb-pmc03-01-cephFS` | yes | `[mds] allow *`, `[mon] allow profile mds`, `[osd] allow rwx` |
| `mds.msb-pmc03-02-cephFS` | yes | `[mds] allow *`, `[mon] allow profile mds`, `[osd] allow rwx` |
| `mds.msb-pmc03-03-cephFS` | yes | `[mds] allow *`, `[mon] allow profile mds`, `[osd] allow rwx` |
| `osd.0` – `osd.8` | yes (9 keys) | `[mgr] allow profile osd`, `[mon] allow profile osd`, `[osd] allow *` |
| `client.admin` | yes | `[mds] allow *`, `[mgr] allow *`, (truncated in output — see raw file for `[mon]` and `[osd]` caps) |

**⚠️ Note:** `mds.msb-pmc03-02-cephFS` has a key in the auth list, but the CephFS Status section earlier reports only `msb-pmc03-01-cephFS` and `msb-pmc03-03-cephFS` as STANDBY MDS daemons. The MDS daemon on msb-pmc03-02 has a key but isn't appearing in the status — possibly stopped, possibly mid-startup. **Action item: confirm msb-pmc03-02 MDS daemon state.**

**Raw output ended mid-`client.admin` caps list** (line 168 was the last line read). The raw file may have been truncated at capture time, or the script terminated early.

For the actual key values: `phases/phase2/development/Incoming/proxmox_audit.md` (gitignored).

---

## 13. Cross-References to Critical Path

This audit informs several CP v1.5 items. Action items derived above feed:

| Action item | CP item | Notes |
|---|---|---|
| Confirm Ceph version drift (Reef 18.2.x → Squid 19.2.3) | P0.0 (Ceph Cluster Bootstrap) | Vendor decision; needs explicit sign-off |
| Confirm CephFS scope | P0.0 + outside-scope check | Vendor doc § 1.1 Pipeline doesn't include CephFS |
| Confirm OSD class `ssd` vs `nvme` | P0.0 | mclock tuning implications |
| Verify SSE on `phi-data` pool | BLOCKER.3a + 3b (HIPAA hardware + at-rest) | Pool is HIPAA-named |
| Verify `audit-logs` pool usage | P2.9 (Centralized Audit Logging + Retention) | Vendor may have provisioned the substrate already |
| Verify P0.6 RGW server-side tuning | P0.6 (Ceph RGW Server-Side Tuning) | Not visible in current config diff |
| Confirm mclock calibration on missing OSDs (0, 4, 6, 7) | P0.0 | OSD performance consistency |
| Confirm msb-pmc03-02 MDS daemon state | P0.0 / cluster sign-over checklist | Has key but not in STANDBY list |

These should be folded into the Phase 2 closing letter (`correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md`) or into a separate cluster-handover verification request when the time comes.

---

## 14. Audit-Run Methodology Notes

- **Vantage point:** Run from `msb-pmc03-01` only; output is cluster-wide because Ceph commands query the cluster state, not the local node.
- **Per-node visibility:** This audit doesn't include per-node OS / Proxmox health (`pveversion`, `systemctl status pve-cluster`, `lsblk -f` for LUKS detection, `cryptsetup status` per device, `top` / `free` snapshots). To check those, run a per-node audit script on each of msb-pmc03-01 / -02 / -03.
- **Auth keys captured:** the raw script captured all auth keys. For future audit runs, consider redacting in-script (e.g., `ceph auth ls | sed 's/key:.*/key: <REDACTED>/'`) so the raw output is git-safe by construction.
- **What's missing for Phase 2 closure verification:**
  - OS-layer state on each Worker VM (P0.1b OS install confirmation)
  - LUKS posture on NVMe scratch drives (BLOCKER.3a verification)
  - YARN RM VM state (P0.2 confirmation)
  - Vendor's § 6.4 RGW tuning presence (P0.6)
  - Network connectivity / MTU verification post-resolution (P0.7)

---

_Created 2026-05-08 from raw audit output. Review and append findings as needed._
