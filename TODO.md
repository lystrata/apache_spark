#  Master TODO — All Contexts
_Last updated 2026-04-21_

---

## Waiting for Vendor Reply

- [ ] [remote_services] Q1 — Airflow executor type (LocalExecutor vs CeleryExecutor) — see `remote_services/Notes/questions_for_vendors.txt`

---

## Open Questions

- [x] [calculators] Review any calculator changes pending in Ready_For_Review/
- [ ] [remote_services] Airflow executor type — LocalExecutor assumed; pending vendor reply
- [ ] [remote_services] "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? Scopes Grafana build-out
- [ ] [remote_services] Second Proxmox host specs (vCPU, RAM, storage) — sets VM allocation ceiling
- [ ] [remote_services] Spark event log location — S3 bucket name or HDFS path; required for History Server config
- [ ] [remote_services] Max concurrent Airflow task slots — drives scheduler RAM and CPU floor
- [ ] [remote_services] Concurrent Jupyter users expected — drives driver memory reservation
- [ ] [remote_services] Ingest batch window timing — validates job concurrency assumptions
- [ ] [remote_services] Is exaBGP floating S3 IP routable from bastion host's network segment?
- [ ] [remote_services] Existing Grafana instance scope — what does it currently monitor?
- [ ] [remote_services] Prometheus — new instance or already running on monitoring cluster?
- [ ] [remote_services] YARN executor VM count per node — refines Prometheus series count and Promtail agent deployment
- [ ] [remote_services] Current Loki VM disk allocation — determines if expansion needed before adding cluster log sources

---

## Pending Tasks

**Configuration & Hardware Updates:**
- [x] [correspondence] Update YARN Node Manager core allocation from 14 to 18 cores
- [x] [correspondence] Confirm 3-OSD storage allocation strategy (OSD utilization max 80%) — see `calculators/Document/dev-cluster-storage-reference.html`
- [x] [correspondence] Revisit and confirm JBOD vs. RAID 5 for scratch drives decision — see `calculators/Document/dev-cluster-storage-reference.html`
- [x] [correspondence] Confirm Spark version 3.5.3 in production calculator
- [ ] [calculators] Dev cluster: no hardware RAID — NVMe scratch drives run JBOD; only Proxmox OS SSDs use ZFS — see `calculators/Document/dev-cluster-storage-reference.html`
- [ ] [calculators] Dev cluster: scratch OSDs formatted with XFS — see `calculators/Document/dev-cluster-storage-reference.html`
- [ ] [calculators] Update all related dev HTML files to reflect JBOD/XFS storage decisions (dev-cluster-storage-reference.html, dev_cluster_math_reference.html, development_spark_calculator.html, dev_slider_guide.html)

**Correspondence & Project Coordination:**
- [ ] [correspondence] Work on Proxmox access method (screen sharing vs. direct) — target completion this week
- [ ] [correspondence] Define required interconnections between remote Airflow server and Spark cluster — coordinate with Sean Klette
- [ ] [correspondence] Review updated resource calculation document from Karthik (pending receipt)
- [x] [correspondence] Provide answers to Production Cluster Q&A questionnaire — address data sizing, SLA, ingestion rate, transformation complexity, and cluster constraints — see `calculators/Document/production_spark_calculator.html`
- [ ] [correspondence] Review and provide feedback on dev cluster resource calculations and mappings — see `calculators/Document/dev_cluster_math_reference.html`
- [x] [correspondence] Confirm JBOD + XFS as final disk strategy for dev — see `calculators/Document/dev-cluster-storage-reference.html`
- [ ] [correspondence] Confirm directory structure for incoming and archived CSV files (date-based vs. flat)
- [ ] [correspondence] Identify where in the pipeline CSV compression occurs and update mapping logic — see `calculators/Document/etl-data-flow-diagram.html`
- [ ] [correspondence] Resolve authentication approach (Keycloak vs. Okta) with Cyber/Security

**Remote Services Provisioning:**
- [ ] [remote_services] Provision bastion VM on second Proxmox cluster (pending host specs)
- [ ] [remote_services] Provision Grafana + Prometheus VM on monitoring cluster
- [ ] [remote_services] Deploy Airflow (webserver, scheduler, PostgreSQL)
- [ ] [remote_services] Deploy Spark History Server
- [ ] [remote_services] Deploy Nginx reverse proxy
- [ ] [remote_services] Deploy Promtail agent on bastion VM
- [ ] [remote_services] Deploy Promtail agents on 3-node Spark cluster
- [ ] [remote_services] Deploy Promtail agents on monitoring cluster VMs
- [ ] [remote_services] Configure Prometheus scrape targets (node_exporter, pve_exporter, ZFS, YARN JMX, Ceph, Airflow StatsD)
- [ ] [remote_services] Build Grafana dashboards for Proxmox nodes, YARN/Spark, Ceph, bastion services
- [ ] [remote_services] Verify network path: bastion → YARN RM port 8032
- [ ] [remote_services] Verify network path: bastion → Ceph RGW floating IP
- [ ] [remote_services] Verify network path: Promtail → Loki port 3100
- [ ] [remote_services] Add CLAUDE.md entry for remote_services directory structure

**Security & Compliance:**
- [ ] [security] Review and promote security/Ready_For_Review/compliance_frameworks_reference.html → security/Document/
- [ ] [security] Define document categories within authentication scope
- [ ] [security] Decide on-site revision control approach (deferred)

---

## Next Session

- [calculators] Review any pending calculator changes
- [remote_services] Resolve open questions (host specs, executor type, event log location) to finalize VM sizing; decide on Grafana dashboard scope
- [security] Promote compliance_frameworks_reference.html after review; define document categories for authentication scope — see `security/Ready_For_Review/compliance_frameworks_reference.html`
- [correspondence] Follow up on vendor replies and finalize configuration decisions
