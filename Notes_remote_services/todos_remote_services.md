# Remote Services — TODO
_Last updated 2026-04-20 16:30_

---

## Open Questions

- [ ] Airflow executor type — LocalExecutor assumed; confirm before deployment
- [ ] "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? Scopes Grafana build-out
- [ ] Second Proxmox host specs (vCPU, RAM, storage) — sets VM allocation ceiling
- [ ] Spark event log location — S3 bucket name or HDFS path; required for History Server config
- [ ] Max concurrent Airflow task slots — drives scheduler RAM and CPU floor
- [ ] Concurrent Jupyter users expected — drives driver memory reservation
- [ ] Ingest batch window timing — validates job concurrency assumptions
- [ ] Is exaBGP floating S3 IP routable from bastion host's network segment?
- [ ] Existing Grafana instance scope — what does it currently monitor?
- [ ] Prometheus — new instance or already running on monitoring cluster?
- [ ] YARN executor VM count per node — refines Prometheus series count and Promtail agent deployment
- [ ] Current Loki VM disk allocation — determines if expansion needed before adding cluster log sources

---

## Pending Tasks

- [ ] Provision bastion VM on second Proxmox cluster (pending host specs)
- [ ] Provision Grafana + Prometheus VM on monitoring cluster
- [ ] Deploy Airflow (webserver, scheduler, PostgreSQL)
- [ ] Deploy Spark History Server
- [ ] Deploy JupyterHub
- [ ] Deploy Nginx reverse proxy
- [ ] Deploy Promtail agent on bastion VM
- [ ] Deploy Promtail agents on 3-node Spark cluster
- [ ] Deploy Promtail agents on monitoring cluster VMs
- [ ] Configure Prometheus scrape targets (node_exporter, pve_exporter, ZFS, YARN JMX, Ceph, Airflow StatsD)
- [ ] Build Grafana dashboards for Proxmox nodes, YARN/Spark, Ceph, bastion services
- [ ] Verify network path: bastion → YARN RM port 8032
- [ ] Verify network path: bastion → Ceph RGW floating IP
- [ ] Verify network path: Promtail → Loki port 3100
- [ ] Add CLAUDE.md entry for remote_services directory structure

---

## Next Session

- Resolve open questions (host specs, executor type, event log location) to finalize VM sizing
- Decide on Grafana dashboard scope ("monitoring Apache" question)
- Begin VM provisioning plan once host specs are known
