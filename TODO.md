#  Master TODO — All Contexts
_Last updated 2026-04-24_

---

## PHASE 1 — PRIORITY ITEMS

### P0 — Critical Path (This Week)

- [ ] [Phase1] [correspondence] Confirm cloud staging target — Azure Blob or AWS S3 — for Snowflake COPY INTO path
- [ ] [Phase1] [correspondence] Confirm RHEL 9.4 subscriptions active on all Worker VMs and YARN RM VM
- [ ] [Phase1] [remote_services] Install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME
- [ ] [Phase1] [calculators] Run first 5 production jobs and measure actual shuffle amplification factor (update phases/phase1/deliverables/dev_cluster_phase1_model.html default once measured)

### P1 — Phase 1 Support & Validation

- [ ] [Phase1] [correspondence] Evaluate Phase 1 node addition timeline — 40-job SLA fails without a 4th node
- [ ] [Phase1] [remote_services] Validate WAN egress throughput (1 Gbps ≈ 125 MB/s) is sufficient for Parquet → cloud staging transfer
- [ ] [Phase1] [remote_services] Monitor Ceph OSD memory under peak ingest — increase osd_memory_target if latency spikes
- [ ] [Phase1] [remote_services] Deploy Spark History Server on Node02 (1 vCPU / 4 GB VM — confirmed in Phase 1 report)
- [ ] [Phase1] [remote_services] Deploy YARN ResourceManager HA: active VM on Node01, standby VM on Node03 (vendor requirement)
- [ ] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover
- [ ] [Phase1] [remote_services] Deploy Nginx reverse proxy on remote Airflow host for YARN RM HA stable endpoint
- [ ] [Phase1] [remote_services] Deploy Ansible control node on remote Airflow host

---

## Waiting for Vendor Reply

_(No pending vendor replies)_

---

## Open Questions

- [ ] [remote_services] "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? Scopes Grafana build-out
- [ ] [remote_services] Second Proxmox host specs (vCPU, RAM, storage) — sets VM allocation ceiling
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
_(All configuration items completed - see Completed section)_

**Correspondence & Project Coordination:**
- [ ] [correspondence] Work on Proxmox access method (screen sharing vs. direct) — target completion this week
- [ ] [correspondence] Define required interconnections between remote Airflow server and Spark cluster — coordinate with Sean Klette
- [ ] [correspondence] Review updated resource calculation document from Karthik (pending receipt)
- [ ] [correspondence] Review and provide feedback on dev cluster resource calculations and mappings — see `calculators/Document/dev_cluster_math_reference.html`
- [ ] [correspondence] Confirm directory structure for incoming and archived CSV files (date-based vs. flat)
- [ ] [correspondence] Identify where in the pipeline CSV compression occurs and update mapping logic — see `calculators/Document/etl-data-flow-diagram.html`
- [ ] [correspondence] Resolve authentication approach (Keycloak vs. Okta) with Cyber/Security

**Remote Services Provisioning:**
- [ ] [remote_services] Provision bastion VM on second Proxmox cluster (pending host specs)
- [ ] [remote_services] Provision Grafana + Prometheus VM on monitoring cluster
- [ ] [remote_services] Deploy Airflow (webserver, scheduler, PostgreSQL)
- [ ] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover — 1 ZooKeeper process per node (confirmed 2026-04-23)
- [ ] [Phase1] [remote_services] Deploy Nginx reverse proxy on remote Airflow host — required by YARN RM HA placement for stable endpoint (confirmed 2026-04-23)
- [ ] [Phase1] [remote_services] Deploy Ansible control node on remote Airflow host — install playbooks, configure SSH key + Proxmox API token access (confirmed 2026-04-23)
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

---

## Completed

- [x] [calculators] Review any calculator changes pending in Ready_For_Review/
- [x] [remote_services] Airflow executor type — CeleryExecutor confirmed (Ksolves directory walkthrough 2026-04-22)
- [x] [remote_services] Spark event log location — s3a://spark-history/ confirmed (Ksolves directory walkthrough 2026-04-22)
- [x] [correspondence] Update YARN Node Manager core allocation from 14 to 18 cores
- [x] [correspondence] Confirm 3-OSD storage allocation strategy (OSD utilization max 80%)
- [x] [correspondence] Revisit and confirm JBOD vs. RAID 5 for scratch drives decision
- [x] [correspondence] Confirm Spark version 3.5.3 in production calculator
- [x] [correspondence] Provide answers to Production Cluster Q&A questionnaire
- [x] [correspondence] Confirm JBOD + XFS as final disk strategy for dev
- [x] [calculators] Dev cluster: no hardware RAID — NVMe scratch drives run JBOD; only Proxmox OS SSDs use ZFS
- [x] [calculators] Dev cluster: scratch OSDs formatted with XFS
- [x] [calculators] Update all related HTML files to reflect JBOD/XFS storage decisions
