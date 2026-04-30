


# Phases Critical Path — fqdn Development Cluster

_Version 1.3 · Last updated 2026-04-30_  
_Phases 1–2 detailed plan from fqdn Phase 1 Report (Ksolves) — April 2026_  
_Report Source: phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf_  
_Status: Phase 1 (Planning) COMPLETED Apr 24 · Phase 2 (Implementation) PENDING BLOCKER.1 (re-opened 2026-04-30 — see Phase 1A hardware prerequisite) · Out-of-scope items flagged for vendor clarification_

---

## Document Overview

This document maps the **Ksolves Phase 1 Report (April 2026)** to a detailed, sequenced implementation plan. It addresses the nine Open Items from the Ksolves report and clarifies ambiguous or vague requirements through fqdn-specific research and decision-making.

### Methodology

**Source Mapping:** All nine Ksolves Open Items have been captured in Phase 2A–2C below. Items are categorized by criticality (CRITICAL/HIGH/MEDIUM) and sequenced by dependency.

**Added Clarity:** Where Ksolves used general language or left scope ambiguous, we have:
- **Added fqdn-specific tasks** (e.g., CSV file information gathering, RHEL subscription pre-flight verification, WAN egress validation)
- **Resequenced for feasibility** (e.g., RHEL subscription verification moved to pre-requisite gate, not post-provisioning validation)
- **Clarified ownership** (User actions vs. Ksolves actions, blockers requiring fqdn decision vs. vendor execution)

**Expanded Scope:** Added items that are prerequisites or dependent on Ksolves' work but were implicit in their report:
- P0.0a — CSV file information gathering (needed for Ksolves' storage/shuffle estimates)
- P0.4 (pre-req) — RHEL subscription pre-flight check (gate for P0.1)

**Cross-Reference:** All items reference the Ksolves report section or open item number. Assumptions and dependencies are documented in dedicated sections below.

---

## Schedule & SOW Status

_Companion tracker: `phases/phase2/development/Document/SOW_timeline_status.md` (full week calendar and SOW phase mapping)._

**Project start (per agreement):** 2026-04-14 · **SOW indicative completion:** 2026-07-06 (12 weeks, no Halt Period) · **Source:** Ksolves SOW V1.0 (March 16, 2026) § 5 Indicative Timelines.

**As of 2026-04-27 — mid-Week 2:**

- **Phase 1 (Discovery & Setup Planning, 1 wk):** Completed 2026-04-24 — about 4 days past the SOW Week-1 boundary. Essentially on plan given the 1-week budget.
- **Phase 2 (Proxmox & VM Creation, 3 wks, window 2026-04-21 → 2026-05-11):** In window, **not yet started**. Each week BLOCKER.1 (Ksolves remote access) stays open consumes ~1/3 of the Phase 2 budget.
- **Halt Period decision point: 2026-05-04** (end of SOW Week 3). If BLOCKER.1 has not closed by this date, fqdn should consider formally invoking SOW § 7.2 (Halt Period) so the gated duration is excised from the schedule, milestones, and SLA. Whether to invoke is a contracting decision per SOW § 9.2 (Project Change Control).
- **SOW V1.1 pending:** the 2026-04-27 verbal vendor reversal (single YARN RM, no ZooKeeper, no nginx — captured in P0.2, P1.2, and the dropped P1.3/P1.4) is **not yet reflected** in a written SOW revision. The SOW Document History table is still blank past V1.0; § 9 requires a written, signed change order for material scope changes. Tracked under `TODO.md § Waiting for Vendor Reply`.
- **Out-of-scope reminder:** SOW § 2.2 excludes "user load or performance testing" — P1.8 (5 production sample jobs / shuffle amplification measurement) likely needs a Change Order or separate SOW.

---

<a id="phase-1-planning-discovery-completed"></a>

## PHASE 1 — PLANNING & DISCOVERY (COMPLETED)

Per Ksolves April 24 status report, Phase 1 planning is **COMPLETE**. All discovery, sizing, and architecture work finalized.

### ✅ Phase 1 Deliverables — Completed Apr 24, 2026

- ✅ **Architecture Design & Cluster Topology** — Finalized; 3-node Proxmox, Spark YARN, Ceph RGW, Airflow orchestration
- ✅ **Cluster Sizing & Hardware Recommendations** — Development spec: 3× 32c/384GB RAM, 7× 3.84TB NVMe per node; production spec defined
- ✅ **Storage Architecture Decision** — Ceph RGW (S3-compatible) + XFS on JBOD (no RAID) for NVMe scratch
- ✅ **Technical Walkthroughs** — Ksolves team reviewed all infrastructure requirements and deployment strategy
- ✅ **Phase 1 Completion Report** — Delivered; available at `phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf`
- ✅ **IAM Integration Decision** — **Okta finalized** (not Keycloak); cloud-based auth service
- ✅ **Executor & Concurrency Assumptions** — 8-core executor, 2-job concurrent baseline, 7× shuffle amplification (to be measured)

**Completed Timeline:** Apr 13–24, 2026 (12 days from project start to planning completion)

---

<a id="phase-2-implementation-pending-blocker1"></a>

## PHASE 2 — IMPLEMENTATION (PENDING BLOCKER.1)

All Phase 2 infrastructure provisioning awaits BLOCKER.1 (Proxmox access). Once interim Phase 1A access (Webex) is established, Ksolves can execute all P0–P2 items in sequence.

<a id="blocker1-establish-ksolves-remote-access"></a>

### 🔒 BLOCKER.1 — Establish Ksolves Remote Access to Both Proxmox Clusters

- **Status:** OPEN — re-opened 2026-04-30 due to newly identified Phase 1A hardware prerequisite (see below)
- **Priority:** BLOCKING — All Ksolves infrastructure work is waiting on this
- **Context:** Ksolves will be granted owner-level access to both Proxmox clusters (Proxmox One for Service Host, Proxmox Two for Spark Development Cluster). No VMs have been created, no NVMes assigned to Ceph OSDs or Spark scratch. Ksolves requires remote access to begin Phase 1 infrastructure provisioning.

Two-stage access strategy: an interim Webex desktop arrangement followed by a permanent VMware Horizon VDI deployment.

<a id="blocker1-phase-1a-interim-webex"></a>

#### Phase 1A — Interim: Shared Webex Desktop with fqdn Team Oversight

- Ksolves Karthik Hegde connects to fqdn Webex Desktop shared by fqdn infrastructure team member
- Ksolves executes Proxmox commands / VM provisioning through shared desktop screen
- fqdn team member retains visual oversight of all Ksolves actions (audit trail)
- **Timeline:** Pending Ksolves Windows host provisioning (see hardware prerequisite below)
- **Duration:** Temporary until secure secondary access ready (estimated 2–4 weeks)

> **🪟 Hardware Prerequisite (Vendor Action — added 2026-04-30):** Webex's Linux desktop client does **not support remote control** of a Windows Webex share (or vice-versa). Ksolves is a Linux shop; fqdn is primarily a Windows shop and shares from a Windows host. Cross-platform remote control is not implemented in Webex's Linux client (verified by user — set up Linux Webex and confirmed remote-control unavailable). **Ksolves must provision a Windows host on their side** (in India) to run the Webex Desktop client and accept remote-control of fqdn's shared Windows session. Without this Windows host, Phase 1A cannot proceed and Ksolves cannot drive Proxmox provisioning through the shared session. This is a Ksolves-side responsibility (vendor provisions, vendor maintains).

<a id="blocker1-phase-1b-permanent-horizon"></a>

#### Phase 1B — Permanent: VMware Horizon Desktop Access

- Two dedicated VMware Horizon Desktop sessions provisioned for Ksolves team
- Ksolves authenticates to Horizon desktops with fqdn-issued credentials
- Full owner-level Proxmox access via Horizon desktop environment
- **Dependency:** fqdn Horizons Teams infrastructure setup (fqdn Cyber Security approval required)
- **Status:** Blocked pending fqdn Cyber Security Approval of Horizons deployment
- **Timeline:** Estimated 2–4 weeks after security approval

---

- **Vendor Actions Required (Hardware Prerequisite — Phase 1A gating, added 2026-04-30):**
  - [ ] Ksolves provisions a Windows host (in India) capable of running the Webex Desktop client with remote-control support
  - [ ] Ksolves installs and licenses Webex Desktop on the Windows host
  - [ ] Ksolves confirms Webex remote-control connectivity from their Windows host into a fqdn-shared Windows Webex session (joint test with fqdn infrastructure team)
  - [ ] Ksolves notifies fqdn when the Windows host is ready, so fqdn can schedule the Phase 1A kickoff session

- **User Actions Required (Immediate — pending vendor hardware prerequisite):**
  - [ ] Set up shared Webex Desktop session (from fqdn Windows host) with Ksolves Karthik Hegde once vendor's Windows host is ready
  - [ ] Create temporary Proxmox root or owner credentials for Ksolves to use during Webex session
  - [ ] Document all Ksolves actions via Webex recording or shared notes for audit trail
  - [ ] Verify Webex connectivity and remote-control permissions before Phase 1 infrastructure work begins

- **User Actions Required (Parallel — does not block interim Webex access):**
  - [ ] Submit fqdn Horizons Teams infrastructure request (if not already submitted)
  - [ ] Obtain fqdn Cyber Security approval for Horizons desktop deployment
  - [ ] Upon approval, provision two Horizon desktop sessions for Ksolves team
  - [ ] Configure Proxmox AAA integration (if desired) or issue owner-level API tokens for Horizon sessions
  - [ ] Migrate Ksolves access from Webex interim to permanent Horizon desktops
  - [ ] Retire temporary Webex session once Horizon is live

- **Verification (Phase 1A — Interim):** 
  - [ ] Ksolves' Windows host runs Webex Desktop and connects to a fqdn-hosted Windows Webex session
  - [ ] Remote control from Ksolves' Windows host into fqdn's shared Windows desktop is functional (verified via test session)
  - [ ] Webex desktop session successfully displays Proxmox web UI
  - [ ] Ksolves confirms Proxmox access and can execute administrative commands via remote control
  - [ ] Webex recording captures all actions (audit trail)

- **Verification (Phase 1B — Permanent):**
  - [ ] Horizon desktop sessions authenticate successfully
  - [ ] Ksolves confirms owner-level Proxmox access via Horizon
  - [ ] Webex session retired; all future access via Horizon

- **Owner:** Ksolves (Windows host hardware prerequisite) + fqdn infrastructure team (User actions) + fqdn Cyber Security (approval gate for Phase 1B)
- **Estimated Effort:** 
  - Vendor Windows host provisioning: Ksolves estimate (added 2026-04-30; previously not in scope)
  - Phase 1A setup (post-vendor-prereq): 1-2 hours (Webex + temporary credentials)
  - Phase 1B setup: 2-3 hours (Horizon provisioning, post-security-approval)
  - **Critical Path Note:** Phase 1A is now gated on vendor's Windows host provisioning. Phase 1B remains non-blocking; both can progress in parallel once Phase 1A is unblocked.

---

<a id="blocker2-provision-rhel-iso"></a>

### ✅ BLOCKER.2 — Provision RHEL ISO to Proxmox Local Storage (User Action) — **CLOSED 2026-04-30**

- **Status:** ✅ CLOSED 2026-04-30 — RHEL ISOs placed on all three dev-cluster nodes via local Directory storage; the original P0.0 dependency was decoupled
- **Priority:** _Was BLOCKING_ — P0.1 (Worker VM creation) and P0.2 (YARN RM VM creation) had been gated on RHEL ISO availability; resolved 2026-04-30
- **Resolution (2026-04-30):**
  - User used the node-local ZFS path `/rpool/data` for ISO placement instead of waiting on Ceph (`/var/lib/vz/template/iso/` was the originally-assumed path; Ceph-backed shared storage was the originally-assumed eventual destination). Decoupling from P0.0 freed BLOCKER.2 to close immediately.
  - **Proxmox storage configuration steps (performed by user):**
    1. Datacenter → Storage → Add → **Directory** entry for `/rpool/data`
    2. Enabled content type **ISO image** on the new Directory storage entry
    3. Proxmox auto-created `/rpool/data/templates/iso/` as part of the Add process
    4. Moved the ISO files from `/rpool/data` into `/rpool/data/templates/iso/` so Proxmox's Create-VM wizard can see them
  - **Replication:** ISOs placed on all three dev-cluster nodes (Proxmox Directory storage is local-per-node, not shared, so each node was populated independently). VM creation on any node can now boot from local ISO without inter-node copy.
- **RHEL Versions Placed:**
  - **RHEL 9.4 — committed.** This is the version Ksolves originally requested; user has elected not to block on RHEL 9.7 compatibility research and will proceed with 9.4 for all Phase 1 VM creation.
  - **RHEL 9.7 — held on disk.** Placed alongside 9.4 in case Ksolves' Spark 3.5.3 compatibility research lands favorably and a future migration is desired. Not on the critical path.
- **Verification (completed 2026-04-30):**
  - [x] `/rpool/data` registered as Datacenter Directory storage with ISO content enabled on all three nodes
  - [x] Both RHEL 9.4 and RHEL 9.7 ISOs visible in `/rpool/data/templates/iso/` on each node
  - [x] Proxmox Create-VM wizard sees the ISOs as bootable
- **Owner:** User (fqdn) — completed
- **Effort:** ~1 hour (Datacenter Storage configuration + ISO placement on three nodes)
- **Downstream impact:** P0.1 and P0.2 VM creation no longer gated on this blocker; only BLOCKER.1 (Ksolves remote access, including the new vendor Windows-host hardware prerequisite) remains.

---

<a id="phase-2a-critical-path-vm-provisioning"></a>

### Phase 2A — Critical Path: VM Provisioning & Foundational Software (P0)

<a id="p0-0-ceph-cluster-bootstrap"></a>

### 🔴 P0.0 — Ceph Cluster Bootstrap (MON, MGR, OSD, RGW)

- **Status:** PENDING BLOCKER.1 (KSOLVES ACCESS)
- **Priority:** CRITICAL — Foundation for entire Phase 1 storage layer; gates RGW-dependent tasks (P1.1 Spark History Server, P2.3 8-stage data flow) and Spark scratch allocation
- **Context:** Ceph Reef 18.2.x cluster must be bootstrapped on all three Proxmox nodes before any VM provisioning or RHEL ISO placement. The cluster spans MON daemons (Paxos quorum), MGR daemons (active/standby), OSD daemons (one per NVMe drive 1–3 per node, 9 OSDs total), and RGW (S3-compatible endpoint). This is Ksolves' **first work item** after gaining Proxmox access.
- **Prerequisites:**
  - [ ] BLOCKER.1 complete (Ksolves has Proxmox access)
  - [ ] Proxmox VE 8.3 installed and clustered on all three nodes (assumed pre-existing)
  - [ ] Network bonding (2×10G LACP) configured at Proxmox host level
  - [ ] NVMe drives 1–3 per node available (3 OSDs/node = 9 OSDs total)
- **Ksolves Actions:**
  - [ ] **Install Ceph Reef 18.2.x packages** on all three Proxmox nodes (via Proxmox PVE Ceph integration or cephadm)
  - [ ] **Bootstrap Ceph cluster** on Node01 with `pveceph init` or `cephadm bootstrap`; configure cluster network on bonded 10G LACP
  - [ ] **Deploy Ceph MON daemons** on all three nodes (Node01, Node02, Node03) — Paxos quorum requires 2-of-3 agreement; verify with `ceph mon stat`
  - [ ] **Deploy Ceph MGR daemons:**
     - Active MGR on Node01
     - Standby MGR on Node02 and Node03
     - Verify with `ceph mgr services`
  - [ ] **Configure Ceph OSDs** (9 total, 3 per node):
     - Allocate NVMe drives 1–3 on each node as OSDs
     - Use BlueStore backend (default for Reef)
     - Set `osd_memory_target=4G` per OSD (per Ksolves Phase 1 spec)
     - Verify with `ceph osd tree` (should show 9 OSDs across 3 hosts, all `up` and `in`)
  - [ ] **Set replication and storage policies:**
     - Pool replication: 3× (size=3, min_size=2)
     - Verify usable capacity: ~11.52 TB after 3× replication + BlueStore overhead
  - [ ] **Deploy Ceph RGW (S3 endpoint):**
     - Install `radosgw` daemon on all three nodes
     - Configure floating IP / load balancer for S3 endpoint stability
     - Allocate 4c / 8GB per RGW instance (per infrastructure reservation)
     - Generate initial S3 access keys (admin)
     - Verify with `radosgw-admin user list`
  - [ ] **Verify cluster health:**
     - `ceph -s` shows HEALTH_OK
     - `ceph osd df` shows balanced data distribution
     - `ceph health detail` shows no warnings
- **Verification:**
  - [ ] Ceph cluster status: HEALTH_OK
  - [ ] 9 OSDs `up` and `in`, 3× replication confirmed
  - [ ] 3 MON daemons in quorum
  - [ ] 1 active MGR + 2 standby
  - [ ] RGW S3 endpoint accessible (test with `s3cmd` or `aws s3 ls --endpoint-url=<rgw-endpoint>`)
  - [ ] Usable capacity: ~11.52 TB available
- **User Sign-Off:** Confirm Ksolves has reported HEALTH_OK and provided S3 endpoint URL/credentials before proceeding to downstream tasks that depend on RGW
- **Owner:** Ksolves
- **Estimated Effort:** 4-6 hours (cluster bootstrap + OSD allocation + RGW setup + verification)
- **Critical Note:** RGW endpoint must be live for P1.1 (Spark History Server) and P2.3 (8-stage data flow) to function. RHEL ISO availability is no longer gated on this task — BLOCKER.2 closed 2026-04-30 via node-local Directory storage at `/rpool/data/templates/iso/`.

---

<a id="p0-4-validate-rhel-subscriptions"></a>

### 🔴 P0.4 — Verify RHEL 9.4 Subscriptions Active (Pre-requisite)

- **Status:** OPEN (USER VERIFICATION)
- **Priority:** CRITICAL — Must be confirmed BEFORE VM provisioning begins
- **Context:** RHEL 9.4 subscriptions must be active on all VMs for yum package installation, security patches, and kernel updates. Confirmation required before Ksolves begins P0.1 VM provisioning so they can proceed immediately with package installation after VM creation.
- **User Actions Required:**
  - [ ] Contact RHEL subscription administrator (or check existing fqdn subscription account)
  - [ ] Verify subscriptions are active for at least 4 RHEL 9.4 licenses (3 Worker VMs + 1 YARN RM VM)
  - [ ] Confirm subscription status: active through end of Phase 1 + buffer (minimum 6 months)
  - [ ] Document subscription keys or proof of active subscriptions
  - [ ] Share confirmation with Ksolves before they start P0.1
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
  - [ ] Analyze local CSV file inventory:
     - Count total number of CSV files in production source
     - Determine size distribution (breakdown by size ranges: <100MB, 100MB–1GB, 1GB–10GB, 10GB+, etc.)
     - Calculate average file size
  - [ ] Measure compression ratio for production CSV files:
     - Select representative sample of CSV files (10–20 files across size range)
     - Compress samples using ZSTD codec (per Ksolves recommendation)
     - Calculate uncompressed size vs. compressed size ratio (e.g., 4 TB → 1.2 TB = 3.3× compression)
  - [ ] Document and share with Ksolves:
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
  - [ ] Provision three RHEL 9.4 VMs on Proxmox: GKPR-SPARK-WK-01 (Node01), GKPR-SPARK-WK-02 (Node02), GKPR-SPARK-WK-03 (Node03)
  - [ ] Allocate 18 vCPU per VM (dev cluster has single NUMA domain × 32 cores per node; 18 vCPU fits within one domain — NUMA pinning enabled, no boundary crossing)
  - [ ] Allocate 384 GB RAM per VM (from dev cluster infrastructure reservation: 12c/33GB per node leaves 20c/351 GB available)
  - [ ] Attach NVMe drives 4-7 to scratch mount (15.36 TB per node for Spark shuffle)
  - [ ] Configure RHEL network, SSH, and passwordless sudo access
- **Verification:** All three Worker VMs boot successfully; `lscpu` confirms 18 vCPU per VM; `mount | grep /var/spark/scratch` confirms NVMe attachment
- **User Sign-Off:** Confirm Ksolves has provisioned all Worker VMs before proceeding to P0.2
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours

<a id="p0-2-yarn-resourcemanager-vm"></a>

### 🔴 P0.2 — YARN ResourceManager VM Provisioning — VM Creation Only

- **Status:** PENDING REMOTE ACCESS (BLOCKER.1) — RHEL ISO already in place per BLOCKER.2 closure
- **Priority:** CRITICAL — Hardware foundation for YARN (deployed in P1.2)
- **Context:** Ksolves will create one RHEL 9.4 VM to host the YARN ResourceManager daemon. **This task is VM provisioning only** — YARN ResourceManager daemon install is P1.2. Per vendor decision (2026-04-27), the YARN RM runs as a single instance with manual recovery on failure (no HA, no standby VM, no ZooKeeper).
- **Ksolves Actions:**
  - [ ] Provision GKPR-YARN-RM-01 VM on Node01 (2 vCPU / 4 GB, RHEL 9.4)
  - [ ] Configure RHEL network, SSH, and passwordless sudo access on the VM
  - [ ] Verify VM boots successfully and accepts SSH connections
  - [ ] Install Java 11 JDK (`yum install -y java-11-openjdk`) on the VM (prerequisite for YARN RM daemon)
- **Verification:** VM boots successfully; `lscpu` confirms 2 vCPU and 4 GB RAM; SSH access verified; Java 11 installed
- **User Sign-Off:** Confirm YARN RM VM is provisioned and accessible before P1.2 deployment
- **Owner:** Ksolves
- **Estimated Effort:** 1 hour (VM provisioning + base RHEL config + Java install)
- **Note:** YARN ResourceManager daemon install → P1.2. Manual-recovery posture: if the RM VM fails, it must be restarted manually; no automatic failover.

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
  - [ ] Contact network team to confirm WAN egress capacity available for production cluster
  - [ ] Verify 1 Gbps sustainable throughput (not burst; must handle continuous transfers)
  - [ ] Confirm no rate-limiting or QoS policies that would throttle inter-batch transfers
  - [ ] Document any limitations or constraints (e.g., scheduled maintenance windows, bandwidth sharing with other systems)
  - [ ] Share network validation with Ksolves before P2.3 (Parquet egress implementation)
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
  - [ ] After VM provisioning complete (P0.1), run `subscription-manager list` on all Worker and YARN RM VMs
  - [ ] Verify yum can resolve packages: `yum search java-17-openjdk`
  - [ ] If issues detected, contact fqdn with subscription error details
  - [ ] Apply latest RHEL 9.4 patches: `yum update -y`
- **Verification:** `yum install` succeeds without subscription warnings on all VMs
- **Owner:** Ksolves (with fqdn subscription support)
- **Estimated Effort:** < 1 hour
- **Dependency:** Requires pre-flight confirmation from P0.4 (subscriptions must be active before VM provisioning)

<a id="p0-5-install-hadoop"></a>

### 🔴 P0.5 — Install Java 11 + Hadoop 3.4.1 on All Worker VMs (YARN client libraries only)

- **Status:** PENDING VM PROVISIONING (P0.1)
- **Priority:** CRITICAL — Foundation for Spark 3.5.3 (P0.5a); required for YARN integration
- **Context:** Spark 3.5.3 requires Java JDK + standalone Hadoop installation on each Worker VM. Per Apache Spark documentation,¹ Hadoop binaries provide the YARN client libraries and Hadoop S3A connector (used to access Ceph RGW). **HDFS is NOT used** — Phase 1 storage is Ceph RGW (S3-compatible), so HDFS daemons are not deployed. Hadoop is installed solely for: (1) YARN client classpath, (2) S3A connector for Ceph RGW. **Java compatibility note:** Apache Hadoop 3.4.1 does not officially support Java 17;¹ Java 11 is the recommended version (compatible with both Hadoop 3.4.1 and Spark 3.5.3).
- **Ksolves Actions:**
  - [ ] **Install Java 11 JDK** on all three Worker VMs:
     - `yum install -y java-11-openjdk java-11-openjdk-devel`
     - Set `JAVA_HOME=/usr/lib/jvm/java-11-openjdk` in `/etc/environment`
     - Verify: `java -version` shows OpenJDK 11
  - [ ] **Download Hadoop 3.4.1 binary** from Apache mirrors to all three Worker VMs
  - [ ] **Extract** to `/opt/hadoop-3.4.1` on each node
  - [ ] **Set environment variables** in `/etc/environment`:
     - `HADOOP_HOME=/opt/hadoop-3.4.1`
     - `HADOOP_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `YARN_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - Add `$HADOOP_HOME/bin` to PATH
  - [ ] **Configure `core-site.xml`** for S3A (Ceph RGW) connector:
     - `fs.s3a.endpoint=<Ceph RGW endpoint from P0.0>`
     - `fs.s3a.access.key=<from P0.0 RGW credentials>`
     - `fs.s3a.secret.key=<from P0.0 RGW credentials>`
     - `fs.s3a.path.style.access=true` (for Ceph RGW compatibility)
  - [ ] **Configure `yarn-site.xml`** to point to YARN ResourceManager on GKPR-YARN-RM-01 (placeholder — will be finalized in P1.2)
  - [ ] **Do NOT start HDFS daemons** (NameNode, DataNode) — HDFS is not used in Phase 1
  - [ ] Verify with `hadoop version` on each node; verify S3A connectivity: `hadoop fs -ls s3a://ingest/`
- **Prerequisites:**
  - [ ] P0.1 (Worker VMs provisioned)
  - [ ] P0.4b (RHEL subscriptions verified, yum working)
  - [ ] P0.0 (Ceph RGW endpoint and S3 credentials available)
- **Verification:**
  - [ ] `java -version` shows OpenJDK 11 on all three Worker VMs
  - [ ] `hadoop version` returns Hadoop 3.4.1
  - [ ] `hadoop classpath` returns non-empty output
  - [ ] `hadoop fs -ls s3a://<bucket>/` succeeds (validates S3A → Ceph RGW connectivity)
  - [ ] HDFS daemons NOT running (`jps` shows no NameNode/DataNode processes)
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours (Java + Hadoop install + S3A configuration)
- **Critical Note:** This task is the foundation for P0.5a (Spark install); confirm completion before proceeding

<a id="p0-5a-install-spark"></a>

### 🔴 P0.5a — Install Apache Spark 3.5.3 on All Worker VMs

- **Status:** PENDING P0.5 (HADOOP + JAVA) COMPLETION
- **Priority:** CRITICAL — Phase 1 compute engine; required for P1.8 sample jobs and all Spark workloads
- **Context:** Per Apache Spark documentation,¹ installation order on YARN is: Java → Hadoop/YARN client → Spark binary distribution. Spark 3.5.3 must be installed on each Worker VM as a standalone install (not via Hadoop ecosystem packaging). The "no-hadoop" Spark distribution will be used since Hadoop 3.4.1 is already installed (P0.5) — Spark will use the existing Hadoop classpath. Spark on YARN requires `HADOOP_CONF_DIR` to locate the YARN ResourceManager.
- **Prerequisites:**
  - [ ] **P0.5 complete** (Java 11 + Hadoop 3.4.1 installed, `HADOOP_CONF_DIR` set)
  - [ ] **P0.0 complete** (Ceph RGW endpoint live for S3A reads/writes)
  - [ ] **P1.2 complete** (YARN ResourceManager running) — required for `spark-submit --master yarn`
- **Ksolves Actions:**
  - [ ] **Download Spark 3.5.3** ("with-Hadoop-free" build) from Apache mirrors:
     - URL pattern: `https://archive.apache.org/dist/spark/spark-3.5.3/spark-3.5.3-bin-without-hadoop.tgz`
     - Download to all three Worker VMs
  - [ ] **Extract** to `/opt/spark-3.5.3` on each Worker VM
  - [ ] **Set environment variables** in `/etc/environment`:
     - `SPARK_HOME=/opt/spark-3.5.3`
     - Add `$SPARK_HOME/bin` and `$SPARK_HOME/sbin` to PATH
     - Set `SPARK_DIST_CLASSPATH=$(hadoop classpath)` (required for "without-hadoop" build)
  - [ ] **Configure `$SPARK_HOME/conf/spark-defaults.conf`:**
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
  - [ ] **Configure `$SPARK_HOME/conf/spark-env.sh`:**
     - `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk`
     - `export HADOOP_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `export YARN_CONF_DIR=/opt/hadoop-3.4.1/etc/hadoop`
     - `export SPARK_DIST_CLASSPATH=$(hadoop classpath)`
  - [ ] **Test installation** with a smoke test:
     - `spark-submit --version` reports Spark 3.5.3 with Java 11
     - Run Pi example on YARN: `spark-submit --master yarn --deploy-mode cluster --class org.apache.spark.examples.SparkPi $SPARK_HOME/examples/jars/spark-examples_*.jar 10`
     - Verify YARN RM accepts the job and reports completion
- **Verification:**
  - [ ] `spark-submit --version` shows Spark 3.5.3 on all Worker VMs
  - [ ] SparkPi example completes successfully on YARN
  - [ ] Event log written to `s3a://spark-history/`
  - [ ] Spark History Server (P1.1) shows the test job after job completion
- **User Sign-Off:** Confirm SparkPi smoke test succeeds before P1.8 (5 sample production jobs)
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours (download, install, configure, smoke test)
- **Critical Note:** Use the "without-hadoop" Spark distribution to leverage the existing Hadoop 3.4.1 install (avoids version conflicts). Java 11 must be set as `JAVA_HOME` for both Hadoop and Spark.

<a id="p0-7-network-connectivity-verification"></a>

### 🔴 P0.7 — Verify Network Connectivity: MSB-PMC01 ↔ MSB-PMC03 (Pre-requisite for P1.0)

- **Status:** OPEN (NETWORK TEAM COORDINATION)
- **Priority:** CRITICAL — Gate for Remote Airflow Server provisioning (P1.0)
- **Context:** Remote Airflow server will be provisioned on MSB-PMC01 cluster. Ksolves requires verified network connectivity between MSB-PMC01 and MSB-PMC03 (Spark cluster nodes) with sufficient bandwidth for:
  - Airflow DAG submission to YARN ResourceManager (port 8032, low bandwidth)
  - Spark driver logs and monitoring (continuous, low-moderate bandwidth)
  - Ansible control node → cluster node SSH (key-based, low bandwidth)
- **User Actions Required:**
  - [ ] Coordinate with fqdn Network Team to verify/establish network path: MSB-PMC01 ↔ MSB-PMC03
  - [ ] Confirm routing between clusters (same VLAN, or routable via firewall)
  - [ ] Verify firewall rules allow:
     - MSB-PMC01 → MSB-PMC03 nodes (TCP 8032, 8088, 22, 9095 for JMX if monitoring)
     - MSB-PMC03 nodes → MSB-PMC01 (return traffic on same ports)
  - [ ] Test connectivity: ping from MSB-PMC01 to each MSB-PMC03 node; TCP port tests (`nc -zv`)
  - [ ] Document network topology and firewall rules for audit trail
  - [ ] Share verification results with Ksolves before P1.0 provisioning begins
- **Verification:** 
  - [ ] Network team confirms connectivity in change ticket
  - [ ] Ping response times < 10ms (same datacenter assumed)
  - [ ] TCP ports open: `nc -zv <node> 8032`, `nc -zv <node> 8088` succeed on all three MSB-PMC03 nodes
- **Owner:** fqdn Network Team
- **Estimated Effort:** 2-4 hours (coordination + testing + documentation)
- **Critical Note:** This is a hard gate. P1.0 cannot proceed until network connectivity verified and documented.

---

<a id="phase-2b-high-priority-infrastructure-services"></a>

### Phase 2B — High Priority: Infrastructure Services & HA (P1)

<a id="p1-0-provision-remote-airflow-host"></a>

### 🟠 P1.0 — Provision Remote Airflow Server (Ksolves Open Item #8)

- **Status:** PENDING P0.7 NETWORK VERIFICATION (REMOTE INFRASTRUCTURE)
- **Priority:** HIGH — Prerequisite for Airflow orchestration and Ansible automation
- **Context:** Remote Airflow host coordinates ETL job submission to Spark cluster. Must run Airflow webserver/scheduler, Okta SSO integration, and Ansible control node. Spec: **6 vCPU / 24 GB RAM / 500 GB SSD**, RHEL 9.4. **Target node: `msb-pmc01-04`** — Intel Xeon Gold 6136 @ 3.00 GHz, 1 socket × 12 cores × 2 threads (24 logical CPUs), 130 GB RAM, single NUMA node, 6 Ceph OSDs. Cluster is fqdn-managed; Ksolves provisions services into it. See `phases/phase2/development/Document/MSB-PMC01_cluster_host_inventory.md` for full hardware inventory of all four nodes (msb-pmc01-01 through 04).
- **Recommended Proxmox VM topology:** `sockets=1, cores=6`. Host is single-NUMA — no NUMA pinning required. 24 GB RAM ≈ 18% of host's 130 GB. 500 GB volume drawn from the `rbd_ssd` Ceph pool (visible in OSD tree as the dedicated SSD class).
- **Dependency:** **P0.7 (Network Connectivity) must be completed and verified first** — MSB-PMC01 and MSB-PMC03 clusters must be on same network with confirmed firewall rules.
- **Ksolves Actions:**
  - [ ] After network connectivity verified (P0.7), provision VM on `msb-pmc01-04`: `sockets=1, cores=6` / 24 GB RAM / 500 GB SSD (rbd_ssd pool), RHEL 9.4
  - [ ] Configure hostname: `airflow-prod-01` (or fqdn-assigned name)
  - [ ] Network setup: routable to all three MSB-PMC03 Spark nodes, to Snowflake, to cloud staging (Azure/AWS)
  - [ ] Install Okta SSO integration (requires OIDC client ID/secret from fqdn Okta tenant)
  - [ ] Verify SSH key access from Ansible control node (to be installed on this host)
  - [ ] Verify network paths: Airflow → YARN RM (port 8032), Airflow → Ceph RGW (floating IP), Airflow → Snowflake
- **User Actions:**
  - [ ] Confirm MSB-PMC01 hosting and IP allocation (coordinate with Network Team)
  - [ ] Provide Okta OIDC credentials for Airflow SSO configuration
  - [ ] Ensure network connectivity verification (P0.7) complete before Ksolves begins provisioning
- **Prerequisites:** 
  - [ ] **P0.7 network connectivity verified and documented**
  - [ ] Okta SSO client provisioned
  - [ ] MSB-PMC01 networking and IP allocation finalized
- **Verification:** SSH to remote host successful; RHEL subscriptions active; network paths confirmed (ping tests to all three cluster nodes <10ms, TCP port tests succeed, Snowflake/cloud routing confirmed)
- **Owner:** Ksolves (provisioning) + fqdn (networking, SSO setup)
- **Estimated Effort:** 2-3 hours (provisioning + network setup)
- **Critical Note:** P1.5 (Ansible) and later P2 items depend on this host being live and network-connected

---

### 🟠 P1.1 — Deploy Spark History Server on Node02

- **Status:** PENDING P0.0 (CEPH RGW) + P0.1 (WORKER VMs) + P0.5a (SPARK INSTALL)
- **Priority:** HIGH — Phase 1 observability and diagnostics
- **Context:** Spark History Server (GKPR-SPARK-HS-01) runs as 1 vCPU / 4 GB VM on Node02. Reads event logs from `s3a://spark-history/` on Ceph RGW (RGW endpoint and credentials provisioned in P0.0). Required for Spark job monitoring and debugging during Phase 1 runs.
- **Ksolves Actions:**
  - [ ] Provision Spark History Server VM on Node02 (1c / 4GB, RHEL 9.4)
  - [ ] Install Spark 3.5.3 and configure to read event logs: `spark.history.fs.logDirectory=s3a://spark-history/`
  - [ ] Create S3 bucket on Ceph RGW: `s3://spark-history` (uses RGW endpoint and S3 access/secret keys generated in P0.0)
  - [ ] Configure S3A connector in `spark-defaults.conf` (endpoint, path-style access — see P0.5a)
  - [ ] Start Spark History Server daemon (port 18080)
- **Prerequisites:** Ceph RGW operational (P0.0); `spark-history` bucket created with RGW credentials from P0.0
- **Verification:** Navigate to http://Node02:18080; confirm jobs appear after spark-submit runs
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

<a id="p1-2-deploy-yarn"></a>

### 🟠 P1.2 — Deploy YARN ResourceManager (Single Instance, Manual Recovery)

- **Status:** PENDING P0.2 (YARN RM VM) + P0.5 (HADOOP) ON WORKER VMs
- **Priority:** HIGH — Phase 1 compute orchestration
- **Context:** YARN ResourceManager runs as a single daemon on `GKPR-YARN-RM-01` (Node01). Per vendor decision (2026-04-27), the development cluster does not run an HA pair; if the RM VM or daemon fails, recovery is manual (operator restarts the daemon or the VM). No standby VM, no ZooKeeper ensemble, and no nginx reverse proxy. Spark drivers and Airflow clients connect directly to the RM endpoint.
- **Ksolves Actions:**
  - [ ] Install YARN ResourceManager on GKPR-YARN-RM-01 (Node01)
  - [ ] Configure `yarn-site.xml` with single-RM settings: `yarn.resourcemanager.hostname=<GKPR-YARN-RM-01 FQDN>`; leave `yarn.resourcemanager.ha.enabled=false` (default)
  - [ ] Update `yarn-site.xml` on every Worker VM (P0.5) to point to GKPR-YARN-RM-01
  - [ ] Start the ResourceManager service and verify it accepts NodeManager registrations from all three Worker VMs
  - [ ] Document the manual recovery runbook (how to restart the RM daemon and the VM) and hand it to fqdn ops
- **Prerequisites:**
  - [ ] YARN RM VM (P0.2) provisioned with Java 11
  - [ ] Worker VMs (P0.1) running with NodeManager and `yarn-site.xml` pointing at the RM
  - [ ] Network connectivity between RM VM and all three Worker VMs
- **Verification:** YARN RM web UI reachable at `http://GKPR-YARN-RM-01:8088`; `yarn node -list` shows all three NodeManagers as RUNNING; a `spark-submit --master yarn` smoke job completes
- **User Sign-Off:** Confirm YARN RM is stable and the manual-recovery runbook is in place before Phase 1 load tests
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

### 🟠 P1.5 — Deploy Ansible Control Node on Remote Airflow Host

- **Status:** PENDING REMOTE AIRFLOW HOST (P1.0)
- **Priority:** HIGH — Required for infrastructure automation
- **Context:** Ansible control node on remote Airflow host enables programmatic cluster management, configuration updates, and VM lifecycle operations. Must have SSH key access to all cluster nodes and Proxmox API token for VM operations.
- **Ksolves Actions:**
  - [ ] Provision remote Airflow host if not yet done (P1.0)
  - [ ] Install Ansible 2.10+ and Python 3.11+ on remote Airflow host
  - [ ] Generate SSH keypair; distribute public key to all cluster nodes (Node01, Node02, Node03) for passwordless access
  - [ ] Store Proxmox API token securely (recommend pass or dedicated secrets manager)
  - [ ] Clone Ansible playbooks from git repository (if exists) or stage initial plays
  - [ ] Test connectivity: `ansible all -i hosts -m ping` should reach all nodes
- **Prerequisites:** Remote Airflow host provisioned; SSH access to all cluster nodes; Proxmox API token generated
- **Verification:** `ansible -i hosts -m command -a "uname -a" all` returns kernel info from all nodes; Proxmox API token successfully authenticates
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

### 🟠 P1.6 — Monitor Ceph OSD Memory Under Peak Ingest

- **Status:** PENDING P0.0 (CEPH BOOTSTRAP) + LOAD TEST (P1.8)
- **Priority:** HIGH — Critical for storage stability
- **Context:** Initial `osd_memory_target=4G` is set during Ceph bootstrap (P0.0). Phase 1 assumes ~3 GB actual usage per OSD under typical load. Must monitor actual memory consumption under peak 4 TB/batch ingest load. If OSD memory exceeds headroom, Ksolves will increase `osd_memory_target` and re-validate.
- **Note on Metrics Collection:** Phase 1 has no dedicated Grafana setup task — the existing Grafana instance (referenced in master TODO `## Open Questions`) is on the monitoring cluster and not yet connected to this Spark cluster's Ceph metrics. For Phase 1 monitoring, capture OSD memory via direct Ceph commands (`ceph osd df`, `ceph daemon osd.<id> dump_mempools`) and node-level tools (`top`, `pidstat`). Grafana dashboard build-out is deferred to Phase 2 / monitoring cluster integration.
- **Ksolves Actions:**
  - [ ] During Phase 1 load test (P1.8), capture OSD memory peaks across all ingest cycles using `ceph daemon osd.<id> dump_mempools` and `ps`/`top` snapshots at 30s intervals
  - [ ] If peak memory > 3.5 GB, incrementally increase `osd_memory_target` (e.g., 4.5GB → 5GB) via `ceph config set osd osd_memory_target <bytes>` and re-test
  - [ ] Document final `osd_memory_target` value in as-built configuration (P3.2)
- **Success Criteria:** OSD memory stays < 3.5 GB peak during 4 TB batch (relative to initial 4 GB target from P0.0)
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (setup) + data collection during load test

### 🟠 P1.7 — Validate WAN Egress Throughput (1 Gbps Target)

- **Status:** PENDING LOAD TEST (P1.8)
- **Priority:** HIGH — Critical for cloud staging speed
- **Context:** Phase 1 assumes 1 Gbps (≈125 MB/s) outbound throughput from cluster to cloud staging (Azure Blob or AWS S3, TBD at P0.3). Must validate actual achievable throughput with Parquet transfers during Phase 1 load tests.
- **Ksolves Actions:**
  - [ ] During Phase 1 load test (P1.8), measure WAN egress throughput in Stage 6 (cloud egress)
  - [ ] Monitor exaBGP floating IP routing to Snowflake egress point; check for packet loss or latency anomalies
  - [ ] Capture sustained throughput over 5–10 minute transfer window
  - [ ] If sustained < 100 MB/s: diagnose network path (check for QoS limits, jumbo frames, MTU mismatch)
- **Success Criteria:** Sustained ≥100 MB/s during Parquet transfer; 0 packet loss
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (measurement during load test)

<a id="p1-8-run-5-production-sample-jobs"></a>

### 🟠 P1.8 — Run 5 Production Sample Jobs (Shuffle Amplification Measurement) — Phase 1 Integration Milestone

- **Status:** PENDING FULL P0 + P1 INFRASTRUCTURE (P0.0–P0.5a, P1.0–P1.2, P1.5)
- **Priority:** HIGH — Validates Phase 1 assumptions and updates default calculator values; gates Phase 2C end-to-end pipeline validation (P2.3)
- **Context:** Phase 1 assumes 7× shuffle amplification; actual measurement needed from real workload. P1.8 is the Phase 1 integration milestone — it cannot run until VMs (P0.1–P0.2), Hadoop/Spark (P0.5–P0.5a), Ceph (P0.0), and YARN RM (P1.2) are all operational. Ksolves will execute 5 sample production jobs at varying sizes (500 GB, 1 TB, 2 TB, 4 TB, 5 TB) and capture actual shuffle behavior. P1.6 (OSD memory) and P1.7 (WAN egress) collect their measurements concurrently during this load test.
- **Ksolves Actions:**
  - [ ] Confirm full infrastructure is live: P0.0 (Ceph), P0.1 (Worker VMs), P0.2 (YARN RM VM), P0.5 (Hadoop+Java), P0.5a (Spark), P1.2 (YARN ResourceManager)
  - [ ] Prepare sample CSV datasets (500 GB, 1 TB, 2 TB, 4 TB, 5 TB)
  - [ ] Submit 5 sequential Spark jobs (one per dataset size) via direct `spark-submit` (Airflow integration is P2.2 → P2.3, not required for P1.8)
  - [ ] For each job, capture:
     - Task shuffle output vs. input ratio (actual amplification factor)
     - Shuffle write bandwidth (MB/s)
     - Ceph RGW throughput ceiling
     - Memory utilization under peak shuffle
     - NVMe scratch I/O patterns
     - OSD memory peaks (feeds P1.6) and WAN egress throughput (feeds P1.7)
  - [ ] Calculate average amplification factor and update `phases/phase1/development/deliverables/dev_cluster_phase1_model.html` default
- **Expected Output:** Actual shuffle amplification factor (e.g., 5.2× instead of assumed 7×) feeds into Phase 1 concurrency SLA
- **Verification:** `phases/phase1/development/deliverables/dev_cluster_phase1_model.html` updated with measured value
- **User Sign-Off:** Review measured amplification and confirm it satisfies Phase 1 SLA (40 jobs in 4 hours)
- **Owner:** Ksolves
- **Estimated Effort:** 2-4 hours

---

<a id="phase-2c-medium-priority-configuration-validation"></a>

### Phase 2C — Medium Priority: Configuration, Validation & Integration (P2)

### 🟡 P2.2 — Deploy Apache Airflow 2.10.4 on Remote Host

- **Status:** PENDING REMOTE HOST (P1.0)
- **Priority:** MEDIUM — Phase 1 job orchestration
- **Context:** Airflow triggers spark-submit via DAG scheduler. CeleryExecutor confirmed for distributed job submission to YARN RM. Database can be embedded (docker-compose PostgreSQL) or standalone.
- **Ksolves Actions:**
  - [ ] Install Python 3.11+, pip, and dependencies
  - [ ] Install Apache Airflow 2.10.4: `pip install apache-airflow[celery,postgres]`
  - [ ] Initialize Airflow database: `airflow db init`
  - [ ] Configure CeleryExecutor in airflow.cfg (broker: Redis or RabbitMQ; backend: PostgreSQL)
  - [ ] Create DAG for Phase 1: stage CSV ingest, trigger Spark jobs, track completion
  - [ ] Set up Airflow web UI (default http://host:8080) with basic auth or Okta integration
- **Verification:** Airflow web UI accessible; DAG uploads successfully; manual trigger works
- **Owner:** Ksolves
- **Estimated Effort:** 2-3 hours

### 🟡 P2.3 — Validate 8-Stage Data Flow Pipeline (CSV → Snowflake)

- **Status:** PENDING FULL INFRASTRUCTURE (P0.0–P0.5a, P1.0, P1.2, P2.2)
- **Priority:** MEDIUM — End-to-end integration test
- **Context:** Phase 1 data flow spans 8 sequential stages from CSV ingest through Snowflake COPY. Each stage has specific requirements (Airflow DAG, Spark containers, S3A reads/writes, cloud staging). Ksolves will validate the complete pipeline with a sample dataset.
- **Stages to Validate:**
  - [ ] CSV Ingest → Ceph RGW (s3a://ingest/csv/)
  - [ ] Airflow DAG trigger via Airflow scheduler
  - [ ] YARN container scheduling (confirm executors allocated)
  - [ ] Spark ETL execution (CSV → Parquet, Snappy compression on shuffle)
  - [ ] Parquet writes to Ceph RGW (s3a://output/parquet/)
  - [ ] Cloud egress to Azure Blob / AWS S3 (requires cloud staging decision at P0.3)
  - [ ] Snowflake COPY INTO (internal stage → table)
  - [ ] Cleanup gate (delete Parquet from Ceph after Snowflake confirmation)
- **Ksolves Actions:**
  - [ ] Prepare sample CSV dataset (500 GB or 1 TB)
  - [ ] Upload CSV to Ceph ingest bucket: s3a://ingest/csv/
  - [ ] Trigger Airflow DAG manually or via scheduler
  - [ ] Monitor Spark job execution: stages, executors, shuffle behavior
  - [ ] Verify Parquet output in Ceph: s3a://output/parquet/
  - [ ] Test cloud staging egress (once P0.3 decision made)
  - [ ] Verify Snowflake COPY INTO succeeds and data appears in target table
  - [ ] Confirm cleanup removes Parquet after Snowflake confirmation
- **Verification:** End-to-end single job completes successfully; data visible in Snowflake; no data loss in pipeline
- **User Sign-Off:** Review pipeline execution logs and confirm all stages work as expected
- **Owner:** Ksolves
- **Snowflake Scope Note:** The Snowflake side of the pipeline is **out of scope for Ksolves and this Phase 1 plan**. fqdn is responsible for: (a) Snowflake account/warehouse provisioning and credentials, (b) target database/schema/table DDL, (c) `COPY INTO` statement authorship and stage configuration (named external stage pointing at the cloud bucket from P0.3), (d) Snowflake-side IAM/storage integration, and (e) Snowpipe or scheduled ingest if used. Ksolves' P2.3 validation ends at delivering a successful `COPY INTO` execution against fqdn-provided Snowflake objects; ongoing Snowflake operations remain a fqdn responsibility.
- **Estimated Effort:** 3-4 hours

<a id="p2-4-confirm-compression"></a>

### 🟡 P2.4 — Confirm Compression Codec Configuration

- **Status:** PENDING SPARK CONFIG
- **Priority:** MEDIUM — Performance and storage optimization
- **Context:** Phase 1 specifies Snappy for shuffle intermediates (2.5× compression, low CPU) and ZSTD for Parquet output (5× compression, higher CPU). Ksolves will validate codec performance during Phase 1 load test (P1.8).
- **Ksolves Actions:**
  - [ ] Configure spark-defaults.conf with compression settings:
     ```
     spark.shuffle.compress=true
     spark.shuffle.spill.compress=true
     spark.io.compression.codec=snappy
     spark.sql.parquet.compression.codec=zstd
     ```
  - [ ] During Phase 1 load test (P1.8), monitor:
     - CPU usage during shuffle phase
     - Actual compression ratio (shuffle output / input)
     - Throughput impact (MB/s with vs. without compression)
  - [ ] If compression overhead > 5% CPU, consider codec swap (e.g., LZ4 for shuffle, ZSTD for output)
- **Verification:** Phase 1 load test meets 4-hour SLA with compression enabled; compression ratios match expectations
- **Owner:** Ksolves
- **Estimated Effort:** < 1 hour (config) + observation during load test

<a id="p2-5-validate-jbod"></a>

### 🟡 P2.5 — Validate JBOD Storage Configuration (NVMe Drives 4–7, XFS)

- **Status:** PENDING VM PROVISIONING (P0.1)
- **Priority:** MEDIUM — Critical for shuffle performance
- **Context:** NVMe drives 4–7 on each node (15.36 TB per node) are configured as JBOD (not RAID) for Spark shuffle scratch using XFS filesystem. No replication. Ksolves will mount, configure permissions, and benchmark I/O during Phase 1 load test.
- **Ksolves Actions:**
  - [ ] After NVMe drives attached to Worker VMs (P0.1), partition and format drives 4–7 with XFS
  - [ ] Mount to /var/spark/scratch (or per-node equivalent)
  - [ ] Set permissions for Spark process user (root or dedicated spark user): `chmod 1777 /var/spark/scratch`
  - [ ] Configure Spark to use scratch mount: `spark.local.dir=/var/spark/scratch`
  - [ ] During Phase 1 load test (P1.8), benchmark I/O:
     - Run `fio` random read/write test on mounted drives
     - Capture peak I/O throughput (target: ~3,000 MB/s aggregate across cluster)
     - Monitor for I/O bottlenecks or dropped tasks
- **Verification:** `fio` benchmark shows ≥2,500 MB/s random I/O; no I/O errors during Phase 1 load test
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (mount + benchmark)

<a id="p2-6-validate-network"></a>

### 🟡 P2.6 — Validate Network Topology (2×10G LACP Bond)

- **Status:** PENDING INFRASTRUCTURE (P0.1)
- **Priority:** MEDIUM — Ensures cluster bandwidth availability
- **Context:** Each node has 2×10G NICs bonded via LACP (Link Aggregation Control Protocol). Phase 1 requires 20G per node effective bandwidth for intra-cluster replication, S3A reads/writes, and WAN egress. Ksolves will verify bond status and validate throughput during Phase 1 load test.
- **Ksolves Actions:**
  - [ ] After VMs provisioned (P0.1), verify LACP bond status on each node: `cat /proc/net/bonding/bond0` should show "Bonding Mode: balance-alb" and both NICs active
  - [ ] If bond not yet configured, set up LACP on switch and VM network stack
  - [ ] During Phase 1 load test (P1.8), validate throughput:
     - Ceph replication: Should saturate ≥95 MB/s per node (intra-cluster traffic)
     - S3A throughput: Should reach ≥284 MB/s aggregate (Ceph RGW ceiling)
     - WAN egress: Should achieve ≥125 MB/s to cloud (P1.7)
  - [ ] Monitor for packet loss: `ethtool -S bond0 | grep errors` should show 0 after load test
- **Verification:** Bond status shows both NICs active; throughput targets met during load test; 0 packet loss
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours (validation during load test)

<a id="p2-7-evaluate-node-addition-timeline"></a>

### 🟡 P2.7 — Evaluate Phase 1 Node Addition Timeline (Ksolves Open Item #9)

- **Status:** PENDING PHASE 1 LOAD TEST RESULTS (P1.8)
- **Priority:** MEDIUM — Critical for Phase 1 → Phase 2 transition planning
- **Context:** Phase 1 report flags 40-job daily SLA as "marginal with 2.1 min buffer" on 3-node cluster. If actual shuffle amplification (P1.8) is higher than assumed 7×, or if concurrent jobs need to exceed 2, a 4th node may be required to hit the SLA reliably. Ksolves will evaluate timing after Phase 1 validation jobs run.
- **Evaluation Criteria:**
  - Actual shuffle amplification factor (measured in P1.8)
  - Concurrent job capability with current 3-node setup
  - If SLA buffer < 5 min for 40 jobs: recommend 4th node addition
  - If SLA buffer ≥ 5 min: proceed with Phase 2 on 3 nodes
- **Ksolves Actions:**
  - [ ] After Phase 1 load test (P1.8) completes, analyze:
     - Actual shuffle amplification vs. 7× assumption
     - Peak memory, CPU, and I/O utilization per node
     - Concurrent job scaling (how many jobs can run simultaneously without SLA breach?)
  - [ ] Calculate revised SLA buffer: (inter-job gap time - job duration) / job duration
  - [ ] If buffer < 5 min: recommend 4th node (same spec: HPE DL385 Gen11, 32c/384GB, 7×3.84TB NVMe)
  - [ ] Provide timeline estimate: can 4th node be provisioned/integrated before Phase 1 production runs?
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
- Shuffle amplification: 7× (uncompressed) — actual measurement required (P1.8)
- Concurrent jobs: 1 → 2 baseline (core-bound, not RAM-bound) — to be measured
- WAN egress: 1 Gbps sustained (125 MB/s actual target, P1.7)
- Cloud staging: Azure Blob or AWS S3 (TBD, P0.3 decision required)
- RHEL 9.4: Active subscriptions on all VMs (P0.4)
- No VMs exist yet; all provisioning is Ksolves responsibility
- No NVMes assigned; Ksolves will allocate per spec (3× Ceph OSD, 4× Spark scratch per node)

**External Dependencies:**
- Ksolves technical contact: Karthik Hegde (karthik.hegde@ksolves.com, 8317382875)
- Ksolves requires owner-level Proxmox access (BLOCKER.1) before any infrastructure work
- fqdn sign-off required at user checkpoints (P0.2, P1.8, P1.2, P2.3) before proceeding to next phase
- Cloud staging platform decision (P0.3) blocks Stage 6 pipeline implementation

**Critical Path Sequence:**
- **Phase 1 (Planning):** ✅ COMPLETE — All discovery & architecture finalized (Apr 24)
- **Phase 2 (Implementation):** PENDING
  - [ ] BLOCKER.1: Establish Ksolves remote access (user action — Phase 1A pending vendor Windows-host hardware prerequisite, Phase 1B parallel)
  - [x] BLOCKER.2: User placed RHEL ISO(s) in Proxmox Directory storage at `/rpool/data/templates/iso/` on all three dev-cluster nodes (closed 2026-04-30 — decoupled from P0.0)
  - [ ] **P0.0: Ksolves bootstraps Ceph cluster** (MON, MGR, 9× OSD, RGW) — first Ksolves work after access granted
  - [ ] *Parallel user prerequisites:* P0.4 (RHEL subscriptions), P0.0a (CSV file info), P0.7 (network MSB-PMC01↔03)
  - [ ] P0.1–P0.5: Ksolves provisions all VMs and base software (RHEL ISO already in place from BLOCKER.2)
  - [ ] **P1.2: Ksolves deploys single-instance YARN ResourceManager on GKPR-YARN-RM-01** (manual recovery; no HA)
  - [ ] P1.0, P1.5: Ksolves provisions Remote Airflow Server and Ansible control
  - [ ] P1.1: Spark History Server deployed on Node02 (depends on P0.0 RGW + P0.5a Spark)
  - [ ] **P1.8: Phase 1 integration milestone — run 5 sample jobs, measure shuffle amplification, OSD memory (P1.6), and WAN egress (P1.7)**
  - [ ] P2.2–P2.3: Ksolves deploys Airflow and validates end-to-end pipeline (Snowflake side is fqdn responsibility)
  - [ ] Phase 2 sign-off: fqdn approves for production if all P0–P2 items pass
- **Beyond Phase 2:** Pending Ksolves clarification — See "Actions Outside Present Known Scope"

---

<a id="reference-documents"></a>

## REFERENCE DOCUMENTS

- **Main Report:** phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf
- **Prerequisites:** phases/phase1/development/Incoming/vendor_prerequisites.docx.pdf
- **Hardware Reference:** CLAUDE.md § Hardware Reference
- **Calculator:** phases/phase1/development/deliverables/dev_cluster_phase1_model.html
- **Ksolves Walkthrough:** phases/phase1/development/research/ksolves-directory-walkthrough.md
- **Vendor Questions:** phases/phase1/development/vendor_comms/phase1_vendor_questions.txt

---

<a id="footnotes"></a>

## FOOTNOTES

¹ Apache Software Foundation, "Running Spark on YARN," in *Apache Spark Documentation*, accessed April 25, 2026, https://spark.apache.org/docs/latest/running-on-yarn.html. The documentation establishes the prerequisite installation order for Spark on YARN: (1) Java/JDK with `JAVA_HOME` set, (2) Hadoop/YARN cluster operational with ResourceManager running, (3) `HADOOP_CONF_DIR` or `YARN_CONF_DIR` pointing to client-side Hadoop configuration, (4) Spark binary distribution built with YARN support. Java compatibility note: "Apache Hadoop 3.4.1 does not support Java 17, but Spark 4.0.0+ requires Java 17+" — for Spark 3.5.3 + Hadoop 3.4.1, Java 11 is the recommended common version. Confirmed with secondary sources: Cloudera/Hortonworks HDP documentation, "Spark Prerequisites," accessed April 25, 2026, https://docs-archive.cloudera.com/HDPDocuments/HDP3/HDP-3.1.5/installing-spark/content/installing_spark.html, which states "HDFS and YARN deployed on the cluster" as Spark prerequisites.

---

---

_Updated: 2026-04-30 (Phase 1A re-opened — vendor Windows-host hardware prerequisite for Webex remote control)_  
_Phase 1 status reflected per ksolves_april_24_process_report.txt_  
_Location: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md_  
_Status: Promoted to Document/ on 2026-04-30_
