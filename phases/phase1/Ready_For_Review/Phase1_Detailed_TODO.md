


# Phase 1–2 Infrastructure Plan — fqdn Development Cluster

_Phases 1–2 detailed plan from fqdn Phase 1 Report (Ksolves) — April 2026_  
_Report Source: phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf_  
_Status: Phase 1 (Planning) COMPLETED Apr 24 · Phase 2 (Implementation) PENDING BLOCKER.1 · Out-of-scope items flagged for vendor clarification_

---

## Document Overview

This document maps the **Ksolves Phase 1 Report (April 2026)** to a detailed, sequenced implementation plan. It addresses the nine Open Items from the Ksolves report and clarifies ambiguous or vague requirements through fqdn-specific research and decision-making.

### Methodology

**Source Mapping:** All nine Ksolves Open Items have been captured in Phase 2A–2C below. Items are categorized by criticality (CRITICAL/HIGH/MEDIUM) and sequenced by dependency.

**Added Clarity:** Where Ksolves used general language or left scope ambiguous, we have:
- **Researched dependencies** (e.g., ZooKeeper as mandatory prerequisite for YARN HA per Apache Hadoop docs)
- **Added fqdn-specific tasks** (e.g., CSV file information gathering, RHEL subscription pre-flight verification, WAN egress validation)
- **Resequenced for feasibility** (e.g., RHEL subscription verification moved to pre-requisite gate, not post-provisioning validation)
- **Clarified ownership** (User actions vs. Ksolves actions, blockers requiring fqdn decision vs. vendor execution)

**Expanded Scope:** Added items that are prerequisites or dependent on Ksolves' work but were implicit in their report:
- P0.0a — CSV file information gathering (needed for Ksolves' storage/shuffle estimates)
- P0.4 (pre-req) — RHEL subscription pre-flight check (gate for P0.1)
- P1.3 — ZooKeeper ensemble (mandatory prerequisite for P1.2 YARN HA per Apache docs)

**Cross-Reference:** All items reference the Ksolves report section or open item number. Assumptions and dependencies are documented in dedicated sections below.

---

## Table of Contents

- [Phase 1 — Planning & Discovery (Completed)](#phase-1-planning-discovery-completed)
- [Phase 2 — Implementation (Pending BLOCKER.1)](#phase-2-implementation-pending-blocker1)
  - [BLOCKER.1 — Establish Ksolves Remote Access](#blocker1-establish-ksolves-remote-access)
  - [BLOCKER.2 — Provision RHEL ISO](#blocker2-provision-rhel-iso)
  - [Phase 2A — Critical Path: VM Provisioning & Foundational Software (P0)](#phase-2a-critical-path-vm-provisioning)
    - [P0.0 — Ceph Cluster Bootstrap (MON, MGR, OSD, RGW)](#p0-0-ceph-cluster-bootstrap)
    - [P0.4 — Verify RHEL Subscriptions (Pre-requisite)](#p0-4-validate-rhel-subscriptions)
    - [P0.0a — Gather CSV File Information](#p0-0a-gather-csv-file-information)
    - [P0.1 — Worker VM Creation & vCPU Allocation](#p0-1-worker-vm-creation)
    - [P0.2 — YARN ResourceManager VM Provisioning](#p0-2-yarn-resourcemanager-vm)
    - [P0.3 — Confirm Cloud Staging Target](#p0-3-confirm-cloud-staging-target)
    - [P0.3b — Validate WAN Egress Throughput](#p0-3b-validate-wan-egress)
    - [P0.4b — Verify RHEL Subscriptions Post-Provisioning](#p0-4-rhel-verification-post-provisioning)
    - [P0.5 — Install Java 11 + Hadoop 3.4.1 (YARN client only, no HDFS)](#p0-5-install-hadoop)
    - [P0.5a — Install Apache Spark 3.5.3](#p0-5a-install-spark)
    - [P0.6 — Run 5 Production Sample Jobs](#p0-6-run-5-production-sample-jobs)
    - [P0.7 — Verify Network Connectivity: MSB-PMC01 ↔ MSB-PMC03](#p0-7-network-connectivity-verification)
  - [Phase 2B — High Priority: Infrastructure Services & HA (P1)](#phase-2b-high-priority-infrastructure-services)
    - [P1.0 — Provision Remote Airflow Server](#p1-0-provision-remote-airflow-host)
    - [P1.1 — Deploy Spark History Server](#p1-1-deploy-spark-history-server)
    - [P1.3 — Deploy ZooKeeper Ensemble](#p1-3-deploy-zookeeper)
    - [P1.2 — Deploy YARN ResourceManager HA](#p1-2-deploy-yarn-ha)
    - [P1.4 — Deploy Nginx Reverse Proxy](#p1-4-deploy-nginx)
    - [P1.5 — Deploy Ansible Control Node](#p1-5-deploy-ansible)
    - [P1.6 — Monitor Ceph OSD Memory](#p1-6-monitor-ceph-osd)
    - [P1.7 — Validate WAN Egress Throughput (Load Test)](#p1-7-validate-wan-egress)
  - [Phase 2C — Medium Priority: Configuration, Validation & Integration (P2)](#phase-2c-medium-priority-configuration-validation)
    - [P2.2 — Deploy Apache Airflow 2.10.4](#p2-2-deploy-apache-airflow)
    - [P2.3 — Validate 8-Stage Data Flow Pipeline](#p2-3-validate-8-stage)
    - [P2.4 — Confirm Compression Codec Configuration](#p2-4-confirm-compression)
    - [P2.5 — Validate JBOD Storage Configuration](#p2-5-validate-jbod)
    - [P2.6 — Validate Network Topology](#p2-6-validate-network)
    - [P2.7 — Evaluate Node Addition Timeline](#p2-7-evaluate-node-addition-timeline)
- [Actions Outside Present Known Scope](#actions-outside-present-known-scope)
- [Assumptions & Dependencies](#assumptions-dependencies)
- [Reference Documents](#reference-documents)
- [Footnotes](#footnotes)

---

<a id="phase-1-planning-discovery-completed"></a>

## PHASE 1 — PLANNING & DISCOVERY (COMPLETED)

Per Ksolves April 24 status report, Phase 1 planning is **COMPLETE**. All discovery, sizing, and architecture work finalized.

### ✅ Phase 1 Deliverables — Completed Apr 24, 2026

- ✅ **Architecture Design & Cluster Topology** — Finalized; 3-node Proxmox, Spark YARN, Ceph RGW, Airflow orchestration
- ✅ **Cluster Sizing & Hardware Recommendations** — Development spec: 3× 32c/384GB RAM, 7× 3.84TB NVMe per node; production spec defined
- ✅ **Storage Architecture Decision** — Ceph RGW (S3-compatible) + XFS on JBOD (no RAID) for NVMe scratch
- ✅ **Technical Walkthroughs** — Ksolves team reviewed all infrastructure requirements and deployment strategy
- ✅ **Phase 1 Completion Report** — Delivered; available at `phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf`
- ✅ **IAM Integration Decision** — **Okta finalized** (not Keycloak); cloud-based auth service
- ✅ **Executor & Concurrency Assumptions** — 8-core executor, 2-job concurrent baseline, 7× shuffle amplification (to be measured)

**Completed Timeline:** Apr 13–24, 2026 (12 days from project start to planning completion)

---

<a id="phase-2-implementation-pending-blocker1"></a>

## PHASE 2 — IMPLEMENTATION (PENDING BLOCKER.1)

All Phase 2 infrastructure provisioning awaits BLOCKER.1 (Proxmox access). Once interim Phase 1A access (Webex) is established, Ksolves can execute all P0–P2 items in sequence.

<a id="blocker1-establish-ksolves-remote-access"></a>

### 🔒 BLOCKER.1 — Establish Ksolves Remote Access to Both Proxmox Clusters

- **Status:** OPEN
- **Priority:** BLOCKING — All Ksolves infrastructure work is waiting on this
- **Context:** Ksolves will be granted owner-level access to both Proxmox clusters (Proxmox One for Service Host, Proxmox Two for Spark Development Cluster). No VMs have been created, no NVMes assigned to Ceph OSDs or Spark scratch. Ksolves requires remote access to begin Phase 1 infrastructure provisioning.

#### Access Strategy (Phased)

**Phase 1A (Interim):** Shared Webex Desktop with fqdn Team Oversight
- Ksolves Karthik Hegde connects to fqdn Webex Desktop shared by fqdn infrastructure team member
- Ksolves executes Proxmox commands / VM provisioning through shared desktop screen
- fqdn team member retains visual oversight of all Ksolves actions (audit trail)
- **Timeline:** Ready immediately; no infrastructure dependencies
- **Duration:** Temporary until secure secondary access ready (estimated 2–4 weeks)

**Phase 1B (Permanent):** VMware Horizon Desktop Access
- Two dedicated VMware Horizon Desktop sessions provisioned for Ksolves team
- Ksolves authenticates to Horizon desktops with fqdn-issued credentials
- Full owner-level Proxmox access via Horizon desktop environment
- **Dependency:** fqdn Horizons Teams infrastructure setup (fqdn Cyber Security approval required)
- **Status:** Blocked pending fqdn Cyber Security Approval of Horizons deployment
- **Timeline:** Estimated 2–4 weeks after security approval

---

- **User Actions Required (Immediate):**
  1. Set up shared Webex Desktop session with Ksolves Karthik Hegde
  2. Create temporary Proxmox root or owner credentials for Ksolves to use during Webex session
  3. Document all Ksolves actions via Webex recording or shared notes for audit trail
  4. Verify Webex connectivity and access permissions before Phase 1 infrastructure work begins

- **User Actions Required (Parallel — does not block interim Webex access):**
  1. Submit fqdn Horizons Teams infrastructure request (if not already submitted)
  2. Obtain fqdn Cyber Security approval for Horizons desktop deployment
  3. Upon approval, provision two Horizon desktop sessions for Ksolves team
  4. Configure Proxmox AAA integration (if desired) or issue owner-level API tokens for Horizon sessions
  5. Migrate Ksolves access from Webex interim to permanent Horizon desktops
  6. Retire temporary Webex session once Horizon is live

- **Verification (Phase 1A — Interim):** 
  - Webex desktop session successfully connects and displays Proxmox web UI
  - Ksolves confirms Proxmox access and can execute administrative commands
  - Webex recording captures all actions (audit trail)

- **Verification (Phase 1B — Permanent):**
  - Horizon desktop sessions authenticate successfully
  - Ksolves confirms owner-level Proxmox access via Horizon
  - Webex session retired; all future access via Horizon

- **Owner:** fqdn infrastructure team (User actions) + fqdn Cyber Security (approval gate for Phase 1B)
- **Estimated Effort:** 
  - Phase 1A setup: 1-2 hours (Webex + temporary credentials)
  - Phase 1B setup: 2-3 hours (Horizon provisioning, post-security-approval)
  - **Critical Path Note:** Phase 1B is non-blocking; Ksolves can begin Phase 1 infrastructure work immediately via Phase 1A (Webex). Phase 1B migration happens in parallel.

---

<a id="blocker2-provision-rhel-iso"></a>

### 🔒 BLOCKER.2 — Provision RHEL ISO to Proxmox Local Storage (User Action)

- **Status:** PENDING P0.0 (CEPH CLUSTER BOOTSTRAP)
- **Priority:** BLOCKING — P0.1 (Worker VM creation) and P0.2 (YARN RM VM creation) cannot proceed without RHEL ISO available
- **Context:** User will place RHEL ISO locally in Proxmox local storage **after** P0.0 (Ceph Cluster Bootstrap) is complete and all 9 OSDs are configured and HEALTH_OK on all three nodes. Ksolves will boot all VMs from this ISO. User performs this action locally while Ksolves team works remotely from India.
- **Dependency:** **Requires P0.0 (Ceph Cluster Bootstrap) completion** — Ksolves must report HEALTH_OK and confirm OSDs ready before user uploads RHEL ISO
- **RHEL Version Decision:**
  - **Current Assumption:** RHEL 9.4 (confirmed compatible with Phase 1 requirements)
  - **Under Research:** RHEL 9.7 (penultimate RHEL9 version) — Ksolves researching Apache Spark 3.5.3 compatibility
  - **Decision Timeline:** Await Ksolves compatibility findings before finalizing ISO selection
  - **Fallback:** If RHEL 9.7 incompatible, proceed with RHEL 9.4
- **User Actions Required:**
  1. **Await notification from Ksolves that P0.0 (Ceph Cluster Bootstrap) is complete and HEALTH_OK** on all three nodes (9 OSDs up/in, MON quorum formed, MGR active, RGW endpoint live)
  2. Once P0.0 confirmed complete, download appropriate RHEL ISO:
     - RHEL 9.4 ISO (if 9.7 deemed incompatible), or
     - RHEL 9.7 ISO (if Ksolves confirms Spark compatibility)
  3. Upload ISO to Proxmox local storage (ISO directory, e.g., `/var/lib/vz/template/iso/`)
  4. Confirm ISO placement with Ksolves before they attempt P0.1 VM creation
- **Verification:**
  - RHEL ISO accessible in Proxmox local storage (`/var/lib/vz/template/iso/` or equivalent)
  - Ksolves confirms ISO visibility and boot accessibility
- **Owner:** User (fqdn) — local provisioning action
- **Estimated Effort:** 1-2 hours (download + upload, depending on ISO size and network bandwidth)
- **Dependency:** Blocks P0.1, P0.2 — Ksolves cannot proceed with VM provisioning without RHEL ISO available

---

<a id="phase-2a-critical-path-vm-provisioning"></a>

### Phase 2A — Critical Path: VM Provisioning & Foundational Software (P0)

<a id="p0-0-ceph-cluster-bootstrap"></a>

### 🔴 P0.0 — Ceph Cluster Bootstrap (MON, MGR, OSD, RGW)

- **Status:** PENDING BLOCKER.1 (KSOLVES ACCESS)
- **Priority:** CRITICAL — Foundation for entire Phase 1 storage layer; gates BLOCKER.2 and all P0.1+ items
- **Context:** Ceph Reef 18.2.x cluster must be bootstrapped on all three Proxmox nodes before any VM provisioning or RHEL ISO placement. The cluster spans MON daemons (Paxos quorum), MGR daemons (active/standby), OSD daemons (one per NVMe drive 1–3 per node, 9 OSDs total), and RGW (S3-compatible endpoint). This is Ksolves' **first work item** after gaining Proxmox access.
- **Prerequisites:**
  - BLOCKER.1 complete (Ksolves has Proxmox access)
  - Proxmox VE 8.3 installed and clustered on all three nodes (assumed pre-existing)
  - Network bonding (2×10G LACP) configured at Proxmox host level
  - NVMe drives 1–3 per node available (3 OSDs/node = 9 OSDs total)
- **Ksolves Actions:**
  1. **Install Ceph Reef 18.2.x packages** on all three Proxmox nodes (via Proxmox PVE Ceph integration or cephadm)
  2. **Bootstrap Ceph cluster** on Node01 with `pveceph init` or `cephadm bootstrap`; configure cluster network on bonded 10G LACP
  3. **Deploy Ceph MON daemons** on all three nodes (Node01, Node02, Node03) — Paxos quorum requires 2-of-3 agreement; verify with `ceph mon stat`
  4. **Deploy Ceph MGR daemons:**
     - Active MGR on Node01
     - Standby MGR on Node02 and Node03
     - Verify with `ceph mgr services`
  5. **Configure Ceph OSDs** (9 total, 3 per node):
     - Allocate NVMe drives 1–3 on each node as OSDs
     - Use BlueStore backend (default for Reef)
     - Set `osd_memory_target=4G` per OSD (per Ksolves Phase 1 spec)
     - Verify with `ceph osd tree` (should show 9 OSDs across 3 hosts, all `up` and `in`)
  6. **Set replication and storage policies:**
     - Pool replication: 3× (size=3, min_size=2)
     - Verify usable capacity: ~11.52 TB after 3× replication + BlueStore overhead
  7. **Deploy Ceph RGW (S3 endpoint):**
     - Install `radosgw` daemon on all three nodes
     - Configure floating IP / load balancer for S3 endpoint stability
     - Allocate 4c / 8GB per RGW instance (per infrastructure reservation)
     - Generate initial S3 access keys (admin)
     - Verify with `radosgw-admin user list`
  8. **Verify cluster health:**
     - `ceph -s` shows HEALTH_OK
     - `ceph osd df` shows balanced data distribution
     - `ceph health detail` shows no warnings
- **Verification:**
  - Ceph cluster status: HEALTH_OK
  - 9 OSDs `up` and `in`, 3× replication confirmed
  - 3 MON daemons in quorum
  - 1 active MGR + 2 standby
  - RGW S3 endpoint accessible (test with `s3cmd` or `aws s3 ls --endpoint-url=<rgw-endpoint>`)
  - Usable capacity: ~11.52 TB available
- **User Sign-Off:** Confirm Ksolves has reported HEALTH_OK and provided S3 endpoint URL/credentials before proceeding to BLOCKER.2 (RHEL ISO placement)
- **Owner:** Ksolves
- **Estimated Effort:** 4-6 hours (cluster bootstrap + OSD allocation + RGW setup + verification)
- **Critical Note:** This task MUST complete before BLOCKER.2 (RHEL ISO upload), P0.1 (Worker VMs), or any subsequent infrastructure work. RGW endpoint must be live for P1.1 (Spark History Server) and P2.3 (8-stage data flow) to function.

---

<a id="p0-4-validate-rhel-subscriptions"></a>

### 🔴 P0.4 — Verify RHEL 9.4 Subscriptions Active (Pre-requisite)

- **Status:** OPEN (USER VERIFICATION)
- **Priority:** CRITICAL — Must be confirmed BEFORE VM provisioning begins
- **Context:** RHEL 9.4 subscriptions must be active on all VMs for yum package installation, security patches, and kernel updates. Confirmation required before Ksolves begins P0.1 VM provisioning so they can proceed immediately with package installation after VM creation.
- **User Actions Required:**
  1. Contact RHEL subscription administrator (or check existing fqdn subscription account)
  2. Verify subscriptions are active for at least 5 RHEL 9.4 licenses (3 Worker VMs + 2 YARN RM VMs)
  3. Confirm subscription status: active through end of Phase 1 + buffer (minimum 6 months)
  4. Document subscription keys or proof of active subscriptions
  5. Share confirmation with Ksolves before they start P0.1
- **Verification:** Subscription administrator confirms active licenses in account portal
- **Owner:** fqdn (subscription management team)
- **Estimated Effort:** < 30 minutes (verification call/check)
- **Critical Note:** This is a gate — P0.1 cannot proceed until subscriptions are confirmed active

---

<a id="p0-0a-gather-csv-file-information"></a>

### 🔴 P0.0a — Gather CSV File Information for Storage & Shuffle Verification

- **Status:** OPEN (USER DATA GATHERING)
- **Priority:** CRITICAL — Required before infrastructure sizing validation
- **Context:** Ksolves needs production CSV file statistics to verify storage allocation and shuffle amplification estimates. This data informs OSD capacity planning and scratch drive sizing decisions. User must analyze local CSV files and provide metrics to Ksolves.
- **User Actions Required:**
  1. Analyze local CSV file inventory:
     - Count total number of CSV files in production source
     - Determine size distribution (breakdown by size ranges: <100MB, 100MB–1GB, 1GB–10GB, 10GB+, etc.)
     - Calculate average file size
  2. Measure compression ratio for production CSV files:
     - Select representative sample of CSV files (10–20 files across size range)
     - Compress samples using ZSTD codec (per Ksolves recommendation)
     - Calculate uncompressed size vs. compressed size ratio (e.g., 4 TB → 1.2 TB = 3.3× compression)
  3. Document and share with Ksolves:
     - Total file count
     - Size distribution table
     - Measured ZSTD compression ratio
     - Any notes on file characteristics that affect compression (data sparsity, cardinality, etc.)
- **Deliverable:** CSV file metrics document or email summary to Ksolves (karthik.hegde@ksolves.com)
- **Owner:** User (fqdn) — local data analysis
- **Estimated Effort:** 2–4 hours (depends on data accessibility and tooling)
- **Impact on Plan:** Informs P0.1 (OSD capacity allocation) and storage headroom decisions. Ksolves will reassess if actual compression differs significantly from 7× shuffle amplification assumption.
- **Critical Note:** Compress samples with ZSTD (standard: `zstd <file>`) to match production pipeline compression strategy

---

<a id="p0-1-worker-vm-creation"></a>

### 🔴 P0.1 — Worker VM Creation & vCPU Allocation (14 → 18)

- **Status:** PENDING REMOTE ACCESS
- **Priority:** CRITICAL — Blocking Phase 1 concurrency baseline
- **Context:** Phase 1 requires 18 vCPU per Worker VM (8-core executor + 4-core driver + 6-core buffer). Current assumptions show 14 vCPU gap. No VMs exist yet; Ksolves will create and configure all three Worker VMs from scratch on Proxmox.
- **Ksolves Actions:**
  1. Provision three RHEL 9.4 VMs on Proxmox: GKPR-SPARK-WK-01 (Node01), GKPR-SPARK-WK-02 (Node02), GKPR-SPARK-WK-03 (Node03)
  2. Allocate 18 vCPU per VM (respect NUMA pinning: 16 vCPU per NUMA domain max)
  3. Allocate 384 GB RAM per VM (from dev cluster infrastructure reservation: 12c/33GB per node leaves 20c/351 GB available)
  4. Attach NVMe drives 4-7 to scratch mount (15.36 TB per node for Spark shuffle)
  5. Configure RHEL network, SSH, and passwordless sudo access
- **Verification:** All three Worker VMs boot successfully; `lscpu` confirms 18 vCPU per VM; `mount | grep /var/spark/scratch` confirms NVMe attachment
- **User Sign-Off:** Confirm Ksolves has provisioned all Worker VMs before proceeding to P0.2
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours

<a id="p0-2-yarn-resourcemanager-vm"></a>

### 🔴 P0.2 — YARN ResourceManager VM Provisioning (Active + Standby) — VM Creation Only

- **Status:** PENDING REMOTE ACCESS, BLOCKER.2 (RHEL ISO)
- **Priority:** CRITICAL — Hardware foundation for YARN HA (deployed in P1.2)
- **Context:** Ksolves will create two RHEL 9.4 VMs that will host the YARN ResourceManager daemons (active/standby). **This task is VM provisioning only** — ZooKeeper deployment is P1.3 and YARN HA configuration is P1.2 (per Apache Hadoop documentation, ZooKeeper must be operational before YARN HA can be configured¹).
- **Ksolves Actions:**
  1. Provision GKPR-YARN-RM-01 VM on Node01 (2 vCPU / 4 GB, RHEL 9.4)
  2. Provision GKPR-YARN-RM-02 VM on Node03 (2 vCPU / 4 GB, RHEL 9.4)
  3. Configure RHEL network, SSH, and passwordless sudo access on both VMs
  4. Verify VMs boot successfully and accept SSH connections
  5. Install Java 11 JDK (`yum install -y java-11-openjdk`) on both VMs (prerequisite for YARN RM daemon)
- **Verification:** Both VMs boot successfully; `lscpu` confirms 2 vCPU and 4 GB RAM; SSH access verified; Java 11 installed
- **User Sign-Off:** Confirm both YARN RM VMs are provisioned and accessible before P1.3 (ZooKeeper) deployment
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (VM provisioning + base RHEL config + Java install)
- **Note:** ZooKeeper installation/configuration → P1.3; YARN ResourceManager daemon install + HA failover → P1.2

<a id="p0-3-confirm-cloud-staging-target"></a>

### 🔴 P0.3 — Confirm Cloud Staging Target (Azure Blob vs AWS S3)

- **Status:** OPEN (VENDOR DECISION)
- **Priority:** CRITICAL — Blocks egress pipeline design (Stage 6)
- **Context:** Phase 1 data flow (Stage 6) transfers Parquet output from Ceph RGW to cloud staging for Snowflake COPY INTO. Cloud platform decision not yet made.
- **Required Decision:** Azure Blob Storage or AWS S3?
- **Impact:** Determines IAM/SAS token configuration, network routing (exaBGP floating IP routing to Snowflake), and Snowflake COPY command syntax. Ksolves will implement credentials and network config once decision is made.
- **Owner:** fqdn data-platform/decision-maker
- **Deadline:** Before Ksolves begins Stage 6 implementation (P2.3, Step 6)

<a id="p0-3b-validate-wan-egress"></a>

### 🔴 P0.3b — Validate WAN Egress Throughput (Ksolves Open Item #3)

- **Status:** OPEN (NETWORK TEAM VERIFICATION)
- **Priority:** HIGH — Required before Stage 6 (Parquet → Cloud Staging) implementation
- **Context:** Phase 1 assumes 1 Gbps WAN egress (≈125 MB/s) is sufficient for inter-batch Parquet transfers to cloud staging. Must validate this throughput is available and sustainable. Per Ksolves: "Parquet output per batch = ~0.8 TB → ~6,400 Gbits → 1.8 hours at 1 Gbps. This must complete within the inter-batch gap."
- **User Actions Required:**
  1. Contact network team to confirm WAN egress capacity available for production cluster
  2. Verify 1 Gbps sustainable throughput (not burst; must handle continuous transfers)
  3. Confirm no rate-limiting or QoS policies that would throttle inter-batch transfers
  4. Document any limitations or constraints (e.g., scheduled maintenance windows, bandwidth sharing with other systems)
  5. Share network validation with Ksolves before P2.3 (Parquet egress implementation)
- **Verification:** Network team confirms 1 Gbps available and sustainable; Ksolves runs test transfer after infrastructure live
- **Owner:** fqdn network team
- **Estimated Effort:** 1-2 hours (network team validation call + documentation)
- **Impact:** If actual WAN egress < 1 Gbps, inter-batch timing increases; affects Phase 1 daily ingest SLA

---

<a id="p0-4-rhel-verification-post-provisioning"></a>

### 🔴 P0.4 — Verify RHEL Subscriptions Post-Provisioning (Ksolves Validation)

- **Status:** PENDING VM PROVISIONING
- **Priority:** CRITICAL — Confirms subscriptions working on actual VMs
- **Context:** After P0.1 VMs are created, Ksolves verifies that subscriptions are properly registered and yum can resolve packages.
- **Ksolves Actions:**
  1. After VM provisioning complete (P0.1), run `subscription-manager list` on all Worker and YARN RM VMs
  2. Verify yum can resolve packages: `yum search java-17-openjdk`
  3. If issues detected, contact fqdn with subscription error details
  4. Apply latest RHEL 9.4 patches: `yum update -y`
- **Verification:** `yum install` succeeds without subscription warnings on all VMs
- **Owner:** Ksolves (with fqdn subscription support)
- **Estimated Effort:** < 1 hour
- **Dependency:** Requires pre-flight confirmation from P0.4 (subscriptions must be active before VM provisioning)

<a id="p0-5-install-hadoop"></a>

### 🔴 P0.5 — Install Java 11 + Hadoop 3.4.1 on All Worker VMs (YARN client libraries only)

- **Status:** PENDING VM PROVISIONING (P0.1)
- **Priority:** CRITICAL — Foundation for Spark 3.5.3 (P0.5a); required for YARN integration
- **Context:** Spark 3.5.3 requires Java JDK + standalone Hadoop installation on each Worker VM. Per Apache Spark documentation,² Hadoop binaries provide the YARN client libraries and Hadoop S3A connector (used to access Ceph RGW). **HDFS is NOT used** — Phase 1 storage is Ceph RGW (S3-compatible), so HDFS daemons are not deployed. Hadoop is installed solely for: (1) YARN client classpath, (2) S3A connector for Ceph RGW. **Java compatibility note:** Apache Hadoop 3.4.1 does not officially support Java 17;² Java 11 is the recommended version (compatible with both Hadoop 3.4.1 and Spark 3.5.3).
- **Ksolves Actions:**
  1. **Install Java 11 JDK** on all three Worker VMs:
     - `yum install -y java-11-openjdk java-11-openjdk-devel`
     - Set `JAVA_HOME=/usr/lib/jvm/java-11-openjdk` in `/etc/environment`
     - Verify: `java -version` shows OpenJDK 11
  2. **Download Hadoop 3.4.1 binary** from Apache mirrors to all three Worker VMs
  3. **Extract** to `/opt/hadoop-3.4.1` on each node
  4. **Set environment variables** in `/etc/environment`:
     - `HADOOP_HOME=/opt/hadoop-3.4.1`
     - `HADOOP_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `YARN_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - Add `$HADOOP_HOME/bin` to PATH
  5. **Configure `core-site.xml`** for S3A (Ceph RGW) connector:
     - `fs.s3a.endpoint=<Ceph RGW endpoint from P0.0>`
     - `fs.s3a.access.key=<from P0.0 RGW credentials>`
     - `fs.s3a.secret.key=<from P0.0 RGW credentials>`
     - `fs.s3a.path.style.access=true` (for Ceph RGW compatibility)
  6. **Configure `yarn-site.xml`** to point to YARN ResourceManager (placeholder — will be updated after P1.2 YARN HA deployment)
  7. **Do NOT start HDFS daemons** (NameNode, DataNode) — HDFS is not used in Phase 1
  8. Verify with `hadoop version` on each node; verify S3A connectivity: `hadoop fs -ls s3a://ingest/`
- **Prerequisites:**
  - P0.1 (Worker VMs provisioned)
  - P0.4b (RHEL subscriptions verified, yum working)
  - P0.0 (Ceph RGW endpoint and S3 credentials available)
- **Verification:**
  - `java -version` shows OpenJDK 11 on all three Worker VMs
  - `hadoop version` returns Hadoop 3.4.1
  - `hadoop classpath` returns non-empty output
  - `hadoop fs -ls s3a://<bucket>/` succeeds (validates S3A → Ceph RGW connectivity)
  - HDFS daemons NOT running (`jps` shows no NameNode/DataNode processes)
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours (Java + Hadoop install + S3A configuration)
- **Critical Note:** This task is the foundation for P0.5a (Spark install); confirm completion before proceeding

<a id="p0-5a-install-spark"></a>

### 🔴 P0.5a — Install Apache Spark 3.5.3 on All Worker VMs

- **Status:** PENDING P0.5 (HADOOP + JAVA) COMPLETION
- **Priority:** CRITICAL — Phase 1 compute engine; required for P0.6 sample jobs and all Spark workloads
- **Context:** Per Apache Spark documentation,² installation order on YARN is: Java → Hadoop/YARN client → Spark binary distribution. Spark 3.5.3 must be installed on each Worker VM as a standalone install (not via Hadoop ecosystem packaging). The "no-hadoop" Spark distribution will be used since Hadoop 3.4.1 is already installed (P0.5) — Spark will use the existing Hadoop classpath. Spark on YARN requires `HADOOP_CONF_DIR` to locate the YARN ResourceManager.
- **Prerequisites:**
  - **P0.5 complete** (Java 11 + Hadoop 3.4.1 installed, `HADOOP_CONF_DIR` set)
  - **P0.0 complete** (Ceph RGW endpoint live for S3A reads/writes)
  - **P1.3 complete** (ZooKeeper) — required for P1.2 YARN HA which Spark connects to
- **Ksolves Actions:**
  1. **Download Spark 3.5.3** ("with-Hadoop-free" build) from Apache mirrors:
     - URL pattern: `https://archive.apache.org/dist/spark/spark-3.5.3/spark-3.5.3-bin-without-hadoop.tgz`
     - Download to all three Worker VMs
  2. **Extract** to `/opt/spark-3.5.3` on each Worker VM
  3. **Set environment variables** in `/etc/environment`:
     - `SPARK_HOME=/opt/spark-3.5.3`
     - Add `$SPARK_HOME/bin` and `$SPARK_HOME/sbin` to PATH
     - Set `SPARK_DIST_CLASSPATH=$(hadoop classpath)` (required for "without-hadoop" build)
  4. **Configure `$SPARK_HOME/conf/spark-defaults.conf`:**
     ```
     spark.master                          yarn
     spark.submit.deployMode               cluster
     spark.executor.cores                  8
     spark.executor.memory                 <calculated from Phase 1 model>
     spark.executor.instances              <calculated>
     spark.driver.cores                    4
     spark.driver.memory                   <calculated>
     spark.local.dir                       /var/spark/scratch
     spark.eventLog.enabled                true
     spark.eventLog.dir                    s3a://spark-history/
     spark.history.fs.logDirectory         s3a://spark-history/
     spark.shuffle.compress                true
     spark.shuffle.spill.compress          true
     spark.io.compression.codec            snappy
     spark.sql.parquet.compression.codec   zstd
     spark.hadoop.fs.s3a.endpoint          <Ceph RGW endpoint from P0.0>
     spark.hadoop.fs.s3a.path.style.access true
     spark.hadoop.fs.s3a.access.key        <from P0.0>
     spark.hadoop.fs.s3a.secret.key        <from P0.0>
     ```
  5. **Configure `$SPARK_HOME/conf/spark-env.sh`:**
     - `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk`
     - `export HADOOP_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `export YARN_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `export SPARK_DIST_CLASSPATH=$(hadoop classpath)`
  6. **Test installation** with a smoke test:
     - `spark-submit --version` reports Spark 3.5.3 with Java 11
     - Run Pi example on YARN: `spark-submit --master yarn --deploy-mode cluster --class org.apache.spark.examples.SparkPi $SPARK_HOME/examples/jars/spark-examples_*.jar 10`
     - Verify YARN RM accepts the job and reports completion
- **Verification:**
  - `spark-submit --version` shows Spark 3.5.3 on all Worker VMs
  - SparkPi example completes successfully on YARN
  - Event log written to `s3a://spark-history/`
  - Spark History Server (P1.1) shows the test job after job completion
- **User Sign-Off:** Confirm SparkPi smoke test succeeds before P0.6 (5 sample production jobs)
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours (download, install, configure, smoke test)
- **Critical Note:** Use the "without-hadoop" Spark distribution to leverage the existing Hadoop 3.4.1 install (avoids version conflicts). Java 11 must be set as `JAVA_HOME` for both Hadoop and Spark.

<a id="p0-6-run-5-production-sample-jobs"></a>

### 🔴 P0.6 — Run 5 Production Sample Jobs (Shuffle Amplification Measurement)

- **Status:** PENDING INFRASTRUCTURE COMPLETION
- **Priority:** CRITICAL — Validates Phase 1 assumptions and updates default calculator values
- **Context:** Phase 1 assumes 7× shuffle amplification; actual measurement needed from real workload. Ksolves will execute 5 sample production jobs at varying sizes (500GB, 1TB, 2TB, 4TB, 5TB) and capture actual shuffle behavior.
- **Ksolves Actions:**
  1. After full infrastructure is live (P0.1–P0.5, P1.2–P1.3), prepare sample CSV datasets (500GB, 1TB, 2TB, 4TB, 5TB)
  2. Submit 5 sequential Spark jobs (one per dataset size) via Airflow DAG or direct spark-submit
  3. For each job, capture:
     - Task shuffle output vs. input ratio (actual amplification factor)
     - Shuffle write bandwidth (MB/s)
     - Ceph RGW throughput ceiling
     - Memory utilization under peak shuffle
     - NVMe scratch I/O patterns
  4. Calculate average amplification factor and update phases/phase1/deliverables/dev_cluster_phase1_model.html default
- **Expected Output:** Actual shuffle amplification factor (e.g., 5.2× instead of assumed 7×) feeds into Phase 1 concurrency SLA
- **Verification:** phases/phase1/deliverables/dev_cluster_phase1_model.html updated with measured value
- **User Sign-Off:** Review measured amplification and confirm it satisfies Phase 1 SLA (40 jobs in 4 hours)
- **Owner:** Ksolves
- **Estimated Effort:** 2-4 hours

<a id="p0-7-network-connectivity-verification"></a>

### 🔴 P0.7 — Verify Network Connectivity: MSB-PMC01 ↔ MSB-PMC03 (Pre-requisite for P1.0)

- **Status:** OPEN (NETWORK TEAM COORDINATION)
- **Priority:** CRITICAL — Gate for Remote Airflow Server provisioning (P1.0)
- **Context:** Remote Airflow server will be provisioned on MSB-PMC01 cluster. Ksolves requires verified network connectivity between MSB-PMC01 and MSB-PMC03 (Spark cluster nodes) with sufficient bandwidth for:
  - Airflow DAG submission to YARN ResourceManager (port 8032, low bandwidth)
  - Spark driver logs and monitoring (continuous, low-moderate bandwidth)
  - Ansible control node → cluster node SSH (key-based, low bandwidth)
  - Nginx reverse proxy → YARN RM HA (port 8088 web UI, low bandwidth)
- **User Actions Required:**
  1. Coordinate with fqdn Network Team to verify/establish network path: MSB-PMC01 ↔ MSB-PMC03
  2. Confirm routing between clusters (same VLAN, or routable via firewall)
  3. Verify firewall rules allow:
     - MSB-PMC01 → MSB-PMC03 nodes (TCP 8032, 8088, 22, 9095 for JMX if monitoring)
     - MSB-PMC03 nodes → MSB-PMC01 (return traffic on same ports)
  4. Test connectivity: ping from MSB-PMC01 to each MSB-PMC03 node; TCP port tests (`nc -zv`)
  5. Document network topology and firewall rules for audit trail
  6. Share verification results with Ksolves before P1.0 provisioning begins
- **Verification:** 
  - Network team confirms connectivity in change ticket
  - Ping response times < 10ms (same datacenter assumed)
  - TCP ports open: `nc -zv <node> 8032`, `nc -zv <node> 8088` succeed on all three MSB-PMC03 nodes
- **Owner:** fqdn Network Team
- **Estimated Effort:** 2-4 hours (coordination + testing + documentation)
- **Critical Note:** This is a hard gate. P1.0 cannot proceed until network connectivity verified and documented.

---

<a id="phase-2b-high-priority-infrastructure-services"></a>

### Phase 2B — High Priority: Infrastructure Services & HA (P1)

<a id="p1-0-provision-remote-airflow-host"></a>

### 🟠 P1.0 — Provision Remote Airflow Server (Ksolves Open Item #8)

- **Status:** PENDING P0.7 NETWORK VERIFICATION (REMOTE INFRASTRUCTURE)
- **Priority:** HIGH — Prerequisite for Airflow orchestration, Ansible automation, and Nginx proxy
- **Context:** Remote Airflow host coordinates ETL job submission to Spark cluster. Must run Airflow webserver/scheduler, Okta SSO integration, Nginx reverse proxy for YARN RM HA, and Ansible control node. Ksolves specifies minimum 6c / 24GB RAM / 500GB SSD. Hosted on MSB-PMC01 cluster.
- **Dependency:** **P0.7 (Network Connectivity) must be completed and verified first** — MSB-PMC01 and MSB-PMC03 clusters must be on same network with confirmed firewall rules.
- **Ksolves Actions:**
  1. After network connectivity verified (P0.7), provision remote server on MSB-PMC01: 6c / 24GB RAM / 500GB SSD, RHEL 9.4
  2. Configure hostname: `airflow-prod-01` (or fqdn-assigned name)
  3. Network setup: routable to all three MSB-PMC03 Spark nodes, to Snowflake, to cloud staging (Azure/AWS)
  4. Install Okta SSO integration (requires OIDC client ID/secret from fqdn Okta tenant)
  5. Verify SSH key access from Ansible control node (to be installed on this host)
  6. Verify network paths: Airflow → YARN RM (port 8032), Airflow → Ceph RGW (floating IP), Airflow → Snowflake
- **User Actions:**
  1. Confirm MSB-PMC01 hosting and IP allocation (coordinate with Network Team)
  2. Provide Okta OIDC credentials for Airflow SSO configuration
  3. Ensure network connectivity verification (P0.7) complete before Ksolves begins provisioning
- **Prerequisites:** 
  - **P0.7 network connectivity verified and documented**
  - Okta SSO client provisioned
  - MSB-PMC01 networking and IP allocation finalized
- **Verification:** SSH to remote host successful; RHEL subscriptions active; network paths confirmed (ping tests to all three cluster nodes <10ms, TCP port tests succeed, Snowflake/cloud routing confirmed)
- **Owner:** Ksolves (provisioning) + fqdn (networking, SSO setup)
- **Estimated Effort:** 2-3 hours (provisioning + network setup)
- **Critical Note:** P1.4 (Nginx), P1.5 (Ansible), and later P2 items depend on this host being live and network-connected

---

### 🟠 P1.1 — Deploy Spark History Server on Node02

- **Status:** PENDING INFRASTRUCTURE (P0.1)
- **Priority:** HIGH — Phase 1 observability and diagnostics
- **Context:** Spark History Server (GKPR-SPARK-HS-01) runs as 1 vCPU / 4 GB VM on Node02. Reads event logs from s3a://spark-history/ on Ceph RGW. Required for Spark job monitoring and debugging during Phase 1 runs.
- **Ksolves Actions:**
  1. Provision Spark History Server VM on Node02 (1c / 4GB, RHEL 9.4)
  2. Install Spark 3.5.3 and configure to read event logs: `spark.history.fs.logDirectory=s3a://spark-history/`
  3. Create S3 bucket on Ceph RGW: s3://spark-history (Ksolves may need Ceph RGW credentials)
  4. Start Spark History Server daemon (port 18080)
- **Prerequisites:** Ceph RGW must be accessible; S3 credentials for spark-history bucket
- **Verification:** Navigate to http://Node02:18080; confirm jobs appear after spark-submit runs
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

### 🟠 P1.3 — Deploy ZooKeeper Ensemble for YARN RM Failover

- **Status:** PENDING P0.0 (CEPH BOOTSTRAP) + P0.1 (WORKER VMs) + P0.2 (YARN RM VMs)
- **Priority:** HIGH — **REQUIRED PREREQUISITE for P1.2** (YARN RM HA cannot be configured until ZooKeeper is operational)
- **Context:** ZooKeeper ensemble — **1 instance per node: Node01, Node02, Node03** (3 instances total) — coordinates YARN ResourceManager failover. Paxos quorum requires 2-of-3 agreement for cluster decisions. Per Apache Hadoop documentation,¹ ZooKeeper must be deployed and running before YARN RM HA configuration begins. Placement (host vs. small VM) to be confirmed with Ksolves; current assumption is host-level deployment on all three Proxmox nodes.
- **Prerequisites:**
  - **Java 11 JDK** installed on each ZooKeeper host (ZooKeeper requires JVM)
  - Network connectivity between all three nodes
  - Firewall ports open: 2181 (client), 2888 (peer), 3888 (leader election)
- **Ksolves Actions:**
  1. Install Java 11 JDK on each ZooKeeper host (if not already from P0.5/P0.2): `yum install -y java-11-openjdk`
  2. Install ZooKeeper 3.8+ on all three nodes (Node01, Node02, Node03) — 1 instance per node
  3. Configure ensemble in `zoo.cfg`: each instance knows about the other two (server.1/2/3 entries pointing to Node01/02/03)
  4. Set unique `myid` file on each node (1, 2, 3 corresponding to Node01, Node02, Node03)
  5. Start ZooKeeper on each node; verify quorum forms: `echo stat | nc localhost 2181`
  6. Verify network connectivity between ZK instances on port 2888 (peer) and 3888 (leader election)
- **Verification:** `echo stat | nc localhost 2181` shows "Mode: leader" or "Mode: follower" on each node; quorum status shows 2-of-3 healthy; one node shows "leader", two show "follower"
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours
- **Critical Note:** Must complete this BEFORE proceeding to P1.2 (YARN HA). Confirm ZK placement (host vs. VM) with Ksolves before installation begins.

### 🟠 P1.2 — Deploy YARN ResourceManager HA (Active/Standby)

- **Status:** PENDING P1.3 COMPLETION (ZooKeeper must be operational first)
- **Priority:** HIGH — Phase 1 stability requirement
- **Context:** YARN ResourceManager runs as VM on Node01 (active) with standby on Node03. Requires ZooKeeper ensemble quorum (1 per node, 3 total) for automatic failover. Per Apache Hadoop documentation,¹ ZooKeeper is a mandatory prerequisite for YARN RM HA. Phase 1 assumes HA for unattended overnight batch runs.
- **Ksolves Actions:**
  1. Install YARN ResourceManager on GKPR-YARN-RM-01 (Node01, active) and GKPR-YARN-RM-02 (Node03, standby)
  2. Configure YARN RM to use ZooKeeper for HA: `yarn.resourcemanager.ha.enabled=true`, `yarn.resourcemanager.zk-address=<zk-quorum>`
  3. Configure ZKRMStateStore (recommended for HA): `yarn.resourcemanager.store.class=org.apache.hadoop.yarn.server.resourcemanager.recovery.ZKRMStateStore`
  4. Set active RM to Node01, standby to Node03 (per vendor requirement)
  5. Test failover: kill active RM process and verify standby takes over automatically
- **Prerequisites:** 
  - **P1.3 (ZooKeeper ensemble) MUST be deployed and operational** (not optional)
  - Network connectivity between all nodes
  - YARN RM VMs (P0.2) must exist
- **Verification:** YARN RM web UI stable at Node01:8088; failover completes in < 30s when active RM is down
- **User Sign-Off:** Confirm YARN RM HA is stable before Phase 1 load tests
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours

### 🟠 P1.4 — Deploy Nginx Reverse Proxy on Remote Airflow Host

- **Status:** PENDING REMOTE AIRFLOW HOST (P2.1)
- **Priority:** HIGH — Provides stable YARN RM endpoint for HA
- **Context:** Nginx acts as reverse proxy for YARN ResourceManager HA, providing stable single endpoint for clients regardless of which node (Node01 or Node03) is currently active. Clients connect to Nginx floating IP; failover is transparent.
- **Ksolves Actions:**
  1. Provision remote Airflow host if not yet done (P2.1)
  2. Install Nginx on remote Airflow host
  3. Configure Nginx upstream to target GKPR-YARN-RM-01 (Node01) and GKPR-YARN-RM-02 (Node03)
  4. Set health checks: active probes to both upstreams every 30s
  5. Configure failover: if Node01 down, route all traffic to Node03 (passive check)
  6. Expose stable endpoints: 
     - http://yarn-rm-proxy:8088 (web UI)
     - http://yarn-rm-proxy:8032 (Spark/Airflow client port)
- **Verification:** Access http://yarn-rm-proxy:8088 and confirm YARN web UI; kill active RM and confirm failover within 30s
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

### 🟠 P1.5 — Deploy Ansible Control Node on Remote Airflow Host

- **Status:** PENDING REMOTE AIRFLOW HOST (P2.1)
- **Priority:** HIGH — Required for infrastructure automation
- **Context:** Ansible control node on remote Airflow host enables programmatic cluster management, configuration updates, and VM lifecycle operations. Must have SSH key access to all cluster nodes and Proxmox API token for VM operations.
- **Ksolves Actions:**
  1. Provision remote Airflow host if not yet done (P2.1)
  2. Install Ansible 2.10+ and Python 3.11+ on remote Airflow host
  3. Generate SSH keypair; distribute public key to all cluster nodes (Node01, Node02, Node03) for passwordless access
  4. Store Proxmox API token securely (recommend pass or dedicated secrets manager)
  5. Clone Ansible playbooks from git repository (if exists) or stage initial plays
  6. Test connectivity: `ansible all -i hosts -m ping` should reach all nodes
- **Prerequisites:** Remote Airflow host provisioned; SSH access to all cluster nodes; Proxmox API token generated
- **Verification:** `ansible -i hosts -m command -a "uname -a" all` returns kernel info from all nodes; Proxmox API token successfully authenticates
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

### 🟠 P1.6 — Monitor Ceph OSD Memory Under Peak Ingest

- **Status:** PENDING METRICS (Grafana, P2.x)
- **Priority:** HIGH — Critical for storage stability
- **Context:** Phase 1 assumes 3 GB per OSD (conservative default osd_memory_target=4GB per Ksolves Phase 1 Report). Must monitor actual memory consumption under peak 4 TB/batch ingest load. If OSD memory exceeds headroom, Ksolves will increase osd_memory_target and re-validate.
- **Ksolves Actions:**
  1. Configure Grafana dashboard for Ceph OSD memory metrics (if Grafana is ready)
  2. During Phase 1 load test (P0.6), capture OSD memory peaks across all ingest cycles
  3. If peak memory > 3.5 GB, incrementally increase osd_memory_target (e.g., 4.5GB → 5GB) and re-test
  4. Document final osd_memory_target value in as-built configuration (P3.2)
- **Success Criteria:** OSD memory stays < 3.5 GB peak during 4 TB batch
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (setup) + data collection during load test

### 🟠 P1.7 — Validate WAN Egress Throughput (1 Gbps Target)

- **Status:** PENDING LOAD TEST (P0.6)
- **Priority:** HIGH — Critical for cloud staging speed
- **Context:** Phase 1 assumes 1 Gbps (≈125 MB/s) outbound throughput from cluster to cloud staging (Azure Blob or AWS S3, TBD at P0.3). Must validate actual achievable throughput with Parquet transfers during Phase 1 load tests.
- **Ksolves Actions:**
  1. During Phase 1 load test (P0.6), measure WAN egress throughput in Stage 6 (cloud egress)
  2. Monitor exaBGP floating IP routing to Snowflake egress point; check for packet loss or latency anomalies
  3. Capture sustained throughput over 5–10 minute transfer window
  4. If sustained < 100 MB/s: diagnose network path (check for QoS limits, jumbo frames, MTU mismatch)
- **Success Criteria:** Sustained ≥100 MB/s during Parquet transfer; 0 packet loss
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (measurement during load test)

---

<a id="phase-2c-medium-priority-configuration-validation"></a>

### Phase 2C — Medium Priority: Configuration, Validation & Integration (P2)

### 🟡 P2.2 — Deploy Apache Airflow 2.10.4 on Remote Host

- **Status:** PENDING REMOTE HOST (P2.1)
- **Priority:** MEDIUM — Phase 1 job orchestration
- **Context:** Airflow triggers spark-submit via DAG scheduler. CeleryExecutor confirmed for distributed job submission to YARN RM. Database can be embedded (docker-compose PostgreSQL) or standalone.
- **Ksolves Actions:**
  1. Install Python 3.11+, pip, and dependencies
  2. Install Apache Airflow 2.10.4: `pip install apache-airflow[celery,postgres]`
  3. Initialize Airflow database: `airflow db init`
  4. Configure CeleryExecutor in airflow.cfg (broker: Redis or RabbitMQ; backend: PostgreSQL)
  5. Create DAG for Phase 1: stage CSV ingest, trigger Spark jobs, track completion
  6. Set up Airflow web UI (default http://host:8080) with basic auth or Okta integration
- **Verification:** Airflow web UI accessible; DAG uploads successfully; manual trigger works
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours

### 🟡 P2.3 — Validate 8-Stage Data Flow Pipeline (CSV → Snowflake)

- **Status:** PENDING FULL INFRASTRUCTURE (P0.1–P0.5, P1.2–P1.3, P2.1–P2.2)
- **Priority:** MEDIUM — End-to-end integration test
- **Context:** Phase 1 data flow spans 8 sequential stages from CSV ingest through Snowflake COPY. Each stage has specific requirements (Airflow DAG, Spark containers, S3A reads/writes, cloud staging). Ksolves will validate the complete pipeline with a sample dataset.
- **Stages to Validate:**
  1. CSV Ingest → Ceph RGW (s3a://ingest/csv/)
  2. Airflow DAG trigger via Airflow scheduler
  3. YARN container scheduling (confirm executors allocated)
  4. Spark ETL execution (CSV → Parquet, Snappy compression on shuffle)
  5. Parquet writes to Ceph RGW (s3a://output/parquet/)
  6. Cloud egress to Azure Blob / AWS S3 (requires cloud staging decision at P0.3)
  7. Snowflake COPY INTO (internal stage → table)
  8. Cleanup gate (delete Parquet from Ceph after Snowflake confirmation)
- **Ksolves Actions:**
  1. Prepare sample CSV dataset (500 GB or 1 TB)
  2. Upload CSV to Ceph ingest bucket: s3a://ingest/csv/
  3. Trigger Airflow DAG manually or via scheduler
  4. Monitor Spark job execution: stages, executors, shuffle behavior
  5. Verify Parquet output in Ceph: s3a://output/parquet/
  6. Test cloud staging egress (once P0.3 decision made)
  7. Verify Snowflake COPY INTO succeeds and data appears in target table
  8. Confirm cleanup removes Parquet after Snowflake confirmation
- **Verification:** End-to-end single job completes successfully; data visible in Snowflake; no data loss in pipeline
- **User Sign-Off:** Review pipeline execution logs and confirm all stages work as expected
- **Owner:** Ksolves
- **Estimated Effort:** 3-4 hours

### 🟡 P2.4 — Confirm Compression Codec Configuration

- **Status:** PENDING SPARK CONFIG
- **Priority:** MEDIUM — Performance and storage optimization
- **Context:** Phase 1 specifies Snappy for shuffle intermediates (2.5× compression, low CPU) and ZSTD for Parquet output (5× compression, higher CPU). Ksolves will validate codec performance during Phase 1 load test (P0.6).
- **Ksolves Actions:**
  1. Configure spark-defaults.conf with compression settings:
     ```
     spark.shuffle.compress=true
     spark.shuffle.spill.compress=true
     spark.io.compression.codec=snappy
     spark.sql.parquet.compression.codec=zstd
     ```
  2. During Phase 1 load test (P0.6), monitor:
     - CPU usage during shuffle phase
     - Actual compression ratio (shuffle output / input)
     - Throughput impact (MB/s with vs. without compression)
  3. If compression overhead > 5% CPU, consider codec swap (e.g., LZ4 for shuffle, ZSTD for output)
- **Verification:** Phase 1 load test meets 4-hour SLA with compression enabled; compression ratios match expectations
- **Owner:** Ksolves
- **Estimated Effort:** < 1 hour (config) + observation during load test

### 🟡 P2.5 — Validate JBOD Storage Configuration (NVMe Drives 4–7, XFS)

- **Status:** PENDING VM PROVISIONING (P0.1)
- **Priority:** MEDIUM — Critical for shuffle performance
- **Context:** NVMe drives 4–7 on each node (15.36 TB per node) are configured as JBOD (not RAID) for Spark shuffle scratch using XFS filesystem. No replication. Ksolves will mount, configure permissions, and benchmark I/O during Phase 1 load test.
- **Ksolves Actions:**
  1. After NVMe drives attached to Worker VMs (P0.1), partition and format drives 4–7 with XFS
  2. Mount to /var/spark/scratch (or per-node equivalent)
  3. Set permissions for Spark process user (root or dedicated spark user): `chmod 1777 /var/spark/scratch`
  4. Configure Spark to use scratch mount: `spark.local.dir=/var/spark/scratch`
  5. During Phase 1 load test (P0.6), benchmark I/O:
     - Run `fio` random read/write test on mounted drives
     - Capture peak I/O throughput (target: ~3,000 MB/s aggregate across cluster)
     - Monitor for I/O bottlenecks or dropped tasks
- **Verification:** `fio` benchmark shows ≥2,500 MB/s random I/O; no I/O errors during Phase 1 load test
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (mount + benchmark)

### 🟡 P2.6 — Validate Network Topology (2×10G LACP Bond)

- **Status:** PENDING INFRASTRUCTURE (P0.1)
- **Priority:** MEDIUM — Ensures cluster bandwidth availability
- **Context:** Each node has 2×10G NICs bonded via LACP (Link Aggregation Control Protocol). Phase 1 requires 20G per node effective bandwidth for intra-cluster replication, S3A reads/writes, and WAN egress. Ksolves will verify bond status and validate throughput during Phase 1 load test.
- **Ksolves Actions:**
  1. After VMs provisioned (P0.1), verify LACP bond status on each node: `cat /proc/net/bonding/bond0` should show "Bonding Mode: balance-alb" and both NICs active
  2. If bond not yet configured, set up LACP on switch and VM network stack
  3. During Phase 1 load test (P0.6), validate throughput:
     - Ceph replication: Should saturate ≥95 MB/s per node (intra-cluster traffic)
     - S3A throughput: Should reach ≥284 MB/s aggregate (Ceph RGW ceiling)
     - WAN egress: Should achieve ≥125 MB/s to cloud (P1.7)
  4. Monitor for packet loss: `ethtool -S bond0 | grep errors` should show 0 after load test
- **Verification:** Bond status shows both NICs active; throughput targets met during load test; 0 packet loss
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (validation during load test)

<a id="p2-7-evaluate-node-addition-timeline"></a>

### 🟡 P2.7 — Evaluate Phase 1 Node Addition Timeline (Ksolves Open Item #9)

- **Status:** PENDING PHASE 1 LOAD TEST RESULTS (P0.6)
- **Priority:** MEDIUM — Critical for Phase 1 → Phase 2 transition planning
- **Context:** Phase 1 report flags 40-job daily SLA as "marginal with 2.1 min buffer" on 3-node cluster. If actual shuffle amplification (P0.6) is higher than assumed 7×, or if concurrent jobs need to exceed 2, a 4th node may be required to hit the SLA reliably. Ksolves will evaluate timing after Phase 1 validation jobs run.
- **Evaluation Criteria:**
  - Actual shuffle amplification factor (measured in P0.6)
  - Concurrent job capability with current 3-node setup
  - If SLA buffer < 5 min for 40 jobs: recommend 4th node addition
  - If SLA buffer ≥ 5 min: proceed with Phase 2 on 3 nodes
- **Ksolves Actions:**
  1. After Phase 1 load test (P0.6) completes, analyze:
     - Actual shuffle amplification vs. 7× assumption
     - Peak memory, CPU, and I/O utilization per node
     - Concurrent job scaling (how many jobs can run simultaneously without SLA breach?)
  2. Calculate revised SLA buffer: (inter-job gap time - job duration) / job duration
  3. If buffer < 5 min: recommend 4th node (same spec: HPE DL385 Gen11, 32c/384GB, 7×3.84TB NVMe)
  4. Provide timeline estimate: can 4th node be provisioned/integrated before Phase 1 production runs?
- **Verification:** Ksolves delivers node addition evaluation report with SLA projections and recommendation
- **Owner:** Ksolves (analysis) + fqdn (decision on 4th node budget/timeline)
- **Estimated Effort:** 2-4 hours (analysis) + 1-2 weeks (procurement/provisioning if approved)
- **Impact on Plan:** If 4th node approved, extends Phase 1 completion by 1-2 weeks; Phase 2 scope does not change

---

<a id="actions-outside-present-known-scope"></a>

## ACTIONS OUTSIDE PRESENT KNOWN SCOPE

The following items are derived from Phase 1 report findings but are not explicitly assigned as Ksolves Phase 1 or Phase 2 responsibilities. Clarification from Ksolves required.

### ❓ Node Addition Timeline & Phase 3 Planning

- **Status:** PENDING KSOLVES CLARIFICATION
- **Context:** Phase 1 report flags 40-job SLA as "marginal with 2.1 min buffer." Phase 2 may require 4+ nodes to support 60+ jobs. Timeline decision: add 4th node before production runs or defer?
- **Options:**
  - Option A: Add 1× HPE DL385 Gen11 node (4 nodes total, relaxes SLA to 5+ min buffer)
  - Option B: Accept Phase 1 2.1 min SLA buffer as acceptable risk
- **Action:** Confirm with Ksolves whether this is Phase 3 scope or fqdn responsibility
- **Owner:** TBD (awaiting Ksolves clarification)

### ❓ Phase 2 As-Built Documentation & Handoff

- **Status:** PENDING KSOLVES CLARIFICATION
- **Context:** After Phase 2 infrastructure is live and validated, create final documentation showing actual configurations, tuning parameters, and lessons learned.
- **Potential Deliverables:**
  - Deployment playbooks and runbooks
  - Known issues, gotchas, and workarounds
  - Recommendations for scaling or Phase 3
- **Action:** Confirm with Ksolves whether this is included in Phase 2 scope or separate engagement
- **Owner:** TBD (awaiting Ksolves clarification)

---

<a id="assumptions-dependencies"></a>

## ASSUMPTIONS & DEPENDENCIES

**Phase 1 Assumptions — FINALIZED (Ksolves Apr 24, 2026):**
- ✅ Cluster topology: 3-node Proxmox (Node01, Node02, Node03)
- ✅ Storage: Ceph RGW (S3) + XFS on JBOD (no RAID on NVMe)
- ✅ Orchestration: Apache Airflow 2.10.4 with CeleryExecutor
- ✅ Authentication: Okta (not Keycloak)
- ✅ Spark version: 3.5.3
- ✅ Hadoop: 3.4.1 standalone

**Phase 2 Assumptions — TO BE VALIDATED:**
- Shuffle amplification: 7× (uncompressed) — actual measurement required (P0.6)
- Concurrent jobs: 1 → 2 baseline (core-bound, not RAM-bound) — to be measured
- WAN egress: 1 Gbps sustained (125 MB/s actual target, P1.7)
- Cloud staging: Azure Blob or AWS S3 (TBD, P0.3 decision required)
- RHEL 9.4: Active subscriptions on all VMs (P0.4)
- No VMs exist yet; all provisioning is Ksolves responsibility
- No NVMes assigned; Ksolves will allocate per spec (3× Ceph OSD, 4× Spark scratch per node)

**External Dependencies:**
- Ksolves technical contact: Karthik Hegde (karthik.hegde@ksolves.com, 8317382875)
- Ksolves requires owner-level Proxmox access (BLOCKER.1) before any infrastructure work
- fqdn sign-off required at user checkpoints (P0.2, P0.6, P1.2, P2.3) before proceeding to next phase
- Cloud staging platform decision (P0.3) blocks Stage 6 pipeline implementation

**Critical Path Sequence:**
- **Phase 1 (Planning):** ✅ COMPLETE — All discovery & architecture finalized (Apr 24)
- **Phase 2 (Implementation):** PENDING
  1. BLOCKER.1: Establish Ksolves remote access (user action — Phase 1A immediate, Phase 1B parallel)
  2. **P0.0: Ksolves bootstraps Ceph cluster** (MON, MGR, 9× OSD, RGW) — first Ksolves work after access granted
  3. BLOCKER.2: User places RHEL ISO in Proxmox local storage (user action — **after** P0.0 HEALTH_OK)
  4. *Parallel user prerequisites:* P0.4 (RHEL subscriptions), P0.0a (CSV file info), P0.7 (network MSB-PMC01↔03)
  5. P0.1–P0.5: Ksolves provisions all VMs and base software (requires RHEL ISO from BLOCKER.2)
  6. **P1.3: Ksolves deploys ZooKeeper ensemble** (required prerequisite for P1.2)
  7. **P1.2: Ksolves deploys YARN HA** (requires P1.3 ZooKeeper to be operational first)
  8. P0.6: Run 5 sample jobs and measure actual shuffle amplification
  9. P1.0, P1.4–P1.5: Ksolves provisions Remote Airflow Server, Nginx reverse proxy, Ansible control
  10. P2.2–P2.3: Ksolves deploys Airflow and validates end-to-end pipeline
  11. Phase 2 sign-off: fqdn approves for production if all P0–P2 items pass
- **Beyond Phase 2:** Pending Ksolves clarification — See "Actions Outside Present Known Scope"

---

<a id="reference-documents"></a>

## REFERENCE DOCUMENTS

- **Main Report:** phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf
- **Prerequisites:** phases/phase1/Incoming/vendor_prerequisites.docx.pdf
- **Hardware Reference:** CLAUDE.md § Hardware Reference
- **Calculator:** phases/phase1/deliverables/dev_cluster_phase1_model.html
- **Ksolves Walkthrough:** phases/phase1/research/ksolves-directory-walkthrough.md
- **Vendor Questions:** phases/phase1/vendor_comms/phase1_vendor_questions.txt

---

<a id="footnotes"></a>

## FOOTNOTES

¹ Apache Software Foundation, "ResourceManager High Availability," in *Apache Hadoop 3.4.1 Documentation*, accessed April 24, 2026, https://hadoop.apache.org/docs/r3.4.1/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html. ZooKeeper is documented as a required prerequisite for YARN ResourceManager High Availability. The documentation explicitly states: "ZooKeeper is a required prerequisite for deploying YARN ResourceManager High Availability" and notes that "The RMs have an option to embed the Zookeeper-based ActiveStandbyElector to decide which RM should be the Active."

² Apache Software Foundation, "Running Spark on YARN," in *Apache Spark Documentation*, accessed April 25, 2026, https://spark.apache.org/docs/latest/running-on-yarn.html. The documentation establishes the prerequisite installation order for Spark on YARN: (1) Java/JDK with `JAVA_HOME` set, (2) Hadoop/YARN cluster operational with ResourceManager running, (3) `HADOOP_CONF_DIR` or `YARN_CONF_DIR` pointing to client-side Hadoop configuration, (4) Spark binary distribution built with YARN support. Java compatibility note: "Apache Hadoop 3.4.1 does not support Java 17, but Spark 4.0.0+ requires Java 17+" — for Spark 3.5.3 + Hadoop 3.4.1, Java 11 is the recommended common version. Confirmed with secondary sources: Cloudera/Hortonworks HDP documentation, "Spark Prerequisites," accessed April 25, 2026, https://docs-archive.cloudera.com/HDPDocuments/HDP3/HDP-3.1.5/installing-spark/content/installing_spark.html, which states "HDFS and YARN deployed on the cluster" as Spark prerequisites.

---

---

_Updated: 2026-04-24 (post-Ksolves Phase 1 completion report)_  
_Phase 1 status reflected per ksolves_april_24_process_report.txt_  
_Prepared for Review: Ready_For_Review/Phase1_Detailed_TODO.md_  
_Status: Draft — Awaiting user review before promotion to Document/_
