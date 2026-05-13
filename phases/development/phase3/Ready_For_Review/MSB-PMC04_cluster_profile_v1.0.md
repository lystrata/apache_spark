# MSB-PMC04 Cluster Profile — Hardware, Network, Workload Split

_Version 1.0 · 2026-05-13_
_For: Ksolves implementation team (Phase 3 preparation)_
_Prepared by: fqdn infrastructure (cluster owner)_
_Status: **Draft for fqdn internal review**. Once approved, promote to `phases/development/phase3/Document/` and circulate to Ksolves with the framework v0.3 context already supplied._
_Source: `phases/development/phase3/Notes/pmc04_cluster_profile_2026-05-13.xlsx`_

---

## Summary

`msb-pmc04` is a **single Proxmox cluster of 6 physical nodes** brought online for the Phase 3 work. **Workload-segregated** (not isolation-segregated): 4 nodes are designated for **development** workloads and 2 nodes are designated for **production** workloads — both inside one cluster membership. This supplements (does not replace) the existing `msb-pmc02` (production Spark) and `msb-pmc03` (development Spark) clusters; msb-pmc04 carries the orchestration, services, and additive Ceph layer that previously lived on `msb-pmc01` (now retiring from the Spark fabric).

**One-line topology:** _all 6 msb-pmc04 hosts sit on **VLAN 37** (Proxmox host management); workload VMs that vendor provisions on these hosts will land on **VLAN 27** per framework v0.3._

---

## Hardware Inventory

All capacities below are in GigaBytes (GB) unless noted. "OSD totals" sum the raw block-device capacity contributed by each node to Ceph.

### Development side — 4 nodes (msb-pmc04-01 → msb-pmc04-04)

| Node | Racked | RAM | ZFS (boot) | OSD layout | OSD raw | iLO | Public IP |
|------|--------|-----|------------|------------|---------|-----|-----------|
| msb-pmc04-01 | Yes | 160 GB | 3 × 600 GB | 5 × 1200 GB | 6 000 GB | 10.1.32.162 | not yet assigned |
| msb-pmc04-02 | Yes | 160 GB | 3 × 600 GB | 3 × 1200 GB + 5 × 900 GB | 8 100 GB | 10.1.32.199 | not yet assigned |
| msb-pmc04-03 | Yes | 160 GB | 3 × 600 GB | 5 × 1200 GB | 6 000 GB | 10.1.32.172 | not yet assigned |
| msb-pmc04-04 | Yes | 160 GB | 3 × 600 GB | 3 × 1200 GB + 5 × 900 GB | 8 100 GB | 10.1.32.232 | not yet assigned |

**Dev subtotals:** **640 GB RAM** · **7.2 TB ZFS (boot)** · **28.2 TB OSD raw**.

### Production side — 2 nodes (msb-pmc04-05, msb-pmc04-06)

| Node | Racked | RAM | ZFS (boot) | OSD layout | OSD raw | iLO | Public IP |
|------|--------|-----|------------|------------|---------|-----|-----------|
| msb-pmc04-05 | Yes | 96 GB | 3 × 600 GB | 21 × 1200 GB | 25 200 GB | _(not yet)_ | not yet assigned |
| msb-pmc04-06 | Yes | 128 GB | 3 × 300 GB | 17 × 1200 GB + 4 × 900 GB | 21 300 GB | 10.1.32.58 | 10.1.37.58 |

**Prod subtotals:** **224 GB RAM** · **~2.7 TB ZFS (boot)** · **46.5 TB OSD raw**.

### Cluster totals

**864 GB RAM · ~9.9 TB ZFS · 74.7 TB OSD raw** across 6 nodes. With the standard Ceph 3-replica configuration, **~24.9 TB usable OSD capacity**.

---

## Network — VLAN 37 (hosts) + VLAN 27 (workload VMs)

Two VLANs interact at msb-pmc04:

| Layer | VLAN | CIDR | Purpose | Examples |
|-------|------|------|---------|----------|
| **Proxmox host management** | **37** | 10.1.37.0/24 | All msb-pmc04 host PubIPs land here; SSH, Proxmox WebUI, Ceph cluster traffic, iLO traffic | msb-pmc04-06 currently 10.1.37.58; other 5 PubIPs pending Sean's assignment |
| **Workload VMs** | **27** | 10.1.27.0/24 | All VMs vendor provisions on these hosts — Airflow, Bastion, GPL, Spark History Server, RGW frontend, Grafana/Prometheus/Loki, etc. | dev cluster VMs already at 10.1.27.130–134 on msb-pmc03 (pattern continues here) |
| iLO out-of-band | _(separate corporate network)_ | 10.1.32.0/24 | Lights-out management for each physical node; not part of Spark fabric | iLO IPs in the table above |

**Why two VLANs:** per the Vendor Access Isolation Framework v0.3 (security/Document/Vendor_Access_Isolation_Framework_v0.3.md), workload VMs sit on a separate VLAN from the Proxmox host layer so that vendor access policy can be enforced at L3 against VLAN 27 specifically without restricting host-management traffic. This is a two-layer control: an L3 firewall policy permits VLAN 157 (Ksolves Horizon pool) → VLAN 27 (workload VMs); remote-domain AD permissions on the VMs are the user-level authorization layer. The host management plane (VLAN 37) is not in the vendor-traffic path.

**Vendor-facing reading:** Ksolves will manage the workload VMs that land on VLAN 27. The Proxmox host layer (VLAN 37) is fqdn-managed. Operational interactions where Ksolves needs to touch a Proxmox host happen via the existing Webex-share / Horizon-pool access mechanisms (BLOCKER.1 / BLOCKER.4), not via direct host network access.

---

## Workload Split — Dev vs Prod within msb-pmc04

The cluster carries **both** dev-orchestration and prod-orchestration services on the same Proxmox fabric. This is consistent with framework v0.3's "dev/prod isolation deferred — not in scope at this design stage" posture.

- **Development orchestration (4 nodes, msb-pmc04-01..04):** Airflow VM, Bastion VM, GPL VM, Grafana/Prometheus/Loki VM, Spark History Server VM, additive Ceph/CephFS/RGW frontend gateways — all serving the msb-pmc03 dev Spark cluster.
- **Production orchestration (2 nodes, msb-pmc04-05/06):** Equivalent service set serving the msb-pmc02 prod Spark cluster. Larger OSD raw capacity reflects production-scale data flows; smaller RAM footprint reflects fewer concurrent VMs (production orchestration is generally less compute-heavy than the workload cluster it serves).

**Note on Ceph topology:** msb-pmc04 contributes OSDs to a Ceph layer that serves both dev and prod orchestration storage. The specific Ceph pool topology (single cluster with pool-level dev/prod separation vs. two separate Ceph clusters within msb-pmc04) is **not finalized in this profile** — Ksolves and fqdn (Rohn + Sean) need to converge on the Ceph design before P0-equivalent Phase 3 work begins.

---

## Open Pre-Provisioning Tasks

These tasks must close before vendor can begin Phase 3 work on msb-pmc04. Tracked under TODO.md § Pending Tasks → Phase 3 prep.

### Owner: Austin (Network)
- [ ] Install 10/25 Gb fibre on msb-pmc04-01: cable + test
- [ ] Install 10/25 Gb fibre on msb-pmc04-02: cable + test
- [ ] Install 10/25 Gb fibre on msb-pmc04-03: cable + test
- [ ] Install 10/25 Gb fibre on msb-pmc04-04: cable + test

### Owner: Sean Klette (Network)
- [ ] Install 10/25 Gb fibre on msb-pmc04-05: cable + test
- [ ] Install 10/25 Gb fibre on msb-pmc04-06: cable + test
- [ ] Configure iLO on msb-pmc04-05 (currently no iLO IP assigned)
- [ ] Assign Public IPs (VLAN 37) to the 10/25 Gb interface on all 6 nodes — msb-pmc04-01..05 pending; msb-pmc04-06 already at 10.1.37.58

### Owner: Rohn (fqdn infrastructure)
- [ ] Install 1.2 TB drive on msb-pmc04-05
- [ ] Install 3 × 900 GB drives on msb-pmc04-06
- [ ] Label all 6 nodes (msb-pmc04-01 through msb-pmc04-06)

### Joint / vendor-coordinated
- [ ] Define Ceph pool topology for msb-pmc04 — single cluster with dev/prod pool separation, or two separate Ceph clusters per workload side. Vendor input needed; aligns with the framework v0.3 dev/prod isolation deferral.
- [ ] Confirm workload VM allocations to specific nodes (which node hosts Airflow, which hosts Bastion, etc.) — anticipates the per-VM placement decisions for Phase 3.

---

## Companion Documents

- **`phases/development/phase2/Document/MSB-PMC01_airflow_host_briefing_v1.3.md`** — prior briefing for the now-retiring msb-pmc01 services; carries the supersession notice pointing here.
- **`phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md`** — main dev critical path; § Update (2026-05-13) covers the Phase 3 May-20 target and Ansible-for-Spark-install scope that anchors msb-pmc04 work.
- **`security/Document/Vendor_Access_Isolation_Framework_v0.3.md`** — VLAN 27 / VLAN 157 architecture that frames vendor access to the workload VMs hosted on msb-pmc04. _(On-site only; reference for fqdn-side context.)_
- **`phases/development/phase3/Notes/pmc04_cluster_profile_2026-05-13.xlsx`** — source spreadsheet captured from Sean / Austin / Rohn's racking work; this briefing derives from it.

---

## Revisions

| Date | Summary |
|------|---------|
| 2026-05-13 | Initial briefing v1.0 — drafted from Sean / Austin / Rohn rack-status spreadsheet captured 2026-05-13. Hardware inventory + VLAN framing + workload split + per-owner pre-provisioning task list. |
