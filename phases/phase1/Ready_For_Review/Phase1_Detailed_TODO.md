# Phase 1 Detailed TODO — fqdn Development Cluster

_Expanded from fqdn Phase 1 Report (Ksolves) — April 2026_
_Source: phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf_

---

## CRITICAL PATH — MUST COMPLETE BEFORE PHASE 1 VALIDATION

### 🔴 P0.1 — Worker VM vCPU Configuration Fix
- **Status:** OPEN
- **Priority:** CRITICAL — Blocking Phase 1 concurrency
- **Context:** Current Worker VMs are configured at 14 vCPU; Phase 1 requires 18 vCPU (8-core executor + 4-core driver + 6-core buffer). Gap analysis shows -4c per VM cluster-wide.
- **Action Required:** Increase Worker VM vCPU allocation from 14 → 18 vCPU on all three nodes (Node01, Node02, Node03). This is a Proxmox configuration edit only; no hardware changes needed.
- **Implementation:** Edit GKPR-SPARK-WK-01, GKPR-SPARK-WK-02, GKPR-SPARK-WK-03 VM configurations in Proxmox
- **Verification:** After change, cluster has 48c effective available (~16c per node after 12c infrastructure reservation)
- **Owner:** infrastructure/proxmox team
- **Estimated Effort:** < 1 hour

### 🔴 P0.2 — Run 40-Job Concurrent Load Test (Phase 1 SLA Validation)
- **Status:** OPEN
- **Priority:** CRITICAL — Validates all Phase 1 assumptions and configurations
- **Context:** Phase 1 requires supporting 40 concurrent jobs (midpoint = 35 jobs/day, upper bound = 40). Current cluster sizing assumes this workload. SLA is 4 hours for batch completion (1 TB/hr throughput). Gap analysis shows tight 2.1 min buffer at 40 jobs; Phase 1 report flags as CRITICAL.
- **Action Required:** Execute full end-to-end test with 40 concurrent Spark jobs, each processing ~100 GB (upper bound scenario). Measure actual execution time, shuffle amplification, Ceph RGW throughput, WAN egress, and OOM behavior.
- **Expected Outcome:** 
  - Actual job duration should be ~6.0 min (currently modeled at 6.8 min)
  - Shuffle amplification factor (actual vs. 7× assumption)
  - Memory utilization under peak load
  - Ceph S3A throughput ceiling
- **Blocker:** This test must pass before Phase 1 sign-off; if it fails, Phase 1 node addition becomes mandatory
- **Owner:** qa/performance team
- **Estimated Effort:** 2-4 hours (includes job setup, execution, teardown, analysis)

### 🔴 P0.3 — Confirm Cloud Staging Target (Azure Blob vs AWS S3)
- **Status:** OPEN
- **Priority:** CRITICAL — Blocks egress pipeline design
- **Context:** Phase 1 data flow (Stage 6) transfers Parquet output from Ceph RGW to cloud staging for Snowflake COPY INTO. Must know target platform to finalize egress networking and credentials.
- **Required Decision:** Azure Blob Storage or AWS S3?
- **Impact:** Determines IAM/SAS token configuration, network routing (exaBGP floating IP routing to Snowflake), and Snowflake COPY command syntax
- **Owner:** data-platform/snowflake team
- **Deadline:** Before Phase 1 pipeline validation (P0.6)

### 🔴 P0.4 — Validate RHEL 9.4 Subscriptions on All VMs
- **Status:** OPEN
- **Priority:** CRITICAL — Blocking package installation and OS patching
- **Context:** Phase 1 assumes RHEL 9.4 on all Worker VMs and remote Ansible control node. Active subscriptions required for yum package installation, security patches, and OpenShift/Kubernetes support.
- **Action Required:** Confirm Red Hat subscription status on:
  - GKPR-SPARK-WK-01, GKPR-SPARK-WK-02, GKPR-SPARK-WK-03 (Spark Worker VMs)
  - GKPR-YARN-RM-01 (YARN ResourceManager VM)
  - Remote Airflow host (if RHEL-based)
- **Verification:** `subscription-manager list` should show active subscription; yum install should succeed
- **Owner:** infrastructure/rhel-licensing team
- **Estimated Effort:** < 1 hour

### 🔴 P0.5 — Install Hadoop 3.4.1 on All Worker VMs
- **Status:** OPEN
- **Priority:** CRITICAL — Spark requires standalone Hadoop installation
- **Context:** Spark 3.5.3 does not bundle Hadoop; must install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME. Phase 1 depends on this for HDFS access, even though we use Ceph S3A.
- **Action Required:** 
  1. Download and install Hadoop 3.4.1 on GKPR-SPARK-WK-01/02/03
  2. Set HADOOP_HOME environment variable (e.g., /opt/hadoop-3.4.1)
  3. Update spark-defaults.conf to reference Hadoop libs
  4. Verify with `hadoop version` on each node
- **Verification:** spark-submit should resolve Hadoop classes without errors
- **Owner:** infrastructure/hadoop-setup team
- **Estimated Effort:** 1-2 hours per node (3-6 hours total)

---

## HIGH PRIORITY — PHASE 1 INFRASTRUCTURE DEPLOYMENT

### 🟠 P1.1 — Deploy Spark History Server on Node02
- **Status:** OPEN
- **Priority:** HIGH — Phase 1 diagnostic and observability
- **Context:** Spark History Server (GKPR-SPARK-HS-01) runs on Node02 with 1 vCPU / 4 GB RAM. Reads event logs from s3a://spark-history/ on Ceph RGW. Required for job monitoring and debugging during Phase 1 runs.
- **Configuration:** Spark 3.5.3, 1c/4GB, reads event logs from s3a://spark-history/ path on Ceph RGW
- **Prerequisites:** Ceph RGW must have spark-history S3 bucket created and readable
- **Owner:** devops/spark-infrastructure team
- **Estimated Effort:** 1-2 hours

### 🟠 P1.2 — Deploy YARN ResourceManager HA (Active/Standby)
- **Status:** OPEN
- **Priority:** HIGH — Phase 1 cluster stability requirement
- **Context:** YARN ResourceManager runs as VM on Node01 (active) with standby on Node03. Requires ZooKeeper ensemble and Nginx reverse proxy for stable endpoint. Phase 1 assumes HA for unattended overnight batch runs.
- **Configuration:**
  - GKPR-YARN-RM-01 (Node01, active): 2 vCPU / 4 GB
  - GKPR-YARN-RM-02 (Node03, standby): 2 vCPU / 4 GB
  - ZooKeeper quorum (1 per node, 3 total)
  - Nginx reverse proxy on remote Airflow host
- **Prerequisites:** ZooKeeper (P1.3) and Nginx (P1.4) must be deployed first
- **Owner:** devops/yarn-ha team
- **Estimated Effort:** 2-3 hours

### 🟠 P1.3 — Deploy ZooKeeper Ensemble for YARN RM Failover
- **Status:** OPEN
- **Priority:** HIGH — Dependency for YARN HA
- **Context:** ZooKeeper ensemble (1 instance per node) coordinates YARN ResourceManager failover. Paxos quorum requires 2-of-3 agreement for cluster decisions.
- **Configuration:** 1 ZooKeeper process per node (Node01, Node02, Node03). Can run on host or in small VM.
- **Prerequisites:** Network connectivity between all nodes required
- **Owner:** devops/zookeeper team
- **Estimated Effort:** 1-2 hours

### 🟠 P1.4 — Deploy Nginx Reverse Proxy on Remote Airflow Host
- **Status:** OPEN
- **Priority:** HIGH — Provides stable YARN RM endpoint for HA
- **Context:** Nginx acts as reverse proxy for YARN ResourceManager HA, providing stable single endpoint for YARN RM web UI (port 8088) and client routing (port 8032). Ensures client connectivity regardless of which node is currently active.
- **Configuration:** 
  - Upstream targets: Node01:8088 (active), Node03:8088 (standby)
  - Health checks every 30s
  - Failover latency: ~30s on detection
- **Prerequisites:** Remote Airflow host must be provisioned (P2.1)
- **Owner:** devops/nginx team
- **Estimated Effort:** 1-2 hours

### 🟠 P1.5 — Deploy Ansible Control Node on Remote Airflow Host
- **Status:** OPEN
- **Priority:** HIGH — Required for infrastructure automation
- **Context:** Ansible control node on remote Airflow host enables programmatic cluster management, configuration updates, and orchestration. Must have SSH key access and Proxmox API token for VM lifecycle operations.
- **Configuration:**
  - Ansible 2.10+
  - SSH key configured for passwordless access to all cluster nodes
  - Proxmox API token stored securely (pass, vault, or secrets manager)
  - Playbooks installed from git repository
- **Prerequisites:** Remote Airflow host must be provisioned; SSH keys must be distributed to cluster nodes
- **Owner:** devops/ansible team
- **Estimated Effort:** 1-2 hours

### 🟠 P1.6 — Monitor Ceph OSD Memory Under Peak Ingest
- **Status:** OPEN
- **Priority:** HIGH — Critical for storage stability
- **Context:** Phase 1 assumes 3 GB per OSD (conservative default osd_memory_target=4GB per Ksolves). Must monitor actual memory consumption under peak 4 TB/batch ingest load. If OSD memory exceeds headroom, increase osd_memory_target.
- **Action Required:** 
  1. Configure Grafana dashboard for Ceph OSD memory metrics
  2. Run Phase 1 load test (P0.2) and capture OSD memory peaks
  3. If peak > 3GB, increase osd_memory_target incrementally and re-test
- **Success Criteria:** OSD memory < 3.5 GB peak during 4 TB batch
- **Owner:** ops/ceph-monitoring team
- **Estimated Effort:** 1-2 hours (monitoring setup) + data collection during P0.2

### 🟠 P1.7 — Validate WAN Egress Throughput (1 Gbps Target)
- **Status:** OPEN
- **Priority:** HIGH — Critical for cloud staging speed
- **Context:** Phase 1 assumes 1 Gbps (≈125 MB/s) outbound throughput from cluster to cloud staging (Azure/AWS). Must validate actual achievable throughput with Parquet transfers during Phase 1 runs.
- **Action Required:** 
  1. Measure actual throughput during Stage 6 (cloud egress) of Phase 1 load test
  2. Monitor exaBGP floating IP routing to Snowflake egress point
  3. Check for packet loss, latency anomalies
- **Success Criteria:** Sustained ≥100 MB/s during Parquet transfer; no packet loss
- **Owner:** infrastructure/network team
- **Estimated Effort:** 1-2 hours (measurement during P0.2)

---

## MEDIUM PRIORITY — PHASE 1 CONFIGURATION & VALIDATION

### 🟡 P2.1 — Provision Remote Airflow Host (6c / 24GB / 500GB SSD)
- **Status:** OPEN
- **Priority:** MEDIUM — Dependency for orchestration
- **Context:** Remote Airflow host (dedicated server or Proxmox VM) runs Apache Airflow 2.10.4, Okta (cloud-based), and Nginx/Ansible. Minimum spec: 6 vCPU, 24 GB RAM, 500 GB SSD (OS + 200GB Airflow logs/DB).
- **Hardware Options:**
  - Proxmox VM (if spare capacity available)
  - Dedicated bare-metal server
  - Cloud VM (GCP Compute Engine, Azure VM, AWS EC2)
- **Prerequisites:** IP allocation, DNS A record, SSH key distribution
- **Owner:** infrastructure/remote-services team
- **Estimated Effort:** 2-4 hours (provisioning + basic setup)

### 🟡 P2.2 — Deploy Apache Airflow 2.10.4 on Remote Host
- **Status:** OPEN
- **Priority:** MEDIUM — Phase 1 job orchestration
- **Context:** Airflow triggers spark-submit via DAG scheduler. CeleryExecutor confirmed for multi-node distributed execution. Embedded PostgreSQL (embedded in docker-compose) or standalone database.
- **Configuration:**
  - Version: 2.10.4
  - Executor: CeleryExecutor
  - Database: PostgreSQL (100 GB OS + 200 GB logs/DB storage)
  - DAG: References Spark job submissions to YARN RM via Nginx endpoint
- **Prerequisites:** Python 3.11+, pip, Docker/Compose or native install
- **Owner:** devops/airflow team
- **Estimated Effort:** 2-3 hours

### 🟡 P2.3 — Validate Data Flow Pipeline (8-Stage ETL)
- **Status:** OPEN
- **Priority:** MEDIUM — End-to-end integration test
- **Context:** Phase 1 data flow spans 8 sequential stages from CSV ingest through Snowflake COPY. Each stage has specific requirements (Airflow DAG, Spark containers, S3A reads/writes, cloud staging).
- **Stages to Validate:**
  1. CSV Ingest → Ceph RGW (s3a://ingest/csv/)
  2. Airflow DAG trigger via Airflow scheduler
  3. YARN container scheduling
  4. Spark ETL execution (CSV → Parquet, Snappy compression)
  5. Parquet writes to Ceph RGW (s3a://output/parquet/)
  6. Cloud egress to Azure Blob / AWS S3
  7. Snowflake COPY INTO (internal stage)
  8. Cleanup gate (delete Parquet from Ceph after Snowflake confirmation)
- **Verification:** Single job run with 4 TB sample CSV → complete pipeline → confirm in Snowflake
- **Owner:** data-engineering/etl team
- **Estimated Effort:** 3-4 hours (test design + execution + validation)

### 🟡 P2.4 — Confirm Compression Codec Configuration
- **Status:** OPEN
- **Priority:** MEDIUM — Performance and storage optimization
- **Context:** Phase 1 specifies Snappy for shuffle intermediates (2.5× compression ratio, low CPU) and ZSTD for Parquet output (5× compression ratio, higher CPU). Must validate codec performance under full load.
- **Configuration:** In spark-defaults.conf:
  ```
  spark.shuffle.compress=true
  spark.shuffle.spill.compress=true
  spark.io.compression.codec=snappy
  spark.sql.parquet.compression.codec=zstd
  ```
- **Validation:** Monitor CPU usage, compression ratio, and throughput during Phase 1 load test
- **Owner:** infrastructure/spark-config team
- **Estimated Effort:** < 1 hour (config validation + load test observation)

### 🟡 P2.5 — Validate JBOD Storage Configuration (NVMe drives 4-7)
- **Status:** OPEN
- **Priority:** MEDIUM — Critical for shuffle performance
- **Context:** NVMe drives 4-7 (15.36 TB per node) are configured as JBOD (not RAID) for Spark shuffle scratch. Phase 1 assumes ephemeral data (no replication). Must confirm mount paths, permissions, and I/O performance.
- **Configuration:**
  - Mount point: /var/spark/scratch (or equivalent per node)
  - Filesystem: XFS (recommended for parallel I/O)
  - Permissions: Spark process user (root or dedicated spark user)
  - Expected I/O: ~3,000 MB/s per drive (combined peak across cluster)
- **Validation:** `fio` benchmarking during Phase 1 load test; monitor for I/O bottlenecks
- **Owner:** infrastructure/storage-config team
- **Estimated Effort:** 1-2 hours (mount setup + benchmark)

### 🟡 P2.6 — Validate Network Topology (2×10G LACP Bond)
- **Status:** OPEN
- **Priority:** MEDIUM — Ensures cluster bandwidth availability
- **Context:** Each node has 2×10G NICs bonded via LACP (Link Aggregation Control Protocol). Phase 1 requires 20G per node effective bandwidth for intra-cluster replication, S3A reads/writes, and WAN egress.
- **Validation Points:**
  - Bond status: `cat /proc/net/bonding/bond0` on each node
  - Ceph replication: Should saturate 13× over 95 MB/s/node (Ceph internal target)
  - S3A throughput: 4× over 284 MB/s (aggregate Ceph RGW ceiling)
  - Packet loss: 0 under sustained load
- **Owner:** infrastructure/network team
- **Estimated Effort:** 1-2 hours (validation during P0.2 load test)

---

## LOWER PRIORITY — POST-PHASE-1 ITEMS

### 🔵 P3.1 — Evaluate Phase 1 Node Addition Timeline
- **Status:** OPEN
- **Priority:** LOW (Planning for Phase 2)
- **Context:** Phase 1 report flags 40-job SLA as "marginal with 2.1 min buffer." Phase 2 requires 4+ nodes to support 60+ jobs. Timeline decision: add 4th node before Phase 1 production runs or wait for Phase 2 go-live?
- **Decision Required:** Add 1× HPE DL385 Gen11 node now (4 nodes total, Phase 1 revised) or defer to Phase 2?
- **Owner:** management/capacity-planning team

### 🔵 P3.2 — Document Phase 1 As-Built Architecture
- **Status:** OPEN
- **Priority:** LOW (Documentation & handoff)
- **Context:** Create final as-built documentation for Phase 1 cluster showing actual configurations, tuning parameters, and lessons learned. Feed into Phase 2 design.
- **Deliverables:** Updated CLAUDE.md, deployment playbooks, runbooks, known issues
- **Owner:** documentation/devops team

---

## ASSUMPTIONS & DEPENDENCIES

**Key Assumptions from Ksolves Phase 1 Report:**
- Shuffle amplification: 7× (uncompressed) — actual measurement needed (P0.2)
- Concurrent jobs: 1 → 2 with Phase 1 (core-bound, not RAM-bound)
- WAN egress: 1 Gbps sustained (125 MB/s actual target)
- Cloud staging: Azure Blob or AWS S3 (TBD, P0.3)
- RHEL 9.4: Active subscriptions on all VMs (P0.4)
- Hadoop: 3.4.1 standalone (P0.5)

**External Dependencies:**
- Ksolves technical contact: Karthik Hegde (karthik.hegde@ksolves.com, 8317382875)
- fqdn sign-off required before Phase 1 production run
- Cloud staging platform decision blocks Stage 6 implementation

---

## REFERENCE DOCUMENTS

- **Main Report:** phases/phase1/Incoming/fqdn Report Phase 1 (Updated).docx.pdf
- **Prerequisites:** phases/phase1/Incoming/vendor_prerequisites.docx.pdf
- **Hardware Reference:** CLAUDE.md § Hardware Reference
- **Calculator:** phases/phase1/deliverables/dev_cluster_phase1_model.html
- **Ksolves Walkthrough:** phases/phase1/research/ksolves-directory-walkthrough.md

---

_Prepared for Review: Ready_For_Review/Phase1_Detailed_TODO.md_
_Status: Draft — Awaiting user review before promotion to Document/_
