# MSB-PMC04 Cluster Profile — Hardware & Network Capacity

_Version 1.0 · 2026-05-13_
_For: Ksolves implementation team (Phase 3 preparation)_
_Prepared by: fqdn infrastructure (cluster owner)_
_Status: **Draft for fqdn internal review**. Once approved, promote to `phases/development/phase3/Document/` and circulate to Ksolves._
_Source: `phases/development/phase3/Notes/pmc04_cluster_profile_2026-05-13.xlsx`_

---

## Summary

| Attribute | Value |
|-----------|-------|
| Cluster name | `msb-pmc04` |
| Type | Single Proxmox cluster, single membership |
| Physical nodes | 6 |
| Purpose | Supports `msb-pmc02` (production Spark) and `msb-pmc03` (development Spark) |
| Node network | VLAN 37 (10.1.37.0/24) |
| Workload-VM network | VLAN 27 (10.1.27.0/24) |

**Scope of this document:** hardware and network infrastructure capacity only. Workload allocation (which VMs run where, packaging into monolithic vs split VMs, Ceph pool/RGW tenancy topology) is Ksolves' design decision and is **not** covered here.

**One-line topology:** _Nodes on VLAN 37; workload VMs on VLAN 27._

---

## Hardware Inventory

All capacities in GigaBytes (GB) unless noted. "OSD raw" is the raw block-device capacity each node contributes to the cluster's Ceph layer.

### Per-node detail

All 6 nodes are racked as of 2026-05-13. _PubIP_ values shown as `TBD` are pending Sean's assignment on the 10/25 Gb interface.

| Node | RAM | ZFS (boot) | OSD layout | OSD raw | iLO | PubIP |
|------|-----|------------|------------|---------|-----|-------|
| msb-pmc04-01 | 160 GB | 3 × 600 GB | 5 × 1200 GB | 6 000 GB | 10.1.32.162 | &nbsp;&nbsp;TBD |
| msb-pmc04-02 | 160 GB | 3 × 600 GB | 3 × 1200 + 5 × 900 GB | 8 100 GB | 10.1.32.199 | &nbsp;&nbsp;TBD |
| msb-pmc04-03 | 160 GB | 3 × 600 GB | 5 × 1200 GB | 6 000 GB | 10.1.32.172 | &nbsp;&nbsp;TBD |
| msb-pmc04-04 | 160 GB | 3 × 600 GB | 3 × 1200 + 5 × 900 GB | 8 100 GB | 10.1.32.232 | &nbsp;&nbsp;TBD |
| msb-pmc04-05 |  96 GB | 3 × 600 GB | 21 × 1200 GB | 25 200 GB | &nbsp;&nbsp;TBD | &nbsp;&nbsp;TBD |
| msb-pmc04-06 | 128 GB | 3 × 300 GB | 17 × 1200 + 4 × 900 GB | 21 300 GB | 10.1.32.58 | 10.1.37.58 |

### Cluster totals

| Metric | Value |
|--------|-------|
| Nodes | 6 |
| Total RAM | 864 GB |
| Total ZFS (boot pool) | ~9.9 TB |
| Total OSD raw (contributes to cluster Ceph) | **74.7 TB** |

**Note on OSD raw:** all 6 nodes' OSDs feed a single cluster-wide Ceph layer; per-node OSD values in the table above are physical drive capacity, not tier-local storage. Usable Ceph capacity depends on replica / pool topology choices (Ksolves' design decision).

---

## Network — VLAN 37 (nodes) + VLAN 27 (VMs)

VLAN assignments at msb-pmc04:

| Layer | VLAN | CIDR | Purpose | Examples |
|-------|------|------|---------|----------|
| **Proxmox nodes** | **37** | 10.1.37.0/24 | All msb-pmc04 node PubIPs land here; SSH, Proxmox WebUI, Ceph cluster traffic | msb-pmc04-06 at 10.1.37.58; other 5 PubIPs TBD |
| **Workload VMs** | **27** | 10.1.27.0/24 | Network where vendor-provisioned VMs land. DHCP-managed. | dev cluster VMs already at 10.1.27.130–134 on msb-pmc03 (pattern continues here) |
| iLO out-of-band | _(corporate management)_ | 10.1.32.0/24 | Lights-out management for each physical node; not part of Spark fabric | iLO IPs in the per-node table above |

Nodes on VLAN 37; VMs on VLAN 27.

---

## Pre-Provisioning Status

**fqdn-side pre-provisioning is in flight** as of 2026-05-13. The hardware specs above are current as of 05/13/26; the items below are the racking / cabling / addressing work that brings each node into a "ready for vendor provisioning" state.

| Item | Scope | Status |
|------|-------|--------|
| 10/25 Gb fibre install + cable + test | All 6 nodes | In flight |
| iLO configuration | msb-pmc04-05 (only node without iLO IP) | In flight |
| PubIP assignment (VLAN 37) on 10/25 Gb interface | All 6 nodes; -06 already at 10.1.37.58 | In flight |
| Drive installs | 1.2 TB drive on msb-pmc04-05; 3 × 900 GB drives on msb-pmc04-06 | In flight |
| Node labeling | All 6 nodes | In flight |

**Vendor's working surface** — VLAN 27 workload VMs on msb-pmc04 hosts — becomes available once the items above complete. An updated status will be circulated when the surface is live.

---

## Revisions

| Date | Summary |
|------|---------|
| 2026-05-13 | Initial briefing v1.0 — drafted from rack-status spreadsheet captured 2026-05-13. Hardware inventory + VLAN framing + workload split + per-owner pre-provisioning task list. |
| 2026-05-13 (review pass) | fqdn internal review applied: (1) dropped msb-pmc01 comparison from Summary (msb-pmc04 stands on its own framing); (2) VLAN 157 row in network table abstracted to "Vendor access ingress (segregated VDI VLAN)" — pool naming kept out of the vendor-facing briefing; (3) pre-provisioning section trimmed to a vendor-facing status summary plus the 2 joint-input items (Ceph pool topology + per-VM allocations); per-owner detail moved out to TODO.md; (4) MSB-PMC01 companion-doc cross-ref removed; framework v0.3 cross-ref retained with "on-site only" annotation. |
| 2026-05-13 (workload allocation revision) | Workload split restructured to reflect Ksolves' Phase 3 Airflow requirements: 1 dev Airflow (no HA) + 3 prod Airflow HA + shared dev/prod S3 / Ceph storage tier. Marked PROPOSED — pending Ksolves sign-off. Hardware table unified with a "Proposed Workload" column. (Superseded by the next revision.) |
| 2026-05-13 (hardware-only scope) | Scope tightened to **hardware and network capacity only**. Removed: Proposed Workload Allocation section; "Proposed Workload" column from hardware table; tier-based subtotals; Airflow / dev / prod application references; Ceph pool/RGW topology framing; usable-capacity claims (depend on Ksolves' Ceph design decisions). Reformatted all major sections as tables — Summary, Hardware Inventory (per-node + cluster totals), Network, Pre-Provisioning Status, Companion Documents. The briefing now reads as the hardware/network capacity record; Ksolves designs the workload deployment over this infrastructure. |
| 2026-05-13 (network section trim) | Removed the "Why VLAN 37 and 27 are separate" paragraph (vendor-access framing not germane to a hardware-profile briefing) and the "Vendor-facing reading" paragraph (Webex / Horizon references not germane here). Dropped the "Vendor access ingress" row from the VLAN table for the same reason. Network section now reads as the simple "Nodes on VLAN 37; VMs on VLAN 27" framing with the table doing the work. Summary header row relabeled "Node network / Workload-VM network" (was "Host network / Workload-VM network"). Also removed framework v0.3 cross-ref from Companion Documents (briefing now stands alone as hardware/network record) and trimmed the document Status line accordingly. |
| 2026-05-13 (PDF formatting fixes) | Tightened the Hardware Inventory table to fit portrait page width: dropped redundant "Racked" column (all 6 racked — noted in lead-in paragraph instead); renamed "Public IP" → "PubIP" for narrower header; collapsed double-spaces in "3 × 1200 GB + 5 × 900 GB" → "3 × 1200 + 5 × 900 GB"; replaced "_(not yet)_" / "not yet assigned" placeholders with "TBD" for consistency. Companion Documents long file path broken into two lines via `<br>` to allow proper wrapping. PDF regenerated. |
| 2026-05-13 (final pass) | Two final adjustments: (1) dropped the Companion Documents section entirely (fqdn-internal source reference only — not vendor-facing); (2) added `&nbsp;` padding before `TBD` values in the Hardware Inventory iLO/PubIP cells so the columns don't merge visually in the PDF render. |
