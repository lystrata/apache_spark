---
name: spark-production-cluster
description: >
  Context and reference material for the Proxmox/Spark Production Cluster project.
  A 3-node hyperconverged cluster running Ceph RGW (S3), YARN, and Apache Spark
  for daily ETL ingest (2 TB/day) to Snowflake. Use this skill when discussing
  the production cluster architecture, calculator, VM layout, storage model,
  YARN configuration, Spark tuning, Ceph sizing, or implementation tasks.
  Also use when the user references the production cluster calculator, the
  development cluster calculator, or any related infrastructure planning.
---

# Spark Production Cluster

## Project Overview

3-node Proxmox hyperconverged cluster running:
- Ceph RGW (S3-compatible object store) for ingest staging
- Ceph RBD for VM images (enables Proxmox HA + live migration)
- YARN as the Spark resource manager (no Kubernetes, no HDFS)
- Apache Spark for daily ETL: CSV ingest → Parquet → Snowflake
- ExaBGP for RGW VIP (BGP-announced, ECMP load balanced)

## Key Architecture Decisions

See [references/architecture.md](references/architecture.md) for design decisions.

## Calculator

Two calculator versions in `/Users/rohn/Serve/`:
- `spark_calculator_v1.html` — frozen v1 (original storage model)
- `spark_calculator.html` — v2 production (current)

See [references/manual.md](references/manual.md) for the calculator user guide.

## Implementation TODO

See [references/todo.md](references/todo.md) for the implementation checklist.

## Hardware Per Node

- 64 cores (2× 32c CPUs), 728 GB RAM, 2 NUMA domains
- 3× 480 GB SSD (ZFS mirror for Proxmox OS + 1 spare)
- 8× 3.2 TB NVMe (default: 4 Ceph OSDs + 4 local scratch)

## VM Layout (default settings)

- Node 1: 2 worker VMs (24 vCPU, 320 GB each) + 1 services VM (6 vCPU, 16 GB)
- Node 2: 2 worker VMs
- Node 3: 2 worker VMs
- Services VM protected by Proxmox HA (auto-restart on surviving node)
- Each worker VM runs a YARN NodeManager (2c + 2 GB reserved)
