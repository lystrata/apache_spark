#  Master TODO — All Contexts
_Last updated 2026-05-05_

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

### Vendor Configuration Baseline — Ksolves Spark & YARN Config v1.0 (2026-05-04)

Ksolves delivered an authoritative configuration document on 2026-05-04 (`phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf`) based on actual DEV environment data (`csv_file_sizes.xlsx`). It establishes the Spark 3.5.3 / YARN 3.4.1 config baseline, answers prior P0.0a items, and surfaces several new decisions.

**Decisions captured 2026-05-05:**

- **Cluster size — finalized at 3 nodes.** Vendor recommended +1 node for 2-concurrent-job operation; user decided 3 nodes only (budget constraint). The vendor's "feasible-but-zero-buffer" SLA analysis at 3 nodes is the accepted posture.
- **GZIP non-splittability mitigation** — owner: **Development team**. Choose 1 of 4 options from § 2: pre-split upstream (best) / bzip2 codec / raw uncompressed CSV / post-read repartition (last resort).
- **Hadoop 3.4.1 vs Spark 3.5.x classpath** — owner: **Vendor (Ksolves)** (they're doing the install). Captured for tracking only; no fqdn-side action.
- **Ceph RGW server-side tuning** (`rgw_thread_pool_size 512`, `rgw_max_concurrent_requests 1024`) — owner: **Vendor (Ksolves)** until cluster sign-over. Captured for tracking only.
- **HIPAA compliance** — forked into a separate sub-project: `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` (forthcoming). Main Critical Path gains a BLOCKER pointing to it. **NVMe disks are already LUKS-encrypted on this side** — must remind Ksolves before they start Spark install so they don't redo it.
- **RAM hardware update** — RAM/node spec'd at **320 GB** (was 384). CLAUDE.md hardware reference updated; calculator defaults to follow.

**New tasks (open):**

- [ ] [Phase1] [correspondence] **GZIP mitigation strategy decision** — Development team picks the upstream/codec/raw/repartition option. Vendor recommends pre-split upstream as the zero-SLA-risk path. See `Ksolves_Spark_YARN_Config_v1.0.pdf` § 2.
- [ ] [Phase1] [correspondence] **Notify Ksolves — NVMe disks already LUKS-encrypted** — vendor's HIPAA guide (§ 8.2) recommends LUKS on NVMe drives 4–7. They are already encrypted. Communicate before Spark install so they don't reformat.
- [ ] [correspondence] **SOW Change Order coordination** — capture HIPAA scope addition + 3-node decision (no additional node) + vendor configuration guide rollover. Coordinate with Mirali.
- [ ] [calculators] **Update calculator defaults** — RAM/node 384 → 320 GB; daily ingest default 5 TB → ≤1.5 TB (per vendor's actual DEV data); embed repartition formula `target_partitions = max(24, ceil(compressed_csv_mb / 50))`; add `spark.sql.shuffle.partitions = 4096` to reference docs.
- [ ] [Phase1] **Bump Phases_Critical_Path_Development to v1.4** — incorporate vendor config baseline, GZIP P0, Hadoop classpath / Ceph RGW tuning as vendor-owned tasks, HIPAA BLOCKER pointing to sub-project, 3-node decision finalization. _(In progress — see batch 2.)_

**Cross-references:**
- `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` — the vendor doc itself
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.4.md` — main CP (forthcoming)
- `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` — HIPAA sub-project (forthcoming)

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

- [x] [Phase1] [correspondence] **Gather CSV file information for Ksolves storage/shuffle verification** — **Closed 2026-05-05**: vendor delivered the analysis themselves in `Ksolves_Spark_YARN_Config_v1.0.pdf` (2026-05-04), based on `csv_file_sizes.xlsx`. Numbers: 800 tables / 359 with data / 12,214 files / 1.52 TB compressed / 2 multi-file tables (5,800 files each) / top 12 tables = 79.29% of volume.

- [x] [Phase1] [correspondence] Confirm cloud staging target — Azure Blob or AWS S3 — for Snowflake COPY INTO path. **Closed 2026-05-05: Azure Blob confirmed**. Pipeline: `Airflow DAG → spark-submit per table → Ceph → Parquet → Snowflake COPY INTO from Azure` (per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1).
- [ ] [Phase1] [correspondence] Confirm RHEL 9.4 subscriptions active on all Worker VMs and YARN RM VM
- [ ] [Phase1] [remote_services] Install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME — **Owner: Vendor (Ksolves)**. Note for vendor: Spark 3.5.x ships with Hadoop 3.3.x; install must set `HADOOP_HOME` → 3.4.1 + `spark.yarn.populateHadoopClasspath = true` per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 3.4 deployment note.
- [ ] [Phase1] [calculators] Run first 5 production jobs and measure actual shuffle amplification factor (update phases/phase1/development/deliverables/dev_cluster_phase1_model.html default once measured)

- [x] [Phase1] [remote_services] **Determine max concurrent Airflow task slots** — **Closed 2026-05-05: 1 concurrent job** (3-node cluster final). Vendor recommended +1 node for 2-concurrent operation but user decided 3 nodes only (budget). Per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.2: "The cluster supports 1 concurrent Spark job with the current 3-node configuration." Airflow host sizing at P1.0 (6c / 24 GB / 500 GB SSD) remains valid for single-job orchestration.

### P1 — Phase 1 Support & Validation

- [x] [Phase1] [correspondence] Evaluate Phase 1 node addition timeline — 40-job SLA fails without a 4th node. **Closed 2026-05-05: NOT adding a 4th node (budget constraint)**. Vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.3 confirms 3-node operation is feasible-but-zero-buffer at the 4-hour SLA. Mitigations: schedule top 12 largest tables first (79.29% of volume); add Airflow size-check gate to skip the 184 placeholder tables.
- [ ] [Phase1] [remote_services] Validate WAN egress throughput (1 Gbps ≈ 125 MB/s) is sufficient for Parquet → cloud staging transfer
- [ ] [Phase1] [remote_services] Monitor Ceph OSD memory under peak ingest — increase osd_memory_target if latency spikes
- [ ] [Phase1] [remote_services] Deploy Spark History Server on Node02 (1 vCPU / 4 GB VM — confirmed in Phase 1 report)
- [x] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover. **Closed 2026-05-05**: scope dropped — single YARN RM final (no HA → no ZooKeeper). See Vendor Configuration Baseline above + v1.3 P1.3 removal.
- [x] [Phase1] [remote_services] Deploy YARN ResourceManager HA: active VM on Node01, standby VM on Node03. **Closed 2026-05-05**: scope dropped — single YARN RM final (3-node decision; no 4th node available for HA pair). See Vendor Configuration Baseline above.
- [x] [Phase1] [remote_services] Deploy Nginx reverse proxy on remote Airflow host for YARN RM HA stable endpoint. **Closed 2026-05-05**: scope dropped — no HA → no need for stable endpoint. See Vendor Configuration Baseline above + v1.3 P1.4 removal.
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

- [x] [Phase1] [correspondence] Revisit YARN HA / ZooKeeper / Nginx decision with Ksolves. **Closed 2026-05-05**: vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 4 implicitly confirms single-RM posture (no HA settings in `yarn-site.xml`). Single YARN RM VM is final. The 3-node decision (no 4th node) further validates: there is no 4th node available for active/standby pair anyway. ZooKeeper / Nginx scope already dropped from v1.3.

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
- [x] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover — **Closed 2026-05-05**: dropped (single YARN RM, no HA). Duplicate of P1 entry above; see Vendor Configuration Baseline.
- [x] [Phase1] [remote_services] Deploy Nginx reverse proxy on remote Airflow host — **Closed 2026-05-05**: dropped (no HA). Duplicate of P1 entry above.
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
