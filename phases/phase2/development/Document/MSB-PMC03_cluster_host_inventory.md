# MSB-PMC03 Cluster — Host Inventory

_Source: `lscpu`, `lsblk`, `lsmem` outputs collected 2026-04-30 from all three nodes._
_Cluster role: Spark **development** environment (YARN, Spark, Ceph, RGW S3, Spark History Server)._
_Ceph is not yet deployed (P0.0 pending) — OSD class assignments are therefore not available; data drives are listed as **Ceph OSD candidates** below._

The cluster comprises **three physical nodes** in a homogeneous Proxmox hyperconverged configuration:

- **CPU (all three nodes):** AMD EPYC 9135 (Zen 5, "Turin"), single-socket, single-NUMA, 16 cores / 32 threads, 64 MiB L3.
- **RAM:** 256 GiB per node (verified on `-02` and `-03`; see lsmem note for `-01`).
- **Storage per node:** 7× 3.5 TiB data drives (≈ 3.84 TB raw NVMe class) + 2× 447.1 GiB ZFS boot mirror members. Nodes `-02` and `-03` additionally expose a 1× 447.1 GiB NVMe device in the boot/installer slot.

> **Note on msb-pmc03-01 lsmem:** the operator's command line was `lscpu;lsblk;lscpu` (the third command was `lscpu`, not `lsmem`), so the lsmem output for this node was not captured. Re-run `lsmem` on `-01` to fill in the lsmem table below.

> **Note on residual partitions:** `sdg` on `-01` and `sdh` on `-02` carry partial partition layouts that do not match the standard Proxmox or Ceph layout — likely vendor pre-shipment test data. These should be wiped before the OSD bring-up. Additionally, `nvme0n1` on `-02` carries a full RHEL LVM (`rhel-swap`/`rhel-home`/`rhel-root`) — flagged for review; `-03`'s `nvme0n1` is unpartitioned.

---

## Table of Contents

- [msb-pmc03-01](#msb-pmc03-01)
  - [lscpu](#msb-pmc03-01-lscpu)
  - [lsblk](#msb-pmc03-01-lsblk)
  - [lsmem](#msb-pmc03-01-lsmem)
- [msb-pmc03-02](#msb-pmc03-02)
  - [lscpu](#msb-pmc03-02-lscpu)
  - [lsblk](#msb-pmc03-02-lsblk)
  - [lsmem](#msb-pmc03-02-lsmem)
- [msb-pmc03-03](#msb-pmc03-03)
  - [lscpu](#msb-pmc03-03-lscpu)
  - [lsblk](#msb-pmc03-03-lsblk)
  - [lsmem](#msb-pmc03-03-lsmem)

---

<a id="msb-pmc03-01"></a>

## msb-pmc03-01 {#msb-pmc03-01}

<a id="msb-pmc03-01-lscpu"></a>

### lscpu {#msb-pmc03-01-lscpu}

| Attribute | Value |
|---|---|
| CPU model | AMD EPYC 9135 16-Core Processor (Zen 5) |
| Base frequency | 3.65 GHz (per BogoMIPS 7288.69; lscpu did not report `CPU max MHz` on this node) |
| Min / max frequency | Not captured (frequency boost / scaling lines absent in output) |
| Sockets | 1 |
| Cores per socket | 16 |
| Threads per core | 2 |
| Logical CPUs | 32 |
| NUMA nodes | 1 (CPUs 0–31) |
| L1d / L1i cache | 768 KiB / 512 KiB (16 instances each) |
| L2 cache | 16 MiB (16 instances) |
| L3 cache | 64 MiB (4 instances) |
| Virtualization | AMD-V |

<a id="msb-pmc03-01-lsblk"></a>

### lsblk {#msb-pmc03-01-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sdb | 447.1 GiB | ZFS mirror member (1007 KiB BIOS boot, 1 GiB EFI, 446 GiB pool) |
| sdi | 447.1 GiB | ZFS mirror member (same partitioning) |

#### Data drives (Ceph OSD candidates)

| Device | Size | Notes |
|---|---|---|
| sda | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdc | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdd | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sde | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdf | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdg | 3.5 TiB | **Residual partitions present** (151.8 GiB + 1.7 TiB + 103.9 GiB ≈ 1.95 TiB used) — wipe before OSD bring-up |
| sdh | 3.5 TiB | Unpartitioned — clean OSD candidate |

#### Other volumes

_None captured — no NVMe boot/installer device present in this node's `lsblk` output (compare with `-02` and `-03`)._

<a id="msb-pmc03-01-lsmem"></a>

### lsmem {#msb-pmc03-01-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | _Not captured_ — operator's command line was `lscpu;lsblk;lscpu` (third command was `lscpu`, not `lsmem`); re-run `lsmem` on this node |
| Memory block size | _Not captured_ |

---

<a id="msb-pmc03-02"></a>

## msb-pmc03-02 {#msb-pmc03-02}

<a id="msb-pmc03-02-lscpu"></a>

### lscpu {#msb-pmc03-02-lscpu}

| Attribute | Value |
|---|---|
| CPU model | AMD EPYC 9135 16-Core Processor (Zen 5) |
| Base frequency | 3.65 GHz |
| Min / max frequency | 1.50 GHz / 3.65 GHz (frequency boost enabled; CPU scaling 98 %) |
| Sockets | 1 |
| Cores per socket | 16 |
| Threads per core | 2 |
| Logical CPUs | 32 |
| NUMA nodes | 1 (CPUs 0–31) |
| L1d / L1i cache | 768 KiB / 512 KiB (16 instances each) |
| L2 cache | 16 MiB (16 instances) |
| L3 cache | 64 MiB (4 instances) |
| Virtualization | AMD-V |

<a id="msb-pmc03-02-lsblk"></a>

### lsblk {#msb-pmc03-02-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sda | 447.1 GiB | ZFS mirror member (1007 KiB BIOS boot, 1 GiB EFI, 446 GiB pool) |
| sdb | 447.1 GiB | ZFS mirror member (same partitioning) |

#### Data drives (Ceph OSD candidates)

| Device | Size | Notes |
|---|---|---|
| sdc | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdd | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sde | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdf | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdg | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdh | 3.5 TiB | **Residual partitions present** (1.4 TiB + 17 GiB + 728.7 GiB ≈ 2.15 TiB used) — wipe before OSD bring-up |

_Only 6 data drives observed on this node (`-01` reports 7). Confirm whether the seventh data slot is depopulated or simply not enumerated here._

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| nvme0n1 | 447.1 GiB | **RHEL bare-metal install present** — partitions: `nvme0n1p1` 600 MiB, `nvme0n1p2` 1 GiB, `nvme0n1p3` 445.5 GiB containing LVM `rhel-swap` 4 GiB, `rhel-home` 371.5 GiB, `rhel-root` 70 GiB. Flag for review: this is a host-level RHEL install on the NVMe slot, not a Proxmox boot disk. |

<a id="msb-pmc03-02-lsmem"></a>

### lsmem {#msb-pmc03-02-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 256 GiB |
| Memory block size | 2 GiB |
| Memory range | 2 GiB at `0x0–0x7fffffff` (block 0) + 254 GiB at `0x100000000–0x407fffffff` (blocks 2–128) |

---

<a id="msb-pmc03-03"></a>

## msb-pmc03-03 {#msb-pmc03-03}

<a id="msb-pmc03-03-lscpu"></a>

### lscpu {#msb-pmc03-03-lscpu}

| Attribute | Value |
|---|---|
| CPU model | AMD EPYC 9135 16-Core Processor (Zen 5) |
| Base frequency | 3.65 GHz |
| Min / max frequency | 1.50 GHz / 3.65 GHz (frequency boost enabled; CPU scaling 88 %) |
| Sockets | 1 |
| Cores per socket | 16 |
| Threads per core | 2 |
| Logical CPUs | 32 |
| NUMA nodes | 1 (CPUs 0–31) |
| L1d / L1i cache | 768 KiB / 512 KiB (16 instances each) |
| L2 cache | 16 MiB (16 instances) |
| L3 cache | 64 MiB (4 instances) |
| Virtualization | AMD-V |

<a id="msb-pmc03-03-lsblk"></a>

### lsblk {#msb-pmc03-03-lsblk}

#### Proxmox boot mirror

| Device | Size | Notes |
|---|---|---|
| sda | 447.1 GiB | ZFS mirror member (1007 KiB BIOS boot, 1 GiB EFI, 446 GiB pool) |
| sdb | 447.1 GiB | ZFS mirror member (same partitioning) |

#### Data drives (Ceph OSD candidates)

| Device | Size | Notes |
|---|---|---|
| sdc | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdd | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sde | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdf | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdg | 3.5 TiB | Unpartitioned — clean OSD candidate |
| sdh | 3.5 TiB | Unpartitioned — clean OSD candidate |

_Only 6 data drives observed on this node (`-01` reports 7). Confirm whether the seventh data slot is depopulated or simply not enumerated here._

#### Other volumes

| Device | Size | Notes |
|---|---|---|
| nvme0n1 | 447.1 GiB | Unpartitioned — empty NVMe boot/installer slot |

<a id="msb-pmc03-03-lsmem"></a>

### lsmem {#msb-pmc03-03-lsmem}

| Attribute | Value |
|---|---|
| Total online memory | 256 GiB |
| Memory block size | 2 GiB |
| Memory range | 2 GiB at `0x0–0x7fffffff` (block 0) + 254 GiB at `0x100000000–0x407fffffff` (blocks 2–128) |

---

_End of inventory._
