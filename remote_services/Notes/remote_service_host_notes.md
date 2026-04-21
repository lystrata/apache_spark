# Remote Service Host Architecture
_2026-04-10_

---

## Concept

A remote service host is a machine outside the 3-node Spark cluster that runs management, monitoring, and developer-facing services. This is the classic "edge node" pattern — externalized.

The cluster becomes invisible to developers. They only ever interact with the remote service host, which proxies or submits on their behalf:

```
Developer → Remote Service Host → (proxies/submits to) → Spark Cluster
```

---

## What Must Stay On-Cluster

With all movable services migrated to the remote host, the only components that genuinely cannot leave the cluster are:

| Service | Why |
|---|---|
| YARN ResourceManager | Job submission and cluster coordination — must see NodeManagers over network |
| YARN NodeManagers | Run on every node where executors live — non-negotiable, baked into executor VMs |
| Ceph MON | Quorum-based, 3 required for 3-node cluster |
| Ceph MGR | Active/standby, on-cluster by design |
| Ceph OSD | Tied to physical drives |
| Ceph RGW | Tied to cluster — exaBGP floating IP handles HA story |

Ceph services are already accounted for in the calculator's reservation math. The only dedicated service VM on-cluster is the one running the YARN ResourceManager.

---

## What Moves to the Remote Service Host

| Service | Notes |
|---|---|
| Airflow | Orchestration — submits spark-submit to YARN RM, monitors completion |
| Spark History Server | Reads event logs from S3/Ceph RGW — purely passive, no cluster coupling |
| Prometheus + Grafana | Scrapes cluster metrics — no reason to be on-cluster |
| Jupyter / JupyterHub | Submits to YARN in client mode — driver runs on remote host |
| Log aggregation | Nodes ship logs out — aggregator can be anywhere |
| Nginx reverse proxy | Exposes YARN UI and other cluster UIs to developers |
| Ansible | Configuration management and recovery automation |

---

## How Developer Workflows Are Served Without Direct Cluster Access

| Developer need | How it's served from the remote host |
|---|---|
| Submit a test Spark job | spark-submit runs on remote host (Spark client libraries installed) — developers SSH to remote host, never the cluster |
| Interactive development | JupyterHub on remote host — Spark driver runs there in YARN client mode, executors run in cluster |
| Watch a job in progress | Nginx reverse proxy exposes YARN UI (port 8088) |
| Post-job analysis | Spark History Server reads event logs from S3/Ceph RGW |
| Logs | Centralized log aggregation on remote host |
| Production job scheduling | Airflow UI on remote host |

### YARN client mode vs cluster mode

- **Client mode**: Spark driver runs on the remote host. Good for interactive/development — driver logs are local and visible. Used by Jupyter.
- **Cluster mode**: Spark driver runs inside the cluster. Better for production — driver lives close to executors. Used by Airflow for production submissions.

---

## Nginx Reverse Proxy — Why It's Needed

The YARN UI generates internal links pointing to cluster-private IP addresses. If a developer browses directly to the RM on port 8088, the main page may load but clicking into job details redirects to internal cluster IPs that are unreachable from outside.

Nginx rewrites those URLs on the fly so every link stays on the proxy's address.

**Alternative for small teams:** SSH tunnel achieves the same result without nginx:

```bash
ssh -L 8088:yarn-rm-node:8088 remote-service-host
```

Developer opens `http://localhost:8088` — all links resolve correctly. For a single-user environment this is sufficient and eliminates the need for nginx entirely.

| Approach | Good for |
|---|---|
| SSH tunnel | Single user or small team comfortable with SSH |
| Nginx reverse proxy | Multiple developers, cleaner URL, no per-user tunnel setup |

---

## Network Path — exaBGP Floating IP and Nginx

These operate at different layers and do not conflict.

- **exaBGP** handles routing-level HA for the S3/Ceph RGW endpoint
- **Nginx** proxies application-layer UI traffic (YARN, Airflow, History Server)

Spark executors talk to Ceph RGW directly via the exaBGP floating IP — nginx is never in the S3 data path.

```
Developer browser
      ↓
  Nginx (remote service host)
      ↓                    ↓
YARN RM               Airflow / History Server / Jupyter

Spark executors ─────→ Ceph RGW (exaBGP floating IP)
                        [nginx never touches this path]
```

If YARN RM HA is adopted (Scenario A), the RM floating IP can also be managed via exaBGP — giving nginx a stable upstream address that survives RM failover transparently.

---

## Chosen Deployment — Second Proxmox Cluster

A second Proxmox cluster already runs Grafana and Ansible. This is the designated remote service host.

**Advantages:**
- Grafana already running — monitoring requires no new infrastructure
- Ansible already running — provisioning and recovery automation in place
- Independent management — survives failures on the 3-node Spark cluster
- No separate HA design needed — second cluster has its own resilience story

**Failure independence:**

```
3-node Spark cluster fails  →  Remote host unaffected
                               Airflow detects failure
                               Grafana shows cluster went dark
                               Ansible available for recovery tasks

Remote host fails           →  Spark cluster keeps running
                               No new job submissions until host recovers
                               Data safe in Ceph
                               Manual intervention possible directly on cluster
```
