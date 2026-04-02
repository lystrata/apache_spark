# Production Cluster — Configuration TODO

## Proxmox Host Setup (all 3 nodes)

- [ ] Install Proxmox VE on ZFS mirror (2× 480 GB SSD per node)
- [ ] Configure 3rd SSD as ZFS hot spare
- [ ] Set up dedicated Ceph cluster network (VLAN for OSD replication traffic)
- [ ] Configure ExaBGP on each node with health check against local RGW
  - Announce RGW VIP via BGP to upstream router
  - ECMP load balancing across healthy RGW instances
- [ ] Configure Proxmox HA fencing (ensure STONITH/fencing is reliable for 3-node quorum)

## Ceph Configuration

- [ ] Create 4 NVMe OSDs per node (12 OSDs total)
- [ ] Create Ceph pools:
  - `spark-s3` — RGW data pool (rep=2 or rep=3, transient ingest data)
  - `vm-rbd` — RBD pool for VM images (rep=3, HA-critical)
  - RGW metadata pools (auto-created by RGW)
- [ ] Deploy Ceph RGW (radosgw) on all 3 nodes
  - Configure S3 endpoint on port 7480
  - Create RGW user with access key / secret key for Spark
- [ ] Create S3 bucket for ingest (e.g., `raw-ingest`)
- [ ] Verify Ceph MON quorum (3 monitors, one per node)
- [ ] Set `require_osd_release` flag to match Ceph version
- [ ] Configure ExaBGP VIP for RGW S3 endpoint

## NVMe Scratch Pass-through

- [ ] Pass remaining 4 NVMe per node through to worker VMs
  - Use virtio-blk or PCI pass-through for maximum performance
  - 2 NVMe per worker VM (with 2 VMs/node)
- [ ] Inside each worker VM: format scratch NVMe as XFS/ext4, mount at `/spark/scratch`

## VM Provisioning

- [ ] Create worker VM template on Ceph RBD:
  - 24 vCPUs, 320 GB RAM
  - NUMA pinning: pin each VM to one NUMA domain
  - OS: RHEL/Rocky/Ubuntu with Java 11/17
  - Install Hadoop (YARN binaries only — no HDFS daemons)
  - Install Spark
  - Scratch NVMe mounts at `/spark/scratch`
- [ ] Clone 6 worker VMs (2 per node), NUMA-pinned:
  - Node 1: VM-1 (NUMA 0), VM-2 (NUMA 1)
  - Node 2: VM-3 (NUMA 0), VM-4 (NUMA 1)
  - Node 3: VM-5 (NUMA 0), VM-6 (NUMA 1)
- [ ] Create services VM on Ceph RBD:
  - 6 vCPUs, 16 GB RAM
  - Place on Node 1 (Proxmox HA will migrate if needed)
  - Install: YARN ResourceManager, Spark History Server, Hive Metastore, PostgreSQL

## Proxmox HA

- [ ] Add services VM to Proxmox HA group (`ha-manager add vm:<vmid> --state started`)
- [ ] Set `max_restart 3`, `max_relocate 2`
- [ ] Test failover: shut down Node 1, verify services VM restarts on Node 2 or 3
- [ ] Consider adding worker VMs to HA as well (lower priority — workers are stateless)

## YARN Configuration

- [ ] Configure `yarn-site.xml` on all worker VMs:
  - `yarn.resourcemanager.hostname` → services VM IP or DNS name
  - `yarn.nodemanager.resource.memory-mb` → (RAM_VM - 2048) MB
  - `yarn.nodemanager.resource.cpu-vcores` → (vCPUs - 2)
  - `yarn.nodemanager.local-dirs` → `/spark/scratch`
  - `yarn.nodemanager.log-dirs` → `/spark/scratch/logs`
- [ ] Start NodeManager daemon on each worker VM
- [ ] Start ResourceManager on services VM
- [ ] Verify all 6 NodeManagers register with RM (`yarn node -list`)

## Spark Configuration

- [ ] Deploy `spark-defaults.conf` to all VMs (use calculator output as base):
  - `spark.master = yarn`
  - `spark.submit.deployMode = cluster`
  - `spark.executor.cores = 5`
  - `spark.executor.memory` = (from calculator)
  - `spark.executor.memoryOverheadFactor = 0.10`
  - `spark.memory.offHeap.enabled = true`
  - `spark.memory.offHeap.size = 6g`
  - `spark.executor.instances` = (from calculator)
  - `spark.default.parallelism` = (from calculator)
  - `spark.sql.shuffle.partitions` = (from calculator)
  - `spark.sql.adaptive.enabled = true`
  - `spark.sql.adaptive.coalescePartitions.enabled = true`
  - `spark.sql.adaptive.skewJoin.enabled = true`
  - `spark.sql.parquet.compression.codec = snappy`
  - `spark.hadoop.fs.s3a.endpoint = https://<rgw-vip>:7480`
  - `spark.hadoop.fs.s3a.path.style.access = true`
  - `spark.hadoop.fs.s3a.access.key = <rgw-access-key>`
  - `spark.hadoop.fs.s3a.secret.key = <rgw-secret-key>`
  - `spark.local.dir = /spark/scratch`
  - `spark.yarn.maxAppAttempts = 2`
- [ ] Configure Spark History Server on services VM:
  - `spark.history.fs.logDirectory = s3a://spark-logs/`
  - Port: 18080
- [ ] Configure `spark-env.sh`:
  - `SPARK_LOG_DIR`, `SPARK_LOCAL_DIRS`, `HADOOP_CONF_DIR`

## Hive Metastore

- [ ] Install PostgreSQL on services VM
- [ ] Create `metastore` database and user
- [ ] Configure `hive-site.xml`:
  - `javax.jdo.option.ConnectionURL` → PostgreSQL JDBC URL
  - `hive.metastore.warehouse.dir` → `s3a://warehouse/`
- [ ] Initialize schema: `schematool -dbType postgres -initSchema`
- [ ] Start Hive Metastore service (port 9083)

## Networking / Access

- [ ] Assign stable DNS name or ExaBGP VIP to services VM for user access
- [ ] Assign ExaBGP VIP for RGW S3 endpoint
- [ ] Verify `spark-submit` works from services VM:
  ```
  spark-submit --master yarn --deploy-mode cluster test_job.py
  ```
- [ ] Verify S3 access from worker VMs:
  ```
  aws --endpoint-url=https://<rgw-vip>:7480 s3 ls s3://raw-ingest/
  ```

## Validation & Smoke Tests

- [ ] Run a test Spark job that reads CSV from S3, transforms, writes Parquet back to S3
- [ ] Verify Spark History Server UI shows completed job (http://<svc-vm>:18080)
- [ ] Verify YARN ResourceManager UI shows all 6 NodeManagers (http://<svc-vm>:8088)
- [ ] Check shuffle spill goes to NVMe scratch (not Ceph)
- [ ] Simulate node failure: stop Node 1, verify:
  - Proxmox HA restarts services VM on another node
  - Worker VMs on other nodes continue accepting jobs
  - Ceph remains healthy (degraded but available)
- [ ] Run daily ingest volume test (2 TB) end-to-end through to Snowflake

## Ongoing Operations

- [ ] Set up Ceph S3 lifecycle policy to purge objects older than 2 days
- [ ] Configure Snowflake COPY INTO pipeline from S3 bucket
- [ ] Set up monitoring: Ceph dashboard, YARN metrics, Spark metrics
- [ ] Document runbook for common failure scenarios
