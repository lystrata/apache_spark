#  Master TODO — All Contexts
_Last updated 2026-05-01_

---

## PHASE 1 — PRIORITY ITEMS

### BLOCKING — Ksolves Remote Access (Phase 1A re-opened 2026-04-30)

- [x] [Phase1] [correspondence] Establish Ksolves Webex desktop access for Phase 1A interim infrastructure provisioning **(closed 2026-04-29 — Ksolves connecting via Webex)** — **superseded; reopened 2026-04-30 due to Webex Linux/Windows remote-control limitation, see entry below**
  - Phase 1A (interim): Shared Webex desktop with fqdn team oversight — **was active; now blocked**
  - Phase 1B (permanent): VMware Horizon VDI — still pending fqdn Cyber Security approval (tracked under Pending Tasks > Correspondence; non-blocking for Phase 1/2 work)
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.1

- [ ] [Phase1] [correspondence] **Phase 1A re-opened 2026-04-30** — Ksolves must provision Windows host (vendor-side, in India) to run Webex Desktop client with remote control enabled
  - **Cause:** Webex's Linux desktop client does not support remote control of a Windows Webex share (verified by user — set up Linux Webex and confirmed remote-control unavailable). Ksolves is a Linux shop; fqdn shares from Windows. Without a Windows host on Ksolves' side, Phase 1A cannot proceed.
  - **Vendor responsibility:** Ksolves provisions and maintains the Windows host on their side (in India)
  - Vendor sub-tasks:
    - [ ] Ksolves provisions Windows host capable of running Webex Desktop with remote-control support
    - [ ] Ksolves installs and licenses Webex Desktop on the Windows host
    - [ ] Joint connectivity test: Ksolves' Windows host → fqdn-shared Windows Webex session, with remote-control verified
    - [ ] Ksolves notifies fqdn when Windows host is ready, so Phase 1A kickoff can be scheduled
  - **Critical path impact:** All Phase 2 infrastructure provisioning is gated on this until vendor's Windows host is operational. Halt Period decision point (2026-05-04) may need re-evaluation depending on vendor turnaround.
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.1 (Hardware Prerequisite)

### Security — Credential Rotation (URGENT, 2026-05-01)

- [ ] [Phase1] [security] **🚨 Rotate exposed iLO administrator credentials** — the iLO admin password used by Ksolves on `msb-pmc03-01-ilo` (10.1.32.64) appears in plain text inside the vendor's bash history. Rotate the iLO password on all three msb-pmc03 nodes; if the same credential is reused for any corporate-AD account, rotate that as well; scrub `~/.bash_history` on each node (and any vendor workstation copies); coordinate with corporate IT.
  - Source: `phases/phase2/development/Incoming/ksolves_node1_commands.txt` (occurrences at lines 82–87, 121, 138–142, 168–172)

### RHEL ISO Provisioning (CLOSED 2026-04-30)

- [x] [Phase1] [correspondence] Confirm RHEL version: 9.4 (current assumption) vs. 9.7 (pending Ksolves Spark compatibility research) **— resolved 2026-04-30: proceeding with RHEL 9.4 (vendor-requested); 9.7 ISO held on disk for future evaluation but not blocking**
  - Decision: RHEL 9.4 committed for all Phase 1 VM provisioning
  - 9.7 compatibility research with Ksolves is no longer on the critical path
  - See: phases/phase1/development/vendor_comms/phase1_vendor_questions.txt § RHEL Version Decision

- [x] [Phase1] [remote_services] Provision RHEL ISO to Proxmox local storage (user action) **— closed 2026-04-30: ISOs placed on all three dev-cluster nodes via local Directory storage at `/rpool/data/templates/iso/`; decoupled from P0.0 dependency**
  - Resolution path: User added `/rpool/data` as Datacenter → Storage → Directory entry with ISO content type enabled; Proxmox auto-created `templates/iso/` subdirectory; ISOs moved there and visible in Create-VM wizard on all three nodes
  - Versions placed: RHEL 9.4 (committed) + RHEL 9.7 (held)
  - Original blocker (waiting for P0.0 / Ceph HEALTH_OK before placing ISOs) was bypassed by using node-local ZFS storage instead of Ceph-backed shared storage
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.2 (CLOSED)

### P0 — Critical Path (This Week)

- [ ] [Phase1] [correspondence] Gather CSV file information for Ksolves storage/shuffle verification
  - Count total CSV files in production source
  - Measure size distribution (breakdown by size ranges)
  - Test ZSTD compression ratio on representative samples
  - Share metrics with Ksolves before P0.1 VM provisioning
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § P0.0a

- [ ] [Phase1] [correspondence] Confirm cloud staging target — Azure Blob or AWS S3 — for Snowflake COPY INTO path
- [ ] [Phase1] [correspondence] Confirm RHEL 9.4 subscriptions active on all Worker VMs and YARN RM VM
- [ ] [Phase1] [remote_services] Install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME
- [ ] [Phase1] [calculators] Run first 5 production jobs and measure actual shuffle amplification factor (update phases/phase1/development/deliverables/dev_cluster_phase1_model.html default once measured)

- [ ] [Phase1] [remote_services] **Determine max concurrent Airflow task slots** — gates final Airflow host sizing before P1.0 provisioning
  - Currently spec'd at P1.0: 6c / 24 GB / 500 GB SSD on MSB-PMC01 (CeleryExecutor)
  - Concurrency drives: Celery worker count, broker (Redis/RabbitMQ) sizing, scheduler RAM/CPU floor
  - Baseline assumption today: 2 concurrent jobs (per `phases/phase1/development/deliverables/dev_cluster_phase1_model.html`)
  - User action: Confirm peak concurrency with stakeholders (number of DAGs × overlap window) and share with Ksolves before P1.0 begins
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § P1.0

### P1 — Phase 1 Support & Validation

- [ ] [Phase1] [correspondence] Evaluate Phase 1 node addition timeline — 40-job SLA fails without a 4th node
- [ ] [Phase1] [remote_services] Validate WAN egress throughput (1 Gbps ≈ 125 MB/s) is sufficient for Parquet → cloud staging transfer
- [ ] [Phase1] [remote_services] Monitor Ceph OSD memory under peak ingest — increase osd_memory_target if latency spikes
- [ ] [Phase1] [remote_services] Deploy Spark History Server on Node02 (1 vCPU / 4 GB VM — confirmed in Phase 1 report)
- [ ] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover (**REQUIRED PREREQUISITE** — must complete before P1.2)
  - Per Apache Hadoop docs: ZooKeeper is a mandatory prerequisite for YARN RM HA
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § P1.3
- [ ] [Phase1] [remote_services] Deploy YARN ResourceManager HA: active VM on Node01, standby VM on Node03 (vendor requirement)
  - **Depends on P1.3 (ZooKeeper) being operational first**
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § P1.2
- [ ] [Phase1] [remote_services] Deploy Nginx reverse proxy on remote Airflow host for YARN RM HA stable endpoint
- [ ] [Phase1] [remote_services] Deploy Ansible control node on remote Airflow host

---

## Waiting for Vendor Reply

- [ ] [Phase1] RHEL version compatibility: Is Apache Spark 3.5.3 compatible with RHEL 9.7? (Ksolves researching) **— no longer blocking as of 2026-04-30; user committed to RHEL 9.4 for Phase 1**
  - Decision: Proceeding with RHEL 9.4 (vendor-requested, confirmed compatible)
  - 9.7 ISO is on disk at `/rpool/data/templates/iso/` for future use if Ksolves' compatibility research lands favorably
  - Vendor reply still welcome but does not gate any Phase 1 work
  - See: phases/phase1/development/vendor_comms/phase1_vendor_questions.txt § RHEL Version Decision

- [ ] [correspondence] [remote_services] [security] Awaiting Ksolves reply on network, firewall, and DNS access matrix for msb-pmc01 / msb-pmc02 / msb-pmc03 — vendor assumptions and scope (combined ACL matrix: network/firewall + switch VLAN + RGW S3 IAM; dev/prod isolation; Azure egress) — see correspondence/Document/Ksolves Network Firewall DNS Query.md
  - Sent: 2026-04-30
  - Held for separate follow-up after this reply: ExaBGP compatibility — does Ksolves' Spark/RGW client config support a single VIP with ExaBGP failover, or does it hardcode per-node RGW addresses?

- [ ] [Phase1] [correspondence] Revisit YARN HA / ZooKeeper / Nginx decision with Ksolves — vendor appears to have changed their mind
  - 2026-04-27 vendor guidance: single YARN RM VM (no HA), no ZooKeeper, no nginx, manual recovery
  - Earlier guidance (Phase 1 report): active/standby YARN RM pair on Node01 + Node03 with ZooKeeper ensemble and nginx reverse proxy
  - User flagged the reversal as suspicious — confirm which posture is final before proceeding with P0.2 / P1.2 implementation
  - Knock-on effects: RHEL license count (4 vs 5), `dev_cluster_phase1_model.html` resource math, P1.3/P1.4 task scope
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § P0.2, P1.2 (and changelog at phases/phase2/development/Document/Phases_Critical_Path_Development_v1.1_changelog.md)

---

## Open Questions

- [ ] [remote_services] "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? Scopes Grafana build-out
- [ ] [remote_services] Second Proxmox host specs (vCPU, RAM, storage) — sets VM allocation ceiling
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
- [x] [correspondence] Work on Proxmox access method (screen sharing vs. direct) — **resolved 2026-04-29: Webex desktop sharing active for Phase 1A; VDI for Phase 1B**
- [ ] [correspondence] Phase 1B — VMware Horizon VDI provisioning for Ksolves (permanent replacement for Webex sharing; pending fqdn Cyber Security approval; non-blocking for Phase 1/2 work)
- [ ] [correspondence] Decide cluster outbound network path: **MPLS** (single Lumen MPLS cloud) vs. **DIA direct** (multiple Lumen DIA handoffs, paid redundancy) vs. **DIA + VPN** (VPN over DIA, traffic-engineered redundancy) — gates WAN egress throughput validation and cloud staging target choice; cluster confirmed sited at ALG Brooks with redundant ingress from Garfield + Windsor — see `phases/phase2/development/Document/ETL_outbound_map.pdf`
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

## Follow-Ups (from Ksolves msb-pmc03-01 baseline review, 2026-05-01)

- [ ] [Phase1] [security] **Follow-Up:** Verify the `Ksolves-Admins` PVE group ACL was actually downgraded along with the per-user ACLs. The vendor's command history shows the group was granted `Administrator` role at `/`, then `prashant@pam` was set to `PVEAuditor` and `karthik@pam` to `PVEUser` via direct user ACLs — but the group-level grant was not visibly revoked. Run `pveum acl list | grep -i Ksolves-Admins`; if the Administrator entry is still present, remove it (`pveum acl delete / --group Ksolves-Admins --role Administrator`).
  - Source: `phases/phase2/development/Incoming/ksolves_node1_commands.txt` (lines 196–308 group/role setup; lines 385–388 per-user downgrade)

- [ ] [Phase1] [remote_services] **Follow-Up (network team):** msb-pmc03-01 bond0 is degraded — `nic1` is DOWN with LACP `churned` state, no LACP partner. Bond is currently 25 Gbps not 50. User has noted this will be resolved when new cables are run. Schedule with the network team; re-verify with `cat /proc/net/bonding/bond0` once cabling is in place; confirm `-02` and `-03` are similarly cabled (their baseline runs are scheduled today and will reveal their state).
  - Source: `phases/phase2/development/Incoming/ksolves_session_capture.txt` (lines 84–92 ip link, 235–312 bond status)

- [ ] [Phase1] [calculators] **Follow-Up:** Confirm the underlying media class for the 7× 3.5 TiB data drives on each msb-pmc03 node. `nvme list` returned empty on `-01`, and the HPE Smart Array presents all data drives as `LOGICAL VOLUME` (single-disk RAID0 LVs — Smart Array does not support JBOD/passthrough, so individual LVs is the only path to meet the Proxmox JBOD requirement). The CLAUDE.md hardware reference states "7× 3.84 TB NVMe per node"; verify whether the underlying media is actually NVMe or SAS/SATA, and update CLAUDE.md plus `calculators/Document/dev-cluster-storage-reference.html` if the spec was wrong. Throughput math may need revising if SAS.
  - Source: `phases/phase2/development/Incoming/ksolves_session_capture.txt` (lines 16–58 lsblk + nvme list)

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
