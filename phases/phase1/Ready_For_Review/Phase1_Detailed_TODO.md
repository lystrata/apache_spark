
# Phase 1–2 Infrastructure Plan — fqdn Development Cluster

_Phases 1–2 detailed plan from fqdn Phase 1 Report (Ksolves) — April 2026_  
_Report Source: phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf_  
_Status: Phase 1 (Planning) COMPLETED Apr 24 · Phase 2 (Implementation) PENDING BLOCKER.1 · Out-of-scope items flagged for vendor clarification_

---

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

## PHASE 2 — IMPLEMENTATION (PENDING BLOCKER.1)

All Phase 2 infrastructure provisioning awaits BLOCKER.1 (Proxmox access). Once interim Phase 1A access (Webex) is established, Ksolves can execute all P0–P2 items in sequence.

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

### 🔒 BLOCKER.2 — Provision RHEL ISO to Proxmox Local Storage (User Action)

- **Status:** PENDING OSD CONFIGURATION
- **Priority:** BLOCKING — P0.1 (Worker VM creation) and P0.2 (YARN RM VM creation) cannot proceed without RHEL ISO available
- **Context:** User will place RHEL ISO locally in Proxmox local storage **after** Ceph OSDs are fully configured on all three nodes. Ksolves will boot all VMs from this ISO. User performs this action locally while Ksolves team works remotely from India.
- **Dependency:** Requires OSD configuration completion (prerequisite — cannot proceed until OSDs ready)
- **RHEL Version Decision:**
  - **Current Assumption:** RHEL 9.4 (confirmed compatible with Phase 1 requirements)
  - **Under Research:** RHEL 9.7 (penultimate RHEL9 version) — Ksolves researching Apache Spark 3.5.3 compatibility
  - **Decision Timeline:** Await Ksolves compatibility findings before finalizing ISO selection
  - **Fallback:** If RHEL 9.7 incompatible, proceed with RHEL 9.4
- **User Actions Required:**
  1. **Await notification that Ceph OSDs are fully configured and ready** on all three nodes (completion of OSD configuration on all three nodes)
  2. Once OSDs ready, download appropriate RHEL ISO:
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

### Phase 2A — Critical Path: VM Provisioning & Foundational Software (P0)

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

### 🔴 P0.2 — YARN ResourceManager VM Provisioning (Active + Standby)

- **Status:** PENDING REMOTE ACCESS
- **Priority:** CRITICAL — Dependency for YARN HA (P1.2)
- **Context:** Ksolves will create two YARN ResourceManager VMs: one active (Node01), one standby (Node03). Each 2 vCPU / 4 GB, running YARN RM with ZooKeeper ensemble coordination.
- **Ksolves Actions:**
  1. Provision GKPR-YARN-RM-01 VM on Node01 (2 vCPU / 4 GB, RHEL 9.4)
  2. Provision GKPR-YARN-RM-02 VM on Node03 (2 vCPU / 4 GB, RHEL 9.4)
  3. Configure ZooKeeper quorum membership (1 instance per node: Node01, Node02, Node03)
  4. Install YARN ResourceManager and configure HA failover via ZooKeeper
  5. Set up health check scripts and failover triggers
- **Verification:** `yarn resourcemanager -format -force` succeeds on both VMs; ZooKeeper ensemble quorum formed with 2-of-3 agreement
- **User Sign-Off:** Confirm YARN RM VMs and ZooKeeper are live before proceeding
- **Owner:** Ksolves
- **Estimated Effort:** 3-4 hours

### 🔴 P0.3 — Confirm Cloud Staging Target (Azure Blob vs AWS S3)

- **Status:** OPEN (VENDOR DECISION)
- **Priority:** CRITICAL — Blocks egress pipeline design (Stage 6)
- **Context:** Phase 1 data flow (Stage 6) transfers Parquet output from Ceph RGW to cloud staging for Snowflake COPY INTO. Cloud platform decision not yet made.
- **Required Decision:** Azure Blob Storage or AWS S3?
- **Impact:** Determines IAM/SAS token configuration, network routing (exaBGP floating IP routing to Snowflake), and Snowflake COPY command syntax. Ksolves will implement credentials and network config once decision is made.
- **Owner:** fqdn data-platform/decision-maker
- **Deadline:** Before Ksolves begins Stage 6 implementation (P2.3, Step 6)

### 🔴 P0.4 — Validate RHEL 9.4 Subscriptions on All VMs

- **Status:** OPEN (VENDOR VERIFICATION)
- **Priority:** CRITICAL — Blocking Ksolves package installation and OS patching
- **Context:** Ksolves will configure all VMs with RHEL 9.4. Active subscriptions required for yum package installation, security patches, and kernel updates.
- **Ksolves Actions:**
  1. After VM provisioning, run `subscription-manager list` on all Worker and YARN RM VMs
  2. If inactive, contact fqdn to activate subscriptions or provide subscription keys
  3. Verify yum can resolve packages: `yum search java-17-openjdk`
  4. Apply latest RHEL 9.4 patches: `yum update -y`
- **Verification:** `yum install` succeeds without subscription warnings on all VMs
- **Owner:** Ksolves (with fqdn subscription support)
- **Estimated Effort:** < 1 hour

### 🔴 P0.5 — Install Hadoop 3.4.1 on All Worker VMs

- **Status:** PENDING VM PROVISIONING
- **Priority:** CRITICAL — Spark 3.5.3 requires standalone Hadoop installation
- **Context:** Spark does not bundle Hadoop; Ksolves will install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME. Phase 1 depends on this for Hadoop classpath resolution, even though we use Ceph S3A.
- **Ksolves Actions:**
  1. Download Hadoop 3.4.1 binary from Apache mirrors to all three Worker VMs
  2. Extract to /opt/hadoop-3.4.1 on each node
  3. Set HADOOP_HOME=/opt/hadoop-3.4.1 in /etc/environment
  4. Update spark-defaults.conf to reference Hadoop libs: `spark.executor.extraClassPath=/opt/hadoop-3.4.1/lib/*`
  5. Verify with `hadoop version` on each node
- **Verification:** spark-submit resolves Hadoop classes without errors; `hadoop classpath` returns non-empty output
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours

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

---

### Phase 2B — High Priority: Infrastructure Services & HA (P1)

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

- **Status:** PENDING INFRASTRUCTURE (P0.2)
- **Priority:** HIGH — **REQUIRED PREREQUISITE for P1.2** (YARN RM HA cannot be configured until ZooKeeper is operational)
- **Context:** ZooKeeper ensemble (1 instance per node) coordinates YARN ResourceManager failover. Paxos quorum requires 2-of-3 agreement for cluster decisions. Per Apache Hadoop documentation,¹ ZooKeeper must be deployed and running before YARN RM HA configuration begins.
- **Ksolves Actions:**
  1. Install ZooKeeper 3.8+ on all three nodes (Node01, Node02, Node03)
  2. Configure ensemble: each instance knows about the other two (zoo.cfg server.1/2/3 entries)
  3. Start ZooKeeper on each node; verify quorum forms: `echo stat | nc localhost 2181`
  4. Ensure network connectivity between ZK instances on port 2888 (peer) and 3888 (leader election)
- **Prerequisites:** Network connectivity between all nodes; no firewall blocks port 2181 (client), 2888, 3888
- **Verification:** `echo stat | nc localhost 2181` shows "Mode: leader" or "Mode: follower" on each node; quorum status shows 2-of-3 healthy
- **Owner:** Ksolves
- **Estimated Effort:** 1-2 hours
- **Critical Note:** Must complete this BEFORE proceeding to P1.2

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

### Phase 2C — Medium Priority: Configuration, Validation & Integration (P2)

### 🟡 P2.1 — Provision Remote Airflow Host (6c / 24GB / 500GB SSD)

- **Status:** OPEN
- **Priority:** MEDIUM — Dependency for orchestration (P1.4, P1.5)
- **Context:** Remote Airflow host (dedicated server or Proxmox VM) will run Apache Airflow 2.10.4, Okta (cloud-based auth), and Nginx/Ansible for cluster automation. Minimum spec: 6 vCPU, 24 GB RAM, 500 GB SSD.
- **Ksolves Actions (if provisioning is delegated):**
  1. Provision VM or bare-metal server per spec (6c / 24GB / 500GB SSD)
  2. Install RHEL 9.4, configure network, SSH, and remote access
  3. Allocate IP address and DNS A record for stable hostname
- **Or User Actions (if user provisions):**
  1. Allocate IP, provision VM on Proxmox or external cloud, DNS setup
  2. Provide Ksolves with root credentials and network details
- **Prerequisites:** IP allocation plan, DNS namespace for remote host, SSH key distribution
- **Owner:** Ksolves (if delegated) or fqdn (if provisioned by user)
- **Estimated Effort:** 2-4 hours

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

---

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
  2. *Ksolves sets up Ceph OSDs on all nodes*
  3. BLOCKER.2: User places RHEL ISO in Proxmox local storage (user action — **after** OSD configuration complete)
  4. P0.1–P0.5: Ksolves provisions all VMs and base software (requires RHEL ISO from BLOCKER.2)
  5. **P1.3: Ksolves deploys ZooKeeper ensemble** (required prerequisite)
  6. **P1.2: Ksolves deploys YARN HA** (requires P1.3 ZooKeeper to be operational first)
  7. P0.6: Run 5 sample jobs and measure actual shuffle amplification
  8. P1.4–P1.5: Ksolves deploys Nginx reverse proxy and Ansible control
  9. P2.1–P2.3: Ksolves validates remote Airflow and end-to-end pipeline
  10. Phase 2 sign-off: fqdn approves for production if all P0–P2 items pass
- **Beyond Phase 2:** Pending Ksolves clarification — See "Actions Outside Present Known Scope"

---

## REFERENCE DOCUMENTS

- **Main Report:** phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf
- **Prerequisites:** phases/phase1/Incoming/vendor_prerequisites.docx.pdf
- **Hardware Reference:** CLAUDE.md § Hardware Reference
- **Calculator:** phases/phase1/deliverables/dev_cluster_phase1_model.html
- **Ksolves Walkthrough:** phases/phase1/research/ksolves-directory-walkthrough.md
- **Vendor Questions:** phases/phase1/vendor_comms/phase1_vendor_questions.txt

---

## FOOTNOTES

¹ Apache Software Foundation, "ResourceManager High Availability," in *Apache Hadoop 3.4.1 Documentation*, accessed April 24, 2026, https://hadoop.apache.org/docs/r3.4.1/hadoop-yarn/hadoop-yarn-site/ResourceManagerHA.html. ZooKeeper is documented as a required prerequisite for YARN ResourceManager High Availability. The documentation explicitly states: "ZooKeeper is a required prerequisite for deploying YARN ResourceManager High Availability" and notes that "The RMs have an option to embed the Zookeeper-based ActiveStandbyElector to decide which RM should be the Active."

---

---

_Updated: 2026-04-24 (post-Ksolves Phase 1 completion report)_  
_Phase 1 status reflected per ksolves_april_24_process_report.txt_  
_Prepared for Review: Ready_For_Review/Phase1_Detailed_TODO.md_  
_Status: Draft — Awaiting user review before promotion to Document/_
