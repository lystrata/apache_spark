# msb-pmc01-04 — Resource Analysis for Co-Located Remote-Service VMs

_Created 2026-05-06_

---

## Purpose

This document captures the CPU and RAM accounting for the three planned VMs co-located on `msb-pmc01-04` (the Tier-A node within the MSB-PMC01 orchestration cluster):

1. **Airflow VM** — `airflow-prod-01` (P1.0 spec, 6 vCPU / 24 GB / 500 GB SSD, RHEL 9.4)
2. **Bastion VM** — vendor-provisioned SSH jump host
3. **Grafana / Prometheus / Loki VM** ("GPL VM") — new monitoring stack VM, decision 2026-05-06

It supersedes the now-obsolete `bastion_sizing_reference.md` (which sized a single unified bastion+Airflow VM) and the `monitoring_sizing_reference.md` totals (which assumed Grafana/Prometheus on a different host). Use this document going forward when the question is "does the host have room?".

**Ceph daemons are explicitly excluded from this accounting** per user direction 2026-05-06. The Ceph cluster's MON/MGR/OSD daemons that participate from `msb-pmc01-04` are tracked separately as cluster overhead and are not new VM allocations.

---

## Host Profile — `msb-pmc01-04`

| Attribute | Value |
|---|---|
| CPU model | Intel Xeon Gold 6136 @ 3.00 GHz (Skylake-SP) |
| Sockets | 1 |
| Cores per socket | 12 |
| Threads per core | 2 |
| **Logical CPUs** | **24** |
| Max boost clock | 3.7 GHz |
| NUMA nodes | 1 (CPUs 0–23, single domain) |
| L3 cache | 24.8 MiB (1 instance) |
| **Total RAM** | **130 GB** |
| Disk pool for VM volumes | Ceph `rbd_ssd` (~1.8 TiB / node, ~5.4 TiB cluster-wide) |

Source: `phases/phase2/development/Document/MSB-PMC01_airflow_host_briefing_v1.1.md` § 3.1.

**Single-NUMA caveat:** Hyperthreaded cores aren't 1:1 with physical cores under sustained compute. The effective throughput ceiling is closer to 12 physical cores. The numbers below stay safely under that threshold because Airflow / Loki / Prometheus / bastion workloads are bursty and largely IO-bound, not CPU-saturated.

---

## Per-VM CPU Requirements

### Airflow VM (P1.0 spec: 6 vCPU)

| Component | vCPU | Source |
|---|---|---|
| Airflow Scheduler + Celery workers | 2–4 | `bastion_sizing_reference.md` § 2.1 |
| Airflow Webserver | 1–2 | `bastion_sizing_reference.md` § 2.1 |
| PostgreSQL metadata DB | 1–2 | `bastion_sizing_reference.md` § 2.1 |
| Redis (Celery broker) | 1 | CeleryExecutor adopted 2026-04-22; required broker |
| Ansible (if co-located here) | ~0.1 | `airflow_planning_notes.md` — Python + SSH, lightweight |
| Promtail agent | ~0.1 | `monitoring_sizing_reference.md` § 2.5 |
| OS overhead | 1 | RHEL 9.4 baseline |
| **Realistic ask** | **7–10** | Range reflects scheduler load uncertainty |
| **P1.0 spec** | **6** | Phase 1 report |

**Note:** the P1.0 6 vCPU spec is **tight but workable** at 1 concurrent Spark job. Celery workers do almost nothing once they fire `spark-submit` (they wait). The host briefing v1.1 § 6 explicitly states "current 6c/24GB has comfortable headroom" for the 1-job-concurrent flow. If concurrency rises later (e.g., +1 node and 2-job concurrency), plan to bump to 8 vCPU.

### Bastion VM (not yet sized)

| Component | vCPU |
|---|---|
| SSH bastion (sshd, jump duties) | 1–2 |
| Promtail agent | ~0.1 |
| OS overhead | 1 |
| **Realistic ask** | **2–3** |

Light-weight workload; 2 vCPU is the recommended starting point.

### Grafana / Prometheus / Loki VM ("GPL VM")

| Component | vCPU | Source |
|---|---|---|
| Prometheus | 2–4 | `monitoring_sizing_reference.md` § 2.1 — ~12k active series, 15s scrape |
| Grafana | 1 | `monitoring_sizing_reference.md` § 2.2 — not a sizing driver |
| Loki | 2–4 | `monitoring_sizing_reference.md` § 2.3 — chunk cache scales with active streams |
| Promtail (own logs only) | ~0.1 | — |
| OS overhead | 1 | — |
| **Realistic ask** | **6–10** | Wide range — depends on Prometheus rule-eval load and Loki active-stream count |

---

## Host Overhead (Ceph excluded per 2026-05-06 directive)

| Service | vCPU |
|---|---|
| Proxmox VE host | 2 |
| **Host overhead total** | **2** |

Ceph daemons running on this node (1× MON, 1× MGR active-or-standby, 6× OSDs) are tracked separately as cluster overhead and are not counted against the new VM allocation.

---

## Total CPU Tally

| Allocation | vCPU | Of 24 logical CPUs |
|---|---|---|
| Proxmox VE host | 2 | 8% |
| Airflow VM | 6 | 25% |
| Bastion VM | 2–3 | 8–12% |
| GPL VM | 6–10 | 25–42% |
| **Total** | **16–21** | **67–88%** |
| **Headroom** | **3–8** | **12–33%** |

**Verdict: comfortably within capacity.** Even at the high end (21 vCPU), there's ~3 vCPU of headroom. At the low end, 8 vCPU free.

---

## RAM Sanity Check

Provided for completeness; CPU is the tighter resource.

| Allocation | RAM |
|---|---|
| Proxmox VE host | 8 GB |
| Airflow VM | 24 GB |
| Bastion VM | ~4 GB (estimate) |
| GPL VM (Prometheus 4–6 + Grafana 1 + Loki 4–8 + OS 2) | 12–16 GB |
| **Total** | **48–52 GB of 130 GB** |
| **Headroom** | **78–82 GB (~60%)** |

Plenty of RAM headroom. If a future decision adds a fourth VM (e.g., dedicated Ansible host, or splitting GPL into two VMs), there is room without disturbing the existing three.

---

## Disk Notes

VM disks are carved from the Ceph `rbd_ssd` pool (~5.4 TiB cluster-wide) per `MSB-PMC01_airflow_host_briefing_v1.1.md` § 3.2.

| VM | Disk allocation |
|---|---|
| Airflow VM | 500 GB (P1.0 spec) |
| Bastion VM | TBD — minimal (~20 GB OS + audit logs) |
| GPL VM | TBD — Prometheus TSDB and Loki chunks dominate; Loki disk varies with retention (sized separately) |

User to compute Loki and Prometheus disk based on retention policy. Reference values:
- **Prometheus TSDB:** 90-day retention at ~12k active series → ~10–15 GB
- **Loki:** 21-day retention at INFO-level (deployment phase) → 42–210 GB; at WARN-level (steady-state production) → 2–10 GB
- See `monitoring_sizing_reference.md` § 2.1 and § 2.3 for derivation.

---

## Recommendations

1. **Provision Airflow VM at the spec'd 6 vCPU.** Monitor CPU under real load; bump to 8 vCPU if scheduler queues build up or concurrency grows beyond 1 Spark job.
2. **Bastion VM at 2 vCPU.** Adequate for SSH jump duties + Promtail.
3. **GPL VM at 6 vCPU** as a starting point. Watch Prometheus rule eval and Loki ingest CPU. Bump to 8 vCPU if either pegs.
4. **Optional: split the GPL VM off to `msb-pmc01-01`** — the other unassigned Tier-A node per the host inventory (msb-pmc01-01 is currently Unassigned). That would clean up `-04` headroom and give the monitoring stack failure independence from the Airflow stack. Trade-off: more VMs to manage.

---

## Open Questions / TBDs

| # | Question | Impact |
|---|---|---|
| 1 | Ansible control node — co-located on Airflow VM or its own VM? | Adds ~1 vCPU / 1 GB if separate; ~0 if co-located |
| 2 | GPL VM final placement — `-04` (current plan) or `-01` (split)? | Affects headroom on `-04` and failure-domain separation |
| 3 | Bastion VM final sizing | Currently estimated; vendor will refine when provisioning |
| 4 | Loki retention policy for production steady-state | Drives Loki disk allocation; user computes |
| 5 | Whether to extend the host's Ceph rbd_ssd pool when adding the GPL VM disks | Capacity check, not a CPU/RAM concern |

---

## Cross-references

- `phases/phase2/development/Document/MSB-PMC01_airflow_host_briefing_v1.1.md` — host briefing for the Airflow target node (definitive host profile)
- `remote_services/Notes/bastion_sizing_reference.md` — older unified bastion VM sizing (now obsolete; superseded by this document)
- `remote_services/Notes/monitoring_sizing_reference.md` — Prometheus / Grafana / Loki per-service sizing references
- `remote_services/Notes/airflow_planning_notes.md` — Airflow architecture rationale
- `remote_services/Notes/remote_service_host_notes.md` — original "remote service host" concept (April 2026; partially superseded — see TODO entries from 2026-05-05/06 for which services were dropped)
- `TODO.md` § Production Architecture Prep + § Pending Tasks > Remote Services Provisioning — current status of each VM and service

---

## Revisions

| Date | Summary |
|---|---|
| 2026-05-06 | Initial document — CPU/RAM accounting for Airflow + Bastion + GPL VMs on `msb-pmc01-04`; Ceph daemons excluded per user directive; supersedes `bastion_sizing_reference.md` totals |
