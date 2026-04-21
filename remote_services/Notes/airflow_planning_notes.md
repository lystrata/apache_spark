# Airflow Planning Notes
_2026-04-10 — updated 2026-04-10_

---

## What is Airflow?

Apache Airflow is a workflow orchestration platform. Pipelines are defined as **DAGs** (Directed Acyclic Graphs) in Python — each node in the graph is a task (run this Spark job, wait for that file, trigger this API call). Airflow's scheduler watches the clock, fires tasks in dependency order, retries failures, and provides a web UI to monitor runs.

In this environment it would serve as the **conductor** for the daily ETL: trigger CSV ingest → submit Spark job to YARN → on success, run COPY INTO Snowflake.

### Resource footprint (LocalExecutor, single-pipeline)

| Component | Typical footprint | Notes |
|---|---|---|
| Scheduler | 1 vCPU, 1–2 GB RAM | Always running |
| Webserver | 1 vCPU, 1–2 GB RAM | UI; can be stopped when not in use |
| Metadata DB (Postgres) | 1 vCPU, 1–2 GB RAM | Stores run history and task state |
| Workers | Minimal | LocalExecutor runs workers inside the scheduler process |

**Total realistic ask: ~3–4 vCPUs, 4–6 GB RAM** as a single VM.

---

## Does Airflow have to be local to the Spark cluster?

No. Airflow only needs network access to:
- **YARN ResourceManager** (port 8032) — to submit Spark jobs
- **Ceph RGW S3 endpoint** — for data read/write and file-sensing

The actual compute happens entirely inside Spark/YARN. Airflow just fires `spark-submit` and watches for completion.

### Deployment options considered

| Option | Pros | Cons |
|---|---|---|
| Remote host (dedicated VM, cloud instance) | Zero impact on cluster resources | Network path to YARN must be open |
| New VM on existing Proxmox node | Stays local, low latency | Consumes ~3–4 vCPUs / 4–6 GB RAM from sizing envelope |
| Co-resident on a YARN VM | No new VM | Competes directly with Spark executors |

**Decision: remote host** — specifically the second Proxmox cluster already running Grafana and Ansible. See Remote Service Host section below.

---

## Is Airflow sufficient for all job submission?

**For production runs: yes.** Airflow submits `spark-submit` to YARN in **cluster mode** (Spark driver runs inside the cluster, close to executors), monitors completion, handles retries, and logs outcomes. Users manage scheduled work entirely through the Airflow UI.

**For development and testing: no.** Developers testing new jobs before they enter a DAG still need:
- `spark-submit` access to YARN (via the remote service host, not the cluster directly)
- Jupyter for interactive development (runs on remote service host in YARN client mode — driver on remote host, executors in cluster)
- YARN UI to watch jobs in progress (via Nginx proxy or SSH tunnel from remote service host)
- Spark History Server for post-job analysis (on remote service host, reads from S3/Ceph RGW)

Developers never need direct access to cluster nodes. All development paths flow through the remote service host.

---

## exaBGP floating IP — effect on remote Airflow placement

The network team proposed a separate interface with a floating IP address announced via exaBGP for the S3/Ceph RGW endpoint.

**This helps remote Airflow placement.** ExaBGP injects a BGP route for the floating IP; whichever node is healthy holds and advertises it. If a node fails, another takes over — transparently to any client.

### How it maps to Airflow's two network paths

| Path | Protocol | Floating IP covers it? |
|---|---|---|
| Read/write data to S3 (Ceph RGW) | HTTP / S3 API | **Yes** — stable address, BGP handles failover |
| Submit Spark jobs to YARN | spark-submit → port 8032 | **No** — YARN RM is a fixed per-node address |

### Question to confirm with network team

Is the floating IP routable from the remote host's network segment, or only announced within the cluster's local routing domain? If local-only, the remote Airflow host needs a VPN/tunnel or an injected route to reach it. Getting a route to YARN RM port 8032 from the same host is a small ask on top of what the team is already doing.

---

## Resilience: Why Airflow must be off-cluster

The question was raised: if Airflow's service VM is on one cluster node and that node goes down, are there sufficient resources on the remaining two nodes?

This revealed two separate resilience concerns with different answers:

### Cluster compute resilience (node failure)
**Yes, degraded but functional.**
- Ceph 3-way replication: data survives a single node loss; MON quorum holds at 2-of-3
- YARN: loses executor VMs on the failed node (~1/3 capacity); in-flight jobs fail and need resubmission, but the cluster continues accepting work

### Orchestration resilience (Airflow on failed node)
**No.** If Airflow is on the failed node, it goes down. Nothing gets scheduled or monitored until the node recovers — exactly when you need it most to detect failures and manage retries.

### Comparison

| | On-cluster (one node) | Off-cluster (remote host) |
|---|---|---|
| Normal operations | Consumes ~3–4 vCPUs / 4–6 GB on one node | No cluster impact |
| Node failure | Airflow goes down with the node | Airflow survives; detects failure, alerts, resubmits |
| Cluster sizing | Complicates calculator math | Cluster resources fully dedicated to Spark |

**Conclusion:** Off-cluster is the only arrangement where orchestration survives a node failure. This drove the decision to place Airflow on the second Proxmox cluster.

---

## Remote Service Host — Decision

A second Proxmox cluster is already in operation running Grafana and Ansible. This becomes the natural home for the remote service host.

**Why this is the right call:**
- Grafana is already running there — cluster monitoring requires no new infrastructure
- Ansible is already there — provisioning, configuration management, and recovery automation in one place
- The second cluster is independently managed — it survives failures on the 3-node Spark cluster completely
- No need to design separate HA for the remote service host — the second Proxmox cluster has its own resilience story

**Services consolidating to the second Proxmox cluster:**

| Service | Status |
|---|---|
| Grafana + Prometheus | Already running |
| Ansible | Already running |
| Airflow | To be added |
| Spark History Server | To be added |
| Jupyter | To be added |
| Nginx reverse proxy | To be added |
| Log aggregation | To be added |

**Failure independence:**

```
3-node Spark cluster fails  →  Remote host unaffected
                               Airflow detects failure
                               Grafana shows cluster went dark
                               Ansible available for recovery

Remote host fails           →  Spark cluster keeps running
                               No new job submissions until host recovers
                               Data safe in Ceph
```
