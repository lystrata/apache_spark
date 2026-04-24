#  Master TODO — All Contexts

_Last updated 2026-04-24_


## ⭐ PHASE 1 — PRIORITY ITEMS

**P0 — Critical Path (This Week)**

- [ ] [Phase1] [correspondence]  
  Confirm cloud staging target — Azure Blob or AWS S3  
  (for Snowflake COPY INTO path)

- [ ] [Phase1] [correspondence]  
  Confirm RHEL 9.4 subscriptions active  
  (all Worker VMs and YARN RM VM)

- [ ] [Phase1] [remote_services]  
  Install Hadoop 3.4.1 separately on Worker VMs  
  (configure HADOOP_HOME — required before spark-submit)

- [ ] [Phase1] [calculators]  
  Run first 5 production jobs & measure shuffle amplification  
  (update dev_cluster_phase1_model.html default once measured)


**P1 — Phase 1 Support & Validation**

- [ ] [Phase1] [correspondence]  
  Evaluate Phase 1 node addition timeline  
  (40-job SLA fails without 4th node)

- [ ] [Phase1] [remote_services]  
  Validate WAN egress throughput  
  (1 Gbps ≈ 125 MB/s sufficient for Parquet → cloud staging)

- [ ] [Phase1] [remote_services]  
  Monitor Ceph OSD memory under peak ingest  
  (increase osd_memory_target if latency spikes)

- [ ] [Phase1] [remote_services]  
  Deploy Spark History Server on Node02  
  (1 vCPU / 4 GB — confirmed in Phase 1 report)

- [ ] [Phase1] [remote_services]  
  Deploy YARN ResourceManager HA  
  (active on Node01, standby on Node03 — vendor requirement)

- [ ] [Phase1] [remote_services]  
  Deploy ZooKeeper ensemble for YARN RM automatic failover

- [ ] [Phase1] [remote_services]  
  Deploy Nginx reverse proxy on remote Airflow host  
  (provides stable endpoint for YARN RM HA)

- [ ] [Phase1] [remote_services]  
  Deploy Ansible control node on remote Airflow host  
  (install playbooks, SSH + Proxmox API token access)


## Waiting for Vendor Reply

_(No pending vendor replies)_


## Open Questions

- [ ] [remote_services]  
  "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both?  
  (scopes Grafana build-out)

- [ ] [remote_services]  
  Second Proxmox host specs  
  (vCPU, RAM, storage — sets VM allocation ceiling)

- [ ] [remote_services]  
  Max concurrent Airflow task slots  
  (drives scheduler RAM and CPU floor)

- [ ] [remote_services]  
  Concurrent Jupyter users expected  
  (drives driver memory reservation)

- [ ] [remote_services]  
  Ingest batch window timing  
  (validates job concurrency assumptions)

- [ ] [remote_services]  
  Is exaBGP floating S3 IP routable from bastion host's network segment?

- [ ] [remote_services]  
  Existing Grafana instance scope  
  (what does it currently monitor?)

- [ ] [remote_services]  
  Prometheus — new instance or already running on monitoring cluster?

- [ ] [remote_services]  
  YARN executor VM count per node  
  (refines Prometheus series count & Promtail agent deployment)

- [ ] [remote_services]  
  Current Loki VM disk allocation  
  (determines if expansion needed before adding cluster log sources)


## Pending Tasks

### Correspondence & Project Coordination

- [ ] [correspondence]  
  Work on Proxmox access method  
  (screen sharing vs. direct — target completion this week)

- [ ] [correspondence]  
  Define required interconnections between remote Airflow server and Spark cluster  
  (coordinate with Sean Klette)

- [ ] [correspondence]  
  Review updated resource calculation document from Karthik  
  (pending receipt)

- [ ] [correspondence]  
  Review and provide feedback on dev cluster resource calculations  
  (see `calculators/Document/dev_cluster_math_reference.html`)

- [ ] [correspondence]  
  Confirm directory structure for incoming and archived CSV files  
  (date-based vs. flat)

- [ ] [correspondence]  
  Identify where in pipeline CSV compression occurs  
  (update mapping logic — see `calculators/Document/etl-data-flow-diagram.html`)

- [ ] [correspondence]  
  Resolve authentication approach  
  (Keycloak vs. Okta — coordinate with Cyber/Security)


### Remote Services Provisioning

- [ ] [remote_services]  
  Provision bastion VM on second Proxmox cluster  
  (pending host specs)

- [ ] [remote_services]  
  Provision Grafana + Prometheus VM on monitoring cluster

- [ ] [remote_services]  
  Deploy Airflow  
  (webserver, scheduler, PostgreSQL)

- [ ] [Phase1] [remote_services]  
  Deploy ZooKeeper ensemble for YARN RM automatic failover  
  (1 ZooKeeper process per node — confirmed 2026-04-23)

- [ ] [Phase1] [remote_services]  
  Deploy Nginx reverse proxy on remote Airflow host  
  (YARN RM HA stable endpoint — confirmed 2026-04-23)

- [ ] [Phase1] [remote_services]  
  Deploy Ansible control node on remote Airflow host  
  (SSH + Proxmox API token access — confirmed 2026-04-23)

- [ ] [remote_services]  
  Deploy Promtail agents  
  (bastion VM, 3-node Spark cluster, monitoring cluster VMs)

- [ ] [remote_services]  
  Configure Prometheus scrape targets  
  (node_exporter, pve_exporter, ZFS, YARN JMX, Ceph, Airflow StatsD)

- [ ] [remote_services]  
  Build Grafana dashboards  
  (Proxmox nodes, YARN/Spark, Ceph, bastion services)

- [ ] [remote_services]  
  Verify network paths  
  (bastion → YARN RM:8032, bastion → Ceph RGW, Promtail → Loki:3100)

- [ ] [remote_services]  
  Add CLAUDE.md entry for remote_services directory structure


### Security & Compliance

- [ ] [security]  
  Review and promote compliance_frameworks_reference.html  
  (see `security/Ready_For_Review/compliance_frameworks_reference.html`)

- [ ] [security]  
  Define document categories within authentication scope

- [ ] [security]  
  Decide on-site revision control approach  
  (deferred)


## Next Session

- [calculators]  
  Review any pending calculator changes

- [remote_services]  
  Resolve open questions (host specs, event log location)  
  Finalize VM sizing & Grafana dashboard scope

- [security]  
  Promote compliance_frameworks_reference.html after review  
  Define document categories for authentication scope

- [correspondence]  
  Follow up on vendor replies  
  Finalize configuration decisions


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
