**Status:** Draft — review and send when ready
**From:** Rohn (fqdn)
**To:** Ksolves lead
**CC:** Murali (per existing Ksolves-correspondence convention)
**Date:** 2026-05-08
**Subject:** Proxmox / Ceph cluster audit — findings for verification

---

Hi [Ksolves lead],

I ran an audit of the dev cluster from `msb-pmc03-01` after your installation and configuration work and wanted to share the findings. Most of what I see is healthy and matches expectations; a handful of items I'd like to clarify before signing off, captured in § 13 below.

---

## 1. Audit context

| Field | Value |
|---|---|
| Vantage point | `msb-pmc03-01.corp.fqdn` (Node01) |
| Run timestamp | Fri May 8 12:23:49 PM MDT 2026 |
| Scope | Cluster-wide Ceph state queried from Node01 |
| Method | Bash audit script (`ceph` CLI commands) |

Cluster-wide Ceph state is captured because Ceph CLI commands query cluster state, not local node state. Per-node OS / Proxmox health (Proxmox version, LUKS state, OS-layer details) is not included in this run — see § 14.

---

## 2. Executive summary

| Aspect | Status |
|---|---|
| Overall health | ✅ HEALTH_OK |
| MON quorum | ✅ 3/3 in quorum (election epoch 336) |
| MGR availability | ✅ 1 active + 2 standby |
| OSD state | ✅ 9 / 9 up + in (epoch 118) |
| RGW | ✅ 1 daemon active (1 host, 1 zone) |
| CephFS MDS | ⚠️ Both MDS daemons in STANDBY; no active MDS reported |
| Total raw capacity | 31 TiB across 9 OSDs (~3.5 TiB each) |
| Used / available | 310 MiB used / 31 TiB available |
| Pools | 8 total, 209 PGs all `active+clean` |
| Insecure global-id reclaim | ✅ Disabled (`auth_allow_insecure_global_id_reclaim = false`) |
| Ceph version | 19.2.3 (Squid) |

---

## 3. Ceph version

```
ceph version 19.2.3 (d74d168b1c80fb01e1a30d5e4ca9a45b12bc145b) squid (stable)
```

| Field | Value |
|---|---|
| Major / minor / patch | 19.2.3 |
| Codename | Squid (stable) |

The configuration baseline document (`Ksolves_Spark_YARN_Config_v1.0.pdf`) referenced **Reef 18.2.x**; the deployed version is **Squid 19.2.3** (the next major release). Verification question in § 13.

---

## 4. Cluster status

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
| PG state | 209 active+clean |

---

## 5. Health detail

```
HEALTH_OK
```

No warnings, no errors.

---

## 6. Monitor quorum

| Field | Value |
|---|---|
| Map epoch | e3 |
| Election epoch | 336 |
| Leader | `msb-pmc03-01` (rank 0) |
| Quorum members | 0, 1, 2 → msb-pmc03-01, msb-pmc03-02, msb-pmc03-03 |

| MON | Address (v2 / msgr2) | Address (v1 / legacy) |
|---|---|---|
| msb-pmc03-01 | `10.1.37.31:3300/0` | `10.1.37.31:6789/0` |
| msb-pmc03-02 | `10.1.37.32:3300/0` | `10.1.37.32:6789/0` |
| msb-pmc03-03 | `10.1.37.33:3300/0` | `10.1.37.33:6789/0` |

---

## 7. Manager status

| Field | Value |
|---|---|
| Epoch | 87 |
| Available | true |
| Active manager | `msb-pmc03-01` |
| Standby count | 2 |

---

## 8. OSD tree

| ID | Class | Weight (TiB) | Type | Name | Status | Reweight | Primary affinity |
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

3 OSDs per node × 3 nodes = 9 OSDs total. Even distribution; weights uniform at 3.49309 TiB / OSD; reweight all 1.00000. The drives 1–3 per node are 3.84 TB NVMe; Ceph has classified them as `ssd` device class. Verification question in § 13.

---

## 9. OSD capacity & utilization

| OSD | Class | Weight | Reweight | Size | Raw use | Data | OMAP | META | Avail | %Use | VAR | PGs | Status |
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

| Distribution metric | Value |
|---|---|
| MIN VAR | 0.92 |
| MAX VAR | 1.05 |
| STDDEV | 0 |
| PG distribution | 56 – 80 (mean ~70) |

PG distribution within ±20% of the mean.

---

## 10. Pools

| ID | Name | Replication | Min size | PG num | PGP num | Autoscale | Application | Read-balance score |
|---|---|---|---|---|---|---|---|---|
| 1 | `.mgr` | 3 | 2 | 1 | 1 | on | mgr | 9.09 |
| 2 | `phi-data` | 3 | 2 | 32 | 32 | on | rgw | 1.69 |
| 3 | `vm-disks` | 3 | 2 | 32 | 32 | on | rbd | 1.69 |
| 4 | `audit-logs` | 3 | 2 | 16 | 16 | on | rgw | 2.25 |
| 5 | `.rgw.root` | 3 | 2 | 32 | 32 | on | rgw | 1.69 |
| 6 | `default.rgw.log` | 3 | 2 | 32 | 32 | on | rgw | 1.41 |
| 7 | `default.rgw.control` | 3 | 2 | 32 | 32 | on | rgw | 2.25 |
| 8 | `default.rgw.meta` | 3 | 2 | 32 | 32 | on | rgw | 1.41 |

All pools 3× replicated (size=3, min_size=2). Pool naming is interesting — `phi-data`, `audit-logs`, and `vm-disks` are all named in a production-style aligned with HIPAA scope. Verification questions in § 13.

---

## 11. Placement groups

```
209 pgs: 209 active+clean; 582 KiB data, 310 MiB used, 31 TiB / 31 TiB avail
```

All 209 PGs `active+clean`. No degraded, undersized, recovering, or backfilling PGs.

---

## 12. CephFS status

| Daemon | Host | Role | State |
|---|---|---|---|
| `msb-pmc03-01-cephFS` | msb-pmc03-01 | MDS | STANDBY |
| `msb-pmc03-03-cephFS` | msb-pmc03-03 | MDS | STANDBY |
| (none) | — | MDS | (no ACTIVE MDS reported) |

Both MDS daemons reported as STANDBY; no active MDS. `mds.msb-pmc03-02-cephFS` has an auth key (next section) but isn't appearing in the MDS status. Verification question in § 13.

---

## 13. Items for verification

These are the items I'd like to clarify before signing off on Phase 2.

### 13.1 Ceph version

The configuration baseline document (`Ksolves_Spark_YARN_Config_v1.0.pdf`) references **Ceph Reef 18.2.x**; the deployed version is **Squid 19.2.3** (one major release ahead).

- Was the upgrade to Squid 19.2.3 intentional?
- What testing has been done against Spark 3.5.3 + Hadoop 3.4.1 on this Ceph release?
- Are there any compatibility considerations with the rest of the planned stack we should track?

### 13.2 CephFS MDS state

Both deployed MDS daemons (`msb-pmc03-01-cephFS`, `msb-pmc03-03-cephFS`) are in STANDBY; no active MDS. `mds.msb-pmc03-02-cephFS` has an auth key but is not appearing in the MDS status output.

- Is CephFS expected to be active at this stage of deployment? (The pipeline diagram in § 1.1 of the configuration document shows Spark → Ceph RGW S3, not CephFS — so CephFS may be out of scope.)
- If CephFS is intended for future use, when do you plan to create the filesystem and bring an MDS active?
- Is the `mds.msb-pmc03-02-cephFS` daemon expected to be running? It has a key but isn't in the status output.

### 13.3 OSD device class

All 9 OSDs are tagged with class `ssd`. The drives 1–3 per node are 3.84 TB NVMe.

- Was `ssd` chosen deliberately, or should the class be `nvme`?
- Does the choice affect the mclock IOPS calibration profile in use?

### 13.4 Pool naming / production-readiness intent

The pools `phi-data`, `audit-logs`, and `vm-disks` are named in a HIPAA-aware production-readiness style.

- Was the `audit-logs` pool provisioned as the destination for centralized audit logging (HIPAA § 164.316(b)(2) 6-year retention)? If yes, what WORM / object-lock posture is configured on it?
- Is server-side encryption (SSE) configured on `phi-data`? (HIPAA § 164.312(a)(2)(iv) data-at-rest encryption.)
- Is the `vm-disks` pool intended as the production-style RBD pool for VM block storage?

### 13.5 mclock IOPS calibration

The Ceph config diff reports calibrated `osd_mclock_max_capacity_iops_ssd` values for OSDs 1, 2, 3, 5, and 8. OSDs 0, 4, 6, and 7 are not listed.

- Did the calibration not run on those OSDs, or did the run produce values that matched defaults?
- Should we re-run calibration on the missing OSDs to ensure consistent mclock behavior?

### 13.6 RGW server-side tuning (config doc § 6.4)

The configuration document § 6.4 recommends:

- `rgw_thread_pool_size = 512`
- `rgw_max_concurrent_requests = 1024`
- RGW daemon restart after the config change

These values do not appear in the current `ceph config diff` output.

- Has this tuning been applied yet?
- If yes, can you point us to where the values are stored (since they're not in the diff)?
- If not yet, when do you plan to apply it? This is on our cluster sign-over verification checklist.

### 13.7 LUKS posture on NVMe scratch drives

Separate from this audit, we'd like to verify the LUKS state of the NVMe scratch drives (drives 4–7 per node), since those drives are hardware-encrypted from the OEM and we LUKS-prepared them before your installation work began. This is covered in our separate follow-up correspondence; mentioning here for completeness.

---

## 14. What this audit didn't cover

The audit script ran cluster-wide Ceph commands from `msb-pmc03-01`. It did not capture per-node state, which we'll need for full Phase 2 closure verification:

- Proxmox version + cluster state (`pveversion`, `pvecm status`) per node
- LUKS posture per drive (`cryptsetup status` on drives 4–7) on each node — this is needed for the HIPAA hardware-encryption verification
- OS state on each Worker VM (RHEL install confirmation)
- YARN ResourceManager VM state
- Network MTU consistency post-resolution

We'll likely run a per-node script on each of msb-pmc03-01 / -02 / -03 to capture those. If you have a recommended audit script you've used elsewhere, that would be helpful to align our verification with your install patterns.

---

## 15. Authentication keys note

The audit script captured all cluster auth keys (MDS, OSD, client.admin) along with their capabilities. Those values are kept locally only. For future audit runs, the script will be modified to redact key values at capture time so the output is shareable by construction.

---

Thanks for the work to date. Once we have responses on § 13, we can either close out Phase 2 cleanly or capture remaining items as Phase 2 follow-ups.

Rohn

---

## Internal tracking notes (not part of the email body)

- **Source:** stripped vendor-facing version of `phases/phase2/development/Notes/proxmox_audit_2026-05-08.md`
- **What was stripped:** Critical Path / BLOCKER.* / P0.x / P2.x labels; Critical Path Document Synchronization rule references; sub-project paths; "review punch-list" framing; cross-reference table to internal CP items; AI-tracked-this voice and methodology notes
- **What was kept:** all factual technical findings, verification questions, audit-run methodology
- **What was added:** explicit "Items for verification" section (§ 13) consolidating the verification questions in vendor-facing language; a "what this audit didn't cover" section (§ 14) listing the per-node state still to capture
- **Pairs with:** the three letter drafts at `correspondence/Document/{phase2_closing_letter, h1_javax_filter_verification_letter, nvme_luks_already_encrypted_followup}_to_ksolves_2026-05-08.md`. The LUKS verification belongs in the Phase 2 closing letter + the NVMe LUKS follow-up; called out here only for completeness (§ 13.7).
