# Bastion Host — Load & Sizing Reference
_Created 2026-04-20 15:59_

This document is the single source of truth for the numbers used to size the Airflow bastion VM on the second Proxmox cluster. Update it when assumptions change or open questions are resolved.

---

## Workload Characterization

| Parameter | Value | Source / Notes |
|---|---|---|
| Daily ingest volume | 2 TB/day | Production target |
| Ingest schedule | TBD | Batch window timing unknown |
| Spark job concurrency | TBD | Max simultaneous jobs at peak |
| DAG count | TBD | Total scheduled pipelines |
| Concurrent Airflow task slots | TBD | Drives executor sizing |
| Jupyter concurrent users | TBD | Affects remote host CPU/RAM floor |
| Spark event log location | TBD | S3/Ceph RGW bucket or HDFS path — needed by History Server |

---

## Service Inventory

Services already running on the second Proxmox cluster (no new infrastructure required):

| Service | Status |
|---|---|
| Grafana + Prometheus | Running |
| Ansible | Running |

Services to be deployed as the new Airflow bastion VM:

| Service | Executor / Mode | Status |
|---|---|---|
| Airflow Webserver | — | Planned |
| Airflow Scheduler | LocalExecutor (assumed) | Planned |
| Airflow Metadata DB | PostgreSQL | Planned |
| Spark History Server | Reads from S3/Ceph RGW | Planned |
| JupyterHub | YARN client mode | Planned |
| Nginx reverse proxy | Exposes YARN UI, Airflow UI, History Server | Planned |
| Promtail agent | Ships logs to existing Loki instance | Planned |
| Redis | Only if CeleryExecutor adopted | Conditional |

Log aggregation is handled by the existing Loki + Grafana infrastructure. No separate logging VM is required. The bastion VM runs a Promtail agent that tails Airflow, History Server, JupyterHub, and Nginx log files and ships them to Loki. The 3-node cluster nodes each get their own Promtail agent (separate deployment, not part of this VM).

---

## Per-Service Sizing Estimates

Ranges reflect uncertainty in open questions. Resolved inputs will collapse these to point estimates.

### Airflow (LocalExecutor)

| Component | vCPU | RAM | Disk |
|---|---|---|---|
| Scheduler + Workers | 2–4 | 4 GB | — |
| Webserver | 2 | 2 GB | — |
| PostgreSQL metadata DB | 2 | 2–4 GB | 20–50 GB |
| **Subtotal** | **6–8** | **8–10 GB** | **20–50 GB** |

Basis: LocalExecutor runs workers inside the scheduler process. No Redis required. Scales with DAG count and concurrent task slots (TBD).

If CeleryExecutor is adopted: add 1 vCPU / 1 GB RAM for Redis; add 2–4 vCPU / 4–8 GB RAM per dedicated worker process.

### Spark History Server

| Component | vCPU | RAM | Disk |
|---|---|---|---|
| History Server | 2–4 | 4–16 GB | Minimal (reads from S3) |

RAM scales with number of completed jobs held in memory. 8 GB is a reasonable starting point for a daily-batch workload; 16 GB if retaining many weeks of history or debugging large jobs.

### JupyterHub

| Concurrent users | vCPU | RAM |
|---|---|---|
| 1–2 | 2 | 4 GB |
| 3–5 | 4 | 8 GB |

Spark drivers for interactive sessions run on this host in YARN client mode. Driver memory per session is workload-dependent; assume 2–4 GB per active session.

### Nginx Reverse Proxy

Negligible: 1 vCPU, 512 MB RAM. Not a sizing driver.

### Log Shipping (Promtail Agent)

Promtail is a lightweight agent — not a sizing driver for this VM.

| Component | vCPU | RAM | Disk |
|---|---|---|---|
| Promtail | 0.1 (negligible) | ~100 MB | None (ships to remote Loki) |

Promtail tails: Airflow scheduler/webserver/task logs, History Server logs, JupyterHub logs, Nginx access/error logs, and system journal. All storage burden lands on the existing Loki host, not this VM.

**Log volume estimate for Loki capacity planning:** 3 cluster nodes + bastion VM generating YARN logs, executor logs, Ceph logs, and system logs. At 2 TB/day ingest with default Spark verbosity, expect 10–50 GB/day of raw log text across all sources. Retention period (TBD) is the primary driver of Loki disk growth — this is a capacity question for the existing Loki host, not this VM.

---

## VM Totals (Preliminary)

Log stack resolved: Loki + Grafana already in place; bastion VM carries only a Promtail agent. ELK eliminated from consideration.

| Component | vCPU | RAM | Disk |
|---|---|---|---|
| Airflow (scheduler, webserver, Postgres) | 6–8 | 8–10 GB | 20–50 GB |
| Spark History Server | 2–4 | 4–16 GB | Minimal |
| JupyterHub (1–2 concurrent users) | 2–4 | 4–8 GB | 20 GB |
| Nginx + Promtail | 1 | 1 GB | Minimal |
| OS + headroom | 2 | 2 GB | 20 GB |
| **Total** | **13–19** | **19–37 GB** | **60–90 GB** |

Recommended starting point: **16 vCPU, 32 GB RAM, 100 GB disk** — midpoint of the range, with disk sized for OS, Postgres WAL/history, and Jupyter workspace. Loki handles all log retention externally.

Primary remaining uncertainty: History Server RAM (4–16 GB range). Resolves once job history retention policy and event log location are confirmed (open questions 3 and 4).

---

## Second Proxmox Host — Available Resources

| Parameter | Value |
|---|---|
| Host specs | **TBD** |
| Available vCPU headroom | TBD |
| Available RAM headroom | TBD |
| Storage pool / available disk | TBD |

---

## Open Questions

Resolved questions should be struck through and the relevant table cells above updated with the confirmed value.

| # | Question | Impact |
|---|---|---|
| 1 | Airflow executor type? (LocalExecutor assumed) | Changes Redis requirement and worker RAM |
| ~~2~~ | ~~Log aggregation stack?~~ | ~~Resolved: existing Loki + Grafana; Promtail agent on bastion VM~~ |
| ~~3~~ | ~~Log retention target?~~ | ~~Resolved: 21 days — aligned with raw compressed CSV file retention policy~~ |
| 4 | Spark event log location? (S3 bucket name / HDFS path) | History Server config; confirms read path |
| 5 | Second Proxmox host specs? | Sets ceiling on VM allocation |
| 6 | Max concurrent Airflow task slots? | Scheduler RAM and CPU floor |
| 7 | Concurrent Jupyter users? | Driver memory reservation |
| 8 | Ingest batch window? | Validates that job concurrency assumptions are reasonable |
| 9 | Is floating S3 IP routable from bastion host's network segment? | Determines if a static route or VPN is needed |

---

## Network Requirements

The bastion VM needs reachable paths to:

| Destination | Port | Purpose |
|---|---|---|
| YARN ResourceManager | 8032 | spark-submit job submission |
| YARN ResourceManager UI | 8088 | Nginx proxy target |
| Ceph RGW / S3 endpoint (floating IP) | 80 / 443 | Data read/write; event log access |
| All cluster nodes | Ephemeral | YARN client mode (Jupyter) — driver-to-executor comms |
| Loki instance | 3100 | Promtail log shipping |

Confirm with network team that the exaBGP-announced floating IP is routable from the second Proxmox cluster's network segment.

---

## Revisions

| Date | Summary |
|---|---|
| 2026-04-20 15:59 | Initial document created — workload characterization, service inventory, per-service sizing, VM totals, network requirements |
| 2026-04-20 15:59 | Log aggregation resolved: Promtail → existing Loki; ELK eliminated; VM totals updated |
| 2026-04-20 15:59 | Log retention resolved: 21 days, aligned with raw compressed CSV retention policy |
