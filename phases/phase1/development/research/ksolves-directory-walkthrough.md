# Dev Cluster Directory Tree Structure

_Converted from: `Incoming/Ksolves Directory walk through.eml` · Date: 2026-04-22_

End-to-end walkthrough of all host, VM, and service-layer directory layouts.

---

## Sections at a Glance

| Section | Layer | Hosts / VMs |
|---|---|---|
| [A](#a-proxmox-host--bare-metal) | Proxmox Host — Bare Metal | Node01 / Node02 / Node03 |
| [B](#b-ceph-daemons--on-host-per-node) | Ceph Daemons — On Host | OSD / MON / MGR / RGW |
| [C](#c-spark-worker-vms) | Spark Worker VMs | GKPR-SPARK-WK-01 / 02 / 03 |
| [D](#d-yarn-resourcemanager-vm) | YARN ResourceManager VM | GKPR-YARN-RM-01 |
| [E](#e-remote-service-host) | Remote Service Host | Airflow · Keycloak · Spark History |
| [F](#f-ceph-rgw--s3-bucket-layout) | Ceph RGW — S3 Bucket Layout | ingest / output / spark-history |

---

## [A] Proxmox Host — Bare Metal

**Node01 / Node02 / Node03**

| Component | Value |
|---|---|
| Storage Pool | rpool (ZFS) |
| OS Drives | ZFS Mirror SSD1+SSD2 — ~480 GB usable · SSD3 = hot spare |
| Network Bond | Bond0 — 2×10G LACP |
| NIC | BCM57414 |
| Cluster Engine | Corosync + PVE |

### /etc — Configuration

```
/etc/
├── pve/
│   ├── nodes/ │ │ └── <nodename>/
│   │   ├── qemu-server/    # VM .conf files (one per VM)
│   │   └── lxc/            # LXC container configs
│   ├── storage.cfg         # Storage pool definitions (Ceph RBD, local-lvm)
│   ├── corosync.conf       # Cluster quorum & network config
│   └── user.cfg            # Proxmox users, roles, permissions
├── ceph/
│   ├── ceph.conf           # Global Ceph config (fsid, mon_host, auth)
│   └── ceph.client.admin.keyring
└── network/
    └── interfaces          # Bond0: 2×10G LACP (BCM57414 NICs)
```

### /var — Runtime State & Logs

```
/var/
├── log/
│   ├── pve/                # Proxmox API, task & cluster event logs
│   │   └── tasks/          # Per-task output (VM create/start/stop)
│   └── ceph/               # All Ceph daemon logs (OSD/MON/MGR/RGW)
└── lib/
    ├── pve/                # Proxmox runtime state & SQLite DB
    └── ceph/               # Ceph daemon working dirs
```

### /mnt & /rpool — Mount Points & ZFS Pool

```
/mnt/
└── pve/
    └── cephfs/             # CephFS mount (if enabled in future)

/rpool/                     # ZFS pool root (SSD1+SSD2 mirror)
├── ROOT/
│   └── pve-1/              # Active Proxmox OS boot environment
├── data/                   # Local thin-provisioned VM disk images
└── var-lib-vz/             # /var/lib/vz — ISO images & templates
```

---

## [B] Ceph Daemons — On Host (Per Node)

**OSD / MON / MGR / RGW — not inside any VM**

| Component | Value |
|---|---|
| OSD Count / Node | 3 (NVMe 1-2-3) |
| OSD Backend | BlueStore |
| OSD Drives | NVMe drives 1–3 — raw block, no filesystem |
| Active MGR | Node01 |
| Standby MGR | Node02 / Node03 |

### /var/lib/ceph — Daemon Working Directories

```
/var/lib/ceph/
├── osd/
│   ├── ceph-0/             # OSD 0 — NVMe drive 1 (raw BlueStore)
│   │   ├── block -> /dev/nvme0n1   # Symlink to raw NVMe block device
│   │   ├── fsid            # Cluster FSID file
│   │   ├── whoami          # OSD ID file
│   │   ├── ready           # Created when OSD is healthy
│   │   └── type            # Contains: bluestore
│   ├── ceph-1/             # OSD 1 — NVMe drive 2
│   └── ceph-2/             # OSD 2 — NVMe drive 3
├── mon/
│   └── ceph-<nodename>/    # MON DB — cluster map, CRUSH map, OSD map
│       ├── store.db/       # RocksDB: cluster state & history
│       └── keyring
├── mgr/
│   └── ceph-<nodename>/    # MGR state (active Node01, standby Node02/03)
│       └── keyring
└── radosgw/
    └── ceph-<nodename>/    # RGW (S3 gateway) state
        └── keyring
```

### /var/log/ceph — Daemon Logs

```
/var/log/ceph/
├── ceph-osd.0.log
├── ceph-osd.1.log
├── ceph-osd.2.log
├── ceph-mon.<nodename>.log         # MON log — quorum events, map changes
├── ceph-mgr.<nodename>.log         # MGR log — dashboard, metrics, health
└── ceph-client.radosgw.<nodename>.log  # RGW S3 access + error log
```

### /etc/ceph — Cluster Configuration

```
/etc/ceph/
├── ceph.conf                       # Global: fsid, mon_host, auth, OSD defaults
├── ceph.client.admin.keyring       # Admin key (restricted access)
└── ceph.client.radosgw.keyring     # RGW service key
```

---

## [C] Spark Worker VMs

**GKPR-SPARK-WK-01 / GKPR-SPARK-WK-02 / GKPR-SPARK-WK-03 — 1 VM per node**

| Component | Value |
|---|---|
| vCPU | 18 |
| RAM | 320 GB |
| OS Disk | 80 GB (Ceph RBD) |
| OS | RHEL 9.4 |
| Spark Version | 3.5.3 |
| Hadoop Version | 3.4.1 |
| Executor Cores | 8 per executor |
| Executor Memory | 28 GB per executor |
| NM vCores | 18 |
| NM Memory | 320 GB (327,680 MB) |
| Scratch (JBOD) | 4× NVMe (nvme4–nvme7) |
| Scratch Total | 4 × 3.84 TB = **15.36 TB per node** |
| Compression | Snappy / ZSTD |

### /opt — Spark & Hadoop Install

```
/opt/
├── spark/                          # Spark 3.5.3 (SPARK_HOME)
│   ├── bin/                        # spark-submit, spark-shell, spark-class
│   ├── sbin/                       # start-worker.sh, stop-worker.sh
│   ├── conf/
│   │   ├── spark-defaults.conf     # executor.cores=8, executor.memory=28g
│   │   │                           # spark.local.dir (4 NVMe paths)
│   │   │                           # io.compression.codec=snappy
│   │   │                           # parquet.compression.codec=zstd
│   │   │                           # eventLog.enabled=true
│   │   │                           # eventLog.dir=s3a://spark-history/
│   │   ├── spark-env.sh            # SPARK_HOME, HADOOP_HOME, JAVA_HOME, SPARK_LOG_DIR
│   │   └── log4j2.properties       # Logging levels
│   └── jars/
│       ├── hadoop-aws-3.4.1.jar
│       └── aws-java-sdk-bundle-*.jar
└── hadoop/                         # Hadoop 3.4.1 (HADOOP_HOME)
    ├── bin/
    ├── sbin/
    ├── etc/hadoop/
    │   ├── core-site.xml           # fs.s3a.endpoint -> Ceph RGW
    │   │                           # fs.s3a.access.key, fs.s3a.secret.key
    │   │                           # fs.s3a.path.style.access=true
    │   ├── hdfs-site.xml           # (minimal — S3A used, not HDFS)
    │   ├── yarn-site.xml           # nodemanager.resource.cpu-vcores=18
    │   │                           # nodemanager.resource.memory-mb=327680
    │   │                           # nodemanager.local-dirs (NM staging)
    │   └── workers                 # Hostnames of 3 NodeManagers
    ├── lib/native/                 # libhadoop.so — native Snappy/ZSTD libs
    └── share/hadoop/common/lib/
```

### /data — NVMe Scratch (Shuffle & Spill)

```
/data/spark/scratch/                # spark.local.dir — JBOD across 4 NVMe drives
├── nvme4/                          # XFS mount — /dev/nvme0n4 (3.84 TB)
├── nvme5/                          # XFS mount — /dev/nvme0n5 (3.84 TB)
├── nvme6/                          # XFS mount — /dev/nvme0n6 (3.84 TB)
└── nvme7/                          # XFS mount — /dev/nvme0n7 (3.84 TB)
                                    # Total: 4 × 3.84 TB = 15.36 TB per node
```

### /var — Logs & YARN Container Staging

```
/var/
├── log/
│   ├── spark/
│   │   ├── spark-worker-<hostname>-*.log
│   │   └── spark-worker-<hostname>-*.out
│   └── hadoop/yarn/
│       ├── yarn-nodemanager-<hostname>-*.log
│       └── userlogs/               # Per-executor stdout/stderr
│           └── application_<id>/container_<id>/
│               ├── stdout
│               └── stderr
└── lib/hadoop/yarn/nm-local-dir/   # YARN NM container staging
    ├── usercache/
    └── nmPrivate/
```

### /etc/fstab Entries (each Spark Worker VM)

```
/dev/nvme0n4  /data/spark/scratch/nvme4  xfs  defaults,noatime,nodiratime,largeio  0  0
/dev/nvme0n5  /data/spark/scratch/nvme5  xfs  defaults,noatime,nodiratime,largeio  0  0
/dev/nvme0n6  /data/spark/scratch/nvme6  xfs  defaults,noatime,nodiratime,largeio  0  0
/dev/nvme0n7  /data/spark/scratch/nvme7  xfs  defaults,noatime,nodiratime,largeio  0  0
```

---

## [D] YARN ResourceManager VM

**GKPR-YARN-RM-01 — Node01 only**

| Component | Value |
|---|---|
| vCPU | 2 |
| RAM | 4 GB |
| OS Disk | 40 GB (Ceph RBD) |
| OS | RHEL 9.4 |
| Max Allocation vCores | 18 |
| Max Allocation Memory | 320 GB (327,680 MB) |
| RM Recovery | Enabled |
| Scheduler | Capacity Scheduler |

### /opt/hadoop — Hadoop Install (RM-only mode)

```
/opt/hadoop/                        # Hadoop 3.4.1 (HADOOP_HOME)
├── bin/
├── sbin/                           # start-yarn.sh (starts RM only)
└── etc/hadoop/
    ├── core-site.xml               # Default FS, s3a endpoint
    ├── yarn-site.xml               # resourcemanager.hostname=<this VM IP>
    │                               # scheduler.maximum-allocation-vcores=18
    │                               # scheduler.maximum-allocation-mb=327680
    │                               # resourcemanager.recovery.enabled=true
    ├── capacity-scheduler.xml      # Queue definitions & limits
    └── workers                     # IPs of 3 Spark Worker VMs
```

### /var — Logs & State Store

```
/var/
├── log/hadoop/yarn/
│   ├── yarn-resourcemanager-<hostname>-*.log
│   └── yarn-resourcemanager-<hostname>-*.out
└── lib/hadoop/yarn/system/         # RM state store — job recovery after restart

/tmp/hadoop-yarn/staging/           # YARN staging dir for spark-submit JAR uploads
└── <username>/
```

---

## [E] Remote Service Host

**Separate Server — Airflow · Spark History Server · Keycloak · PostgreSQL**

| Component | Value |
|---|---|
| vCPU | 10c |
| RAM | 48 GB |
| Storage | 1 TB SSD |
| OS | RHEL 9.4 |
| Container Runtime | Podman / systemd |
| Airflow | 2.10.4 · CeleryExecutor |
| Spark History | 3.5.3 · port 18080 |
| Keycloak | 26.0.x · port 8443 |
| Airflow Web | port 8080 |
| Database | PostgreSQL 16.x |

### /opt/airflow — Airflow DAGs & Config

```
/opt/airflow/                       # Airflow 2.10.4 (AIRFLOW_HOME)
├── dags/
│   ├── ingest_pipeline.py          # Watches s3a://ingest/csv/ -> triggers spark-submit
│   ├── snowflake_load.py           # Parquet confirmed -> Snowflake COPY INTO
│   └── cleanup.py                  # Post-load: deletes Parquet, archives CSV on Ceph
├── plugins/
│   ├── spark_yarn_operator.py
│   └── ceph_s3a_hook.py
├── config/
│   └── airflow.cfg                 # executor=CeleryExecutor
│                                   # sql_alchemy_conn=postgresql://localhost/airflow_db
└── logs/
    └── <dag_id>/<run_id>/<task_id>/
```

### /opt/spark-history — Spark History Server

```
/opt/spark-history/                 # Spark History Server 3.5.3
├── bin/
│   └── start-history-server.sh
└── conf/
    ├── spark-defaults.conf         # spark.history.fs.logDirectory=s3a://spark-history/
    │                               # spark.history.fs.update.interval=30s
    │                               # fs.s3a.endpoint -> Ceph RGW
    └── spark-env.sh                # JAVA_HOME, history server port (18080)
```

### /opt/keycloak — Keycloak SSO

```
/opt/keycloak/                      # Keycloak 26.0.x Quarkus dist
├── bin/
│   └── kc.sh                       # ./kc.sh start --optimized
├── conf/
│   ├── keycloak.conf               # db=postgres, hostname, TLS cert paths
│   └── quarkus.properties
├── providers/
├── themes/
└── data/import/
    └── fqdn-realm.json             # Realm export — clients, roles, mappers
```

### /var/lib — Databases & Session Cache

```
/var/lib/
├── postgresql/                     # PostgreSQL 16.x data directory
│   ├── base/
│   │   ├── airflow_db/             # DAG runs, task state, XCom
│   │   └── keycloak_db/            # Realms, users, sessions, tokens
│   └── pg_wal/
└── keycloak/                       # Infinispan session cache
```

### /srv — Secrets

```
/srv/airflow/secrets/
├── ceph_s3a.json                   # s3a:// access key + secret for Ceph RGW
└── snowflake_conn.json             # Snowflake account, warehouse, credentials
```

### /etc/systemd/system — Service Units

```
/etc/systemd/system/
├── airflow-webserver.service       # port 8080
├── airflow-scheduler.service
├── airflow-worker.service          # Celery worker
├── spark-history.service           # port 18080
├── keycloak.service                # port 8443 HTTPS
└── postgresql.service
```

---

## [F] Ceph RGW — S3 Bucket Layout

_Logical layout (not filesystem paths) · Access via `s3a://<bucket>/` using Hadoop-AWS connector_

**3 RGW instances · Hadoop-AWS S3A connector**

### s3a://ingest/

```
s3a://ingest/csv/batch_YYYYMMDD_HHMMSS/*.csv
```

Raw CSV input files. One prefix per batch run. Watched by `ingest_pipeline.py` DAG which triggers `spark-submit` on new arrivals.

**~4 TB / batch**

### s3a://output/

```
s3a://output/parquet/batch_YYYYMMDD_HHMMSS/part-*.parquet
```

ZSTD-compressed Parquet output written by Spark workers. Confirmed by `snowflake_load.py` DAG before `COPY INTO Snowflake`. Deleted post-load by `cleanup.py`.

**~0.8 TB / batch**

### s3a://spark-history/

```
s3a://spark-history/application_<app_id>/*.lz4
```

LZ4-compressed Spark event logs. One prefix per job. Read by Spark History Server at port 18080. Polled every 30 seconds.

Settings: `spark.eventLog.enabled=true`, `spark.eventLog.compress=true`
