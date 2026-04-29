# MSB-PMC01 Cluster — Host Inventory

_Source: `lscpu`, `lsblk`, `lsmem` outputs collected 2026-04-29 from all four nodes._
_Kernel observed on msb-pmc01-03: `Linux 6.8.12-20-pve` (Proxmox VE)._
_OSD class assignments are taken from `ceph osd df tree` (see `phases/phase2/development/Incoming/PMC01_OSD_Tree/`)._

The cluster comprises **four physical nodes** in a hyperconverged Proxmox + Ceph configuration. Hardware is heterogeneous, with two CPU tiers:

- **Tier A (Xeon Gold 6136):** msb-pmc01-01, msb-pmc01-04 — single-socket, single-NUMA, 130 GB RAM.
- **Tier B (Xeon Silver 4210R):** msb-pmc01-02, msb-pmc01-03 — dual-socket, dual-NUMA, 162 GB RAM.

Ceph runs two OSD device cpolasses:

- `hdd` — 838 GiB and 1.1 TiB drives (bulk storage pool).
- `rbd_ssd` — 894 GiB drives (dedicated SSD pool for VM block storage).

---

## Table of Contents

- [msb-pmc01-01](#msb-pmc01-01)
  - [lscpu](#msb-pmc01-01-lscpu)
  - [lsblk](#msb-pmc01-01-lsblk)
  - [lsmem](#msb-pmc01-01-lsmem)
- [msb-pmc01-02](#msb-pmc01-02)
  - [lscpu](#msb-pmc01-02-lscpu)
  - [lsblk](#msb-pmc01-02-lsblk)
  - [lsmem](#msb-pmc01-02-lsmem)
- [msb-pmc01-03](#msb-pmc01-03)
  - [lscpu](#msb-pmc01-03-lscpu)
  - [lsblk](#msb-pmc01-03-lsblk)
  - [lsmem](#msb-pmc01-03-lsmem)
- [msb-pmc01-04](#msb-pmc01-04) — _Airflow VM target (P1.0)_
  - [lscpu](#msb-pmc01-04-lscpu)
  - [lsblk](#msb-pmc01-04-lsblk)
  - [lsmem](#msb-pmc01-04-lsmem)

---

<a id="msb-pmc01-01"></a>

## msb-pmc01-01 {#msb-pmc01-01}

<a id="msb-pmc01-01-lscpu"></a>

### lscpu {#msb-pmc01-01-lscpu}

| Attribute | Value |
|---|---|
| CPU model | Intel Xeon Gold 6136 (Skylake-SP) |
| Base frequency | 3.00 GHz |
| Min / max frequency | 1.20 GHz / 3.70 GHz |
| Sockets | 1 |
| Cores per socket | 12 |
| Threads per core | 2 |
| Logical CPUs | 24 |
| NUMA nodes | 1 (CPUs 0–23) |
| L3 cache | 24.8 MiB (1 instance) |

<a id="msb-pmc01-01-lsblk"></a>

### lsblk {#msb-pmc01-01-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sde | 447.1 GiB | ZFS mirror member (1 MiB BIOS boot, 1 GiB EFI/boot, 446 GiB pool) |
| sdf | 447.1 GiB | ZFS mirror member (same partitioning) |

#### Ceph OSDs

| Device | Size | OSD ID | Class |
|---|---|---|---|
| sda | 838.3 GiB | osd.2 | hdd |
| sdb | 838.3 GiB | osd.3 | hdd |
| sdc | 838.3 GiB | osd.4 | hdd |
| sdd | 1.1 TiB | osd.5 | hdd |
| sdg | 894.2 GiB | osd.0 | rbd_ssd |
| sdh | 894.2 GiB | osd.1 | rbd_ssd |

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| sdi | 0 B | Reserved drive bay (no disk present) |
| zd0 | 50 GiB | ZFS volume (49.9 GiB + 4 MiB + 106 MiB partitions — pattern matches an active Linux VM root disk) |
| zd16 | 4 MiB | Small ZFS volume |
| rbd0 | 64 GiB | Active Ceph RBD volume |

<a id="msb-pmc01-01-lsmem"></a>

### lsmem {#msb-pmc01-01-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 130 GiB |
| Memory block size | 2 GiB |

---

<a id="msb-pmc01-02"></a>

## msb-pmc01-02 {#msb-pmc01-02}

<a id="msb-pmc01-02-lscpu"></a>

### lscpu {#msb-pmc01-02-lscpu}

| Attribute | Value |
|---|---|
| CPU model | Intel Xeon Silver 4210R (Cascade Lake) |
| Base frequency | 2.40 GHz |
| Min / max frequency | 1.00 GHz / 3.20 GHz |
| Sockets | 2 |
| Cores per socket | 10 |
| Threads per core | 2 |
| Logical CPUs | 40 |
| NUMA nodes | 2 (node0: CPUs 0–9, 20–29 · node1: CPUs 10–19, 30–39) |
| L3 cache | 27.5 MiB (2 instances, one per socket) |

<a id="msb-pmc01-02-lsblk"></a>

### lsblk {#msb-pmc01-02-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sde | 447.1 GiB | ZFS mirror member |
| sdf | 447.1 GiB | ZFS mirror member |

#### Ceph OSDs

| Device | Size | OSD ID | Class |
|---|---|---|---|
| sda | 838.3 GiB | osd.8 | hdd |
| sdb | 838.3 GiB | osd.9 | hdd |
| sdc | 1.1 TiB | osd.10 | hdd |
| sdd | 1.1 TiB | osd.11 | hdd |
| sdg | 894.2 GiB | osd.6 | rbd_ssd |
| sdh | 894.2 GiB | osd.7 | rbd_ssd |

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| sdi | 0 B | Reserved drive bay |
| rbd0 | 1 TiB | Active Ceph RBD volume (1024 GiB partition) |

<a id="msb-pmc01-02-lsmem"></a>

### lsmem {#msb-pmc01-02-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 162 GiB |
| Memory block size | 2 GiB |

---

<a id="msb-pmc01-03"></a>

## msb-pmc01-03 {#msb-pmc01-03}

<a id="msb-pmc01-03-lscpu"></a>

### lscpu {#msb-pmc01-03-lscpu}

| Attribute | Value |
|---|---|
| CPU model | Intel Xeon Silver 4210R (Cascade Lake) |
| Base frequency | 2.40 GHz |
| Min / max frequency | 1.00 GHz / 3.20 GHz |
| Sockets | 2 |
| Cores per socket | 10 |
| Threads per core | 2 |
| Logical CPUs | 40 |
| NUMA nodes | 2 (node0: CPUs 0–9, 20–29 · node1: CPUs 10–19, 30–39) |
| L3 cache | 27.5 MiB (2 instances, one per socket) |

<a id="msb-pmc01-03-lsblk"></a>

### lsblk {#msb-pmc01-03-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sde | 447.1 GiB | ZFS mirror member |
| sdf | 447.1 GiB | ZFS mirror member |

#### Ceph OSDs

| Device | Size | OSD ID | Class |
|---|---|---|---|
| sda | 838.3 GiB | osd.14 | hdd |
| sdb | 838.3 GiB | osd.15 | hdd |
| sdc | 838.3 GiB | osd.16 | hdd |
| sdd | 1.1 TiB | osd.17 | hdd |
| sdg | 894.2 GiB | osd.12 | rbd_ssd |
| sdh | 894.2 GiB | osd.13 | rbd_ssd |

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| sdi | 0 B | Reserved drive bay |
| rbd0 | 1 TiB | Active Ceph RBD volume (1024 GiB partition) |

<a id="msb-pmc01-03-lsmem"></a>

### lsmem {#msb-pmc01-03-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 162 GiB |
| Memory block size | 2 GiB |

---

<a id="msb-pmc01-04"></a>

## msb-pmc01-04 {#msb-pmc01-04}

_Designated host for the Airflow VM (P1.0). No active production VMs at the time of inventory; only Proxmox VE and Ceph daemons (MON/MGR/OSDs) are running._

<a id="msb-pmc01-04-lscpu"></a>

### lscpu {#msb-pmc01-04-lscpu}

| Attribute | Value |
|---|---|
| CPU model | Intel Xeon Gold 6136 (Skylake-SP) |
| Base frequency | 3.00 GHz |
| Min / max frequency | 1.20 GHz / 3.70 GHz |
| Sockets | 1 |
| Cores per socket | 12 |
| Threads per core | 2 |
| Logical CPUs | 24 |
| NUMA nodes | 1 (CPUs 0–23) |
| L3 cache | 24.8 MiB (1 instance) |

<a id="msb-pmc01-04-lsblk"></a>

### lsblk {#msb-pmc01-04-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sda | 447.1 GiB | ZFS mirror member |
| sdb | 447.1 GiB | ZFS mirror member |

#### Ceph OSDs

| Device | Size | OSD ID | Class |
|---|---|---|---|
| sdc | 894.3 GiB | osd.18 | rbd_ssd |
| sdd | 894.3 GiB | osd.19 | rbd_ssd |
| sde | 838.4 GiB | osd.22 | hdd |
| sdf | 838.4 GiB | osd.21 | hdd |
| sdg | 838.4 GiB | osd.20 | hdd |
| sdh | 1.1 TiB | osd.23 | hdd |

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| sdi | 0 B | Reserved drive bay |
| sdj | 512 MiB read-only | Virtual media (likely BMC/iLO mount) |
| zd0 | 64 GiB | Proxmox-internal ZFS volume (1 MiB + 1 GiB + 63 GiB partitions) |

<a id="msb-pmc01-04-lsmem"></a>

### lsmem {#msb-pmc01-04-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 130 GiB |
| Memory block size | 2 GiB |

---

_End of inventory._
