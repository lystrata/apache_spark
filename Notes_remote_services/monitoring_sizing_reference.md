# Monitoring Infrastructure — Load & Sizing Reference
_Created 2026-04-20 15:59_

All monitoring services live on the existing monitoring Proxmox cluster. This document covers the new additions and their resource requirements. Update when assumptions change or open questions are resolved.

---

## Infrastructure Overview

| Service | Instance | Status |
|---|---|---|
| Grafana (existing) | Existing VM | Running — purpose TBD |
| Loki | Existing VM | Running — log aggregation |
| Prometheus | TBD — new or existing | TBD |
| Ansible | Existing VM | Running |
| **Grafana (new)** | New VM | Planned — consolidated infrastructure monitoring |

The new Grafana instance consolidates all infrastructure dashboards: Proxmox nodes, Spark/YARN VMs, bastion services, and Ceph. It is distinct from the existing Grafana instance whose scope is TBD.

---

## Scrape Target Inventory

### Prometheus — Time Series Sources

| Target | Exporter | Series (est.) | Notes |
|---|---|---|---|
| Proxmox node 1 | node_exporter + pve_exporter + ZFS | ~1,700 | Bare metal host metrics |
| Proxmox node 2 | node_exporter + pve_exporter + ZFS | ~1,700 | |
| Proxmox node 3 | node_exporter + pve_exporter + ZFS | ~1,700 | |
| YARN / Spark VMs | node_exporter + YARN JMX | ~800 | Per VM; count TBD |
| Ceph cluster | ceph_exporter | ~1,000 | OSD, MON, MGR, RGW metrics |
| Bastion VM | node_exporter + Airflow StatsD | ~500 | |
| **Total (estimate)** | | **~12,000** | Proxmox nodes dominate cardinality |

Ceph is the highest-cardinality wildcard — OSD count and pool count multiply metric series. Confirm OSD count per node when finalizing (currently 9× NVMe per production node, but OSD allocation per node is calculator-dependent).

### Loki — Log Sources

| Source | Shipper | Log types |
|---|---|---|
| Proxmox node 1–3 | Promtail | System journal, Ceph OSD/MON/RGW, ZFS |
| YARN executor VMs | Promtail | YARN NodeManager, Spark executor, system |
| Bastion VM | Promtail | Airflow scheduler/webserver/task, History Server, JupyterHub, Nginx |
| Monitoring cluster VMs | Promtail | Grafana, Prometheus, Loki, Ansible |

---

## Per-Service Sizing

### Prometheus

| Parameter | Value | Basis |
|---|---|---|
| Total active series | ~12,000 | Scrape target inventory above |
| Scrape interval | 15 sec | Standard |
| Retention | 90 days | Aligned with existing TSDB policy |
| **TSDB disk** | **~10–15 GB** | `90d × (12,000/15) × 1.5 bytes/sample` |
| **RAM** | **4–6 GB** | ~3 KB/series in memory + chunk cache |
| **vCPU** | **2–4** | Scrape + rule evaluation load |

TSDB is not a disk concern at this scale. Even doubling series count stays under 30 GB at 90-day retention.

### Grafana (new instance)

| Component | vCPU | RAM | Disk |
|---|---|---|---|
| Grafana server | 1 | 1 GB | — |
| Dashboard DB (SQLite) | — | — | ~500 MB |
| **Total** | **1** | **1 GB** | **~1 GB** |

Grafana is not a sizing driver. Resource use grows only if many concurrent users run heavy dashboard queries simultaneously — not expected in this environment.

### Loki (existing instance — capacity impact)

Log level hierarchy (most → least verbose): TRACE > DEBUG > **INFO** > **WARN** > ERROR > FATAL. INFO includes all normal operational messages (task starts, shuffle stats, stage completions). WARN captures only abnormal conditions.

**Deployment phase plan:** run INFO during initial standup and testing; scale back to WARN for steady-state production. Size Loki disk for INFO to cover the deployment period.

| Spark Log Level | Phase | Raw log rate | Compressed (10:1) | **21-day total** |
|---|---|---|---|---|
| INFO | Initial deployment / testing | 20–100 GB/day | 2–10 GB/day | **42–210 GB** |
| WARN | Steady-state production | 1–5 GB/day | 100–500 MB/day | **2–10 GB** |

Retention: 21 days — aligned with raw compressed CSV file retention policy.

Loki server resources (unchanged by adding Promtail sources, as it is already running):

| Component | vCPU | RAM | Notes |
|---|---|---|---|
| Loki server | 2–4 | 4–8 GB | Chunk cache scales with active streams |
| Disk | — | — | Size for INFO (42–210 GB); WARN production steady-state reclaims most of this |

If Loki currently runs on a VM with limited disk, provision for INFO-level capacity at deployment time. Once stable on WARN in production, disk pressure drops significantly.

### Promtail Agents (per host)

Negligible: ~0.1 vCPU, ~100 MB RAM per host. Not a sizing concern.

---

## VM Totals — New Monitoring VM

Only the new Grafana instance requires a new VM. Prometheus may be added to an existing VM or provisioned new (TBD).

| Scenario | vCPU | RAM | Disk |
|---|---|---|---|
| Grafana only | 1 | 1 GB | 5 GB |
| Grafana + Prometheus (colocated) | 3–5 | 5–7 GB | 15–20 GB |

**Recommendation:** colocate the new Grafana and Prometheus on a single VM — **4 vCPU, 8 GB RAM, 20 GB disk**. Clean separation from the existing Grafana instance; Prometheus disk is small enough that a single volume covers OS + TSDB comfortably.

---

## Open Questions

| # | Question | Impact |
|---|---|---|
| ~~1~~ | ~~Spark log verbosity level?~~ | ~~Resolved: INFO during deployment/testing; WARN in production. Size Loki for INFO.~~ |
| 2 | What does the existing Grafana instance monitor? | Determines overlap and whether scope boundaries need defining |
| 3 | Is Prometheus new or already running on the monitoring cluster? | Determines whether this is a new VM or a config addition |
| 4 | How many YARN executor VMs per node? | Refines series count and Promtail agent deployment count |
| 5 | "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? | Scopes Grafana dashboard build-out |
| 6 | Current Loki VM disk allocation? | Determines if expansion is needed before adding cluster log sources |

---

## Retention Policy Summary

| Data type | Retention | Policy basis |
|---|---|---|
| Prometheus TSDB | 90 days | Existing policy |
| Loki logs | 21 days | Aligned with raw compressed CSV retention |
| Spark event logs (History Server) | TBD | Separate — stored in Ceph S3 |

---

## Revisions

| Date | Summary |
|---|---|
| 2026-04-20 15:59 | Initial document created — scrape target inventory, per-service sizing, Loki verbosity phases, VM totals |
