


# Phases Critical Path — fqdn Development Cluster

_Version 1.5 · Last updated 2026-05-07_  
_Phases 1–2 detailed plan from fqdn Phase 1 Report (Ksolves) — April 2026 · Configuration baseline from Ksolves Spark & YARN Config v1.0 (2026-05-04)_  
_Report Source: phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf_  
_Config Source: phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf_  
_Status: Phase 1 (Planning) COMPLETED Apr 24 · Phase 2 (Implementation) PENDING BLOCKER.1 (Ksolves access — Phase 1A active via Webex; Phase 1B gated by BLOCKER.4) + BLOCKER.3 (HIPAA compliance) + BLOCKER.4 (Phase 1B vendor-access isolation, NEW 2026-05-06) · 3-node cluster finalized 2026-05-05 (vendor-recommended +1 node declined — budget) · Ksolves Horizon pool stood up 2026-05-07 (test-ready, awaiting validation) · Out-of-scope items flagged for vendor clarification_

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
- **SOW V1.1 pending:** the 2026-04-27 verbal vendor reversal (single YARN RM, no ZooKeeper, no nginx — captured in P0.2, P1.2, and the dropped P1.3/P1.4) is **not yet reflected** in a written SOW revision. SOW V1.1 also needs to capture (a) the 3-node finalization (vendor recommended +1 node; declined 2026-05-05 on budget), (b) the new HIPAA scope (BLOCKER.3 below + `CP_HIPAA_Compliance_v1.0.md` sub-project), and (c) the rollover to vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` (2026-05-04) as the configuration baseline. The SOW Document History table is still blank past V1.0; § 9 requires a written, signed change order for material scope changes. Tracked under `TODO.md § Waiting for Vendor Reply`.
- **Out-of-scope reminder:** SOW § 2.2 excludes "user load or performance testing" — P1.8 (5 production sample jobs / shuffle amplification measurement) likely needs a Change Order or separate SOW.
- **3-node cluster decision (2026-05-05):** Vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.3 SLA Risk Summary recommends "Phase 1 (+1 node → 2 concurrent jobs) strongly recommended" — fqdn has **declined** the +1 node addition on budget grounds. The 3-node cluster proceeds with **1 concurrent Spark job**; vendor's "feasible-but-zero-buffer" SLA analysis at 3 nodes is the accepted posture. Mitigation strategies: schedule the 12 largest tables first (79.29% of total volume per vendor analysis); add Airflow size-check gate to skip the 184 placeholder tables.
- **NUC hardware prerequisite resolved (2026-05-06):** Ksolves' Phase 1A Windows-host hardware blocker (NUC reliability issues in their data center) is resolved. User has shifted to hosting Webex from their fqdn-office host. Phase 1A is **active** — vendor lead drives Proxmox provisioning over Webex screen share with fqdn oversight. Ansible `--check`-mode playbook testing has begun (2026-05-07).
- **CIO declined Phase 1B (2026-05-06):** A 2026-05-06 meeting with the CIO declined Phase 1B (Ksolves VMware Horizon VDI access) on the originally-proposed terms. Phase 1B is now gated on a vendor-access isolation design — captured as BLOCKER.4 below. Phase 1A (Webex screen share) continues as the interim access mechanism while the BLOCKER.4 design is sized.
- **Ksolves Horizon pool stood up (2026-05-07):** Initial pool built and reachable via UAG; `ks_test` AD group attached for fqdn-side validation; pool-egress firewall policies set (DNS, AD, UAG, Connection Servers allowed; everything else blocked). One BLOCKER.4 sub-task complete pending validation testing. Other vendor-isolation requirements remain open. Email circulated to Network and Cyber stakeholders requesting alignment on pool-↔-cluster-side design layering. Tracked in TODO.md § Vendor Access Isolation.
- **MTU mismatch resolved (2026-05-06):** fqdn networking team resolved the 1400/9000 MTU mismatch between MSB-PMC01 and MSB-PMC03 cluster paths. Closes a previously implicit P0.7 follow-up.

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

- **Status:** PARTIALLY OPEN — Phase 1A **active 2026-05-06** (NUC hardware prerequisite resolved); Phase 1B blocked on **BLOCKER.4** (vendor-access isolation design)
- **Priority:** BLOCKING for Phase 1B; Phase 1A is unblocking some Ksolves work in the interim
- **Context:** Ksolves will be granted owner-level access to both Proxmox clusters (Proxmox One for Service Host, Proxmox Two for Spark Development Cluster). No VMs have been created, no NVMes assigned to Ceph OSDs or Spark scratch. Ksolves requires remote access to begin Phase 1 infrastructure provisioning.

Two-stage access strategy: an interim Webex desktop arrangement followed by a permanent VMware Horizon VDI deployment.

<a id="blocker1-phase-1a-interim-webex"></a>

#### Phase 1A — Interim: Shared Webex Desktop with fqdn Team Oversight — **ACTIVE 2026-05-06**

- Ksolves vendor lead connects to fqdn Webex Desktop shared by fqdn infrastructure team member
- Ksolves executes Proxmox commands / VM provisioning through shared desktop screen
- fqdn team member retains visual oversight of all Ksolves actions (audit trail)
- **Status:** Active 2026-05-06 — vendor's Windows-host hardware prerequisite resolved (see resolution note below)
- **Throughput:** Limited by single shared desktop; Phase 1B (Horizon VDI) targets parallel sessions for vendor team

> **🪟 Hardware Prerequisite Resolution (2026-05-06):** The original Phase 1A blocker was that Webex's Linux desktop client does not support remote control of a Windows Webex share (or vice-versa). Ksolves is a Linux shop; fqdn shares from a Windows host. Cross-platform remote control is not implemented in Webex's Linux client (verified 2026-04-30). The blocker was specifically **NUC reliability issues** in Ksolves' data center delaying their Windows-host provisioning. **Resolution (2026-05-06):** user shifted to hosting Webex from their fqdn-office host; Phase 1A activated on that path. Ksolves' NUC remediation is no longer on the critical path for Phase 1A.

<a id="blocker1-phase-1b-permanent-horizon"></a>

#### Phase 1B — Permanent: VMware Horizon Desktop Access — **GATED BY BLOCKER.4**

- Multiple VMware Horizon Desktop sessions provisioned for Ksolves team via the **Ksolves Horizon pool** stood up 2026-05-07
- Ksolves authenticates to Horizon desktops with fqdn-issued credentials (vendor-account list pending — Michelle owns the bridge)
- Full owner-level Proxmox access via Horizon desktop environment
- **Dependency:** **BLOCKER.4** (vendor-access isolation design + Cyber endorsement + CIO sign-off) — original Cyber Security approval was declined 2026-05-06 on the originally-proposed terms
- **Status (2026-05-07):** Pool stood up by vendor (UAG-reachable); pool-egress firewall policies set; `ks_test` AD group attached for fqdn-side validation. **One** BLOCKER.4 sub-task complete pending validation; remaining gates open. Ksolves user provisioning awaits Michelle's user-list completion.
- **Timeline:** Pool validation testing imminent (Sean + Rohn). Phase 1B go-live still gated on BLOCKER.4 closure.

---

- **Phase 1A — User Actions (Active 2026-05-06):**
  - [x] Set up shared Webex Desktop session from fqdn Windows host with Ksolves vendor lead — **active 2026-05-06**
  - [x] Create temporary Proxmox owner credentials for Ksolves to use during Webex session
  - [x] Document Ksolves actions via Webex recording / shared notes for audit trail
  - [x] Verify Webex connectivity and remote-control permissions

- **Phase 1A — Vendor Actions (Resolved 2026-05-06):**
  - [x] Ksolves Windows-host NUC remediation — no longer on Phase 1A critical path; user shifted to fqdn-office Windows host

- **Phase 1B — User Actions (BLOCKER.4-gated; in flight 2026-05-07):**
  - [x] Ksolves Horizon pool stood up (Jason / 2026-05-07) — UAG-reachable, `ks_test` AD group attached
  - [x] Pool-egress firewall policies set (Austin / 2026-05-07) — DNS, AD, UAG, Connection Servers allowed; everything else blocked
  - [ ] Pool validation testing (Sean + Rohn) — confirm session brokering, AD auth, allow-list reachability, deny-list blocking
  - [ ] Vendor user list (Michelle owns) — provision Ksolves AD accounts on the pool
  - [ ] Cluster-side isolation design (Sean Klette lead — see BLOCKER.4)
  - [ ] Cyber endorsement of design candidate (Paul Barber)
  - [ ] CIO risk-acceptance sign-off (Rob Ball)
  - [ ] Phase 1B exit-condition decision (Rohn + Paul)
  - [ ] Migrate Ksolves access from Webex interim to permanent Horizon
  - [ ] Retire Phase 1A Webex session once Phase 1B is live

- **Verification (Phase 1A — Active):** 
  - [x] Webex desktop session displays Proxmox web UI
  - [x] Ksolves vendor lead can execute administrative commands via remote control
  - [x] Webex recording captures actions (audit trail)

- **Verification (Phase 1B — Pending):**
  - [ ] Horizon desktop sessions authenticate via fqdn AD
  - [ ] Pool validation confirms expected reachability/blocking posture
  - [ ] Ksolves confirms owner-level Proxmox access via Horizon
  - [ ] Phase 1A Webex session retired; all future access via Horizon

- **Owner:** fqdn infrastructure team (Phase 1A active) + Network/Cyber/CIO/Ksolves (BLOCKER.4 gate for Phase 1B)
- **Estimated Effort:** 
  - Phase 1A: ongoing (active interim access)
  - Phase 1B: pool validation 1–2 hours; cluster-side design + Cyber/CIO sign-off measured in weeks (see BLOCKER.4 for breakdown)
  - **Critical Path Note:** Phase 1A is unblocking some work in the interim; Phase 1B closure is bound by BLOCKER.4 and is the long-pole gate.

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
- **Downstream impact:** P0.1 and P0.2 VM creation no longer gated on this blocker; BLOCKER.1 (Ksolves remote access) and the newly-added BLOCKER.3 (HIPAA compliance) are the remaining production gates.

---

<a id="blocker3-hipaa-compliance"></a>

### 🔒 BLOCKER.3 — HIPAA Compliance (Spark / YARN / Ceph encryption + Web UI ACL)

- **Status:** OPEN — added 2026-05-05; tracked in companion sub-project
- **Priority:** BLOCKING — production handling of ePHI data on the Spark cluster requires HIPAA encryption and access-control posture per 45 CFR § 164.312
- **Sub-project:** **`phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md`** — owns all detailed items, owners, and verification steps. This BLOCKER carries only the gate; resolve all items in the sub-project to lift the gate.
- **Source:** Ksolves' `Ksolves_Spark_YARN_Config_v1.0.pdf` § 8 (HIPAA Compliance Architecture & Guidelines)
- **Why it's a separate sub-project:** the scope spans three encryption pillars (transmission, at rest, web UI) plus a custom javax servlet filter that fqdn must develop; mixing it into the main critical path obscures the cross-team coordination needed (Cybersecurity / Dev / Vendor / Ops). The sub-project tracks each item with explicit ownership and a critical-path sequence of its own.

#### Quick summary (full detail in sub-project)

- **Vendor-owned** (configured during Spark install — § 8.1, § 8.2):
  - TLS to Ceph S3A · authenticated + encrypted Spark RPC (AES-GCM) · SSL on Web UIs · local Spark I/O encryption · server-side encryption on Ceph buckets
- **fqdn-owned** (parallel work):
  - Custom javax servlet filter for Spark Web UI / History Server ACL (Spark provides no built-in)
  - Decide auth integration target for the filter (Okta / LDAP / Kerberos)
  - Kerberos realm + `spark-etl@<REALM>` keytab for Spark service auth
  - Notify Ksolves: NVMe scratch drives are **already LUKS-encrypted** (vendor's § 8.2 calls for LUKS — fqdn-side already done; vendor must not reformat)
- **Already done** (fqdn side):
  - LUKS encryption on the four NVMe scratch drives across all 3 dev nodes

- **Verification gate (lifts BLOCKER.3):** all items in `CP_HIPAA_Compliance_v1.0.md` closed; verification artifacts captured for HIPAA audit trail.

---

<a id="blocker4-vendor-access-isolation"></a>

### 🔒 BLOCKER.4 — Phase 1B Vendor-Access Isolation Design (NEW 2026-05-06)

- **Status:** OPEN — added 2026-05-06 following CIO declination of Phase 1B on the originally-proposed terms; partial progress 2026-05-07 (Horizon pool stand-up + initial firewall posture)
- **Priority:** BLOCKING for Phase 1B (VMware Horizon VDI access) — does not block Phase 1A (Webex screen share is the active interim access)
- **Context:** A 2026-05-06 meeting with the CIO declined Phase 1B on the originally-proposed terms. Phase 1B is now gated on a vendor-access isolation design that constrains the vendor's network exposure to a documented IP allowlist + cluster-side network controls. The design must be sized, endorsed by Cyber, and signed off by the CIO before vendor accounts are created on the Horizon pool.
- **Source documents (security context — on-site revision control only):**
  - `security/Notes/vendor-access-isolation-plan_2026-05-06.md` — full meeting capture, CIO position, mitigation brainstorm, ruled-out approaches, open architecture questions
  - `security/Document/vendor_security_design_overview_v1.0.md` — distribution brief
  - `security/Notes/harper_meeting_summary_vdi_security_2026-05-06.md` — Harper's meeting summary (12 action items)
- **Allowed-surface constraints (CIO directive 2026-05-06; list expected to evolve):**
  - Spark Proxmox cluster (msb-pmc03) — all 3 hosts
  - VMs created on msb-pmc03
  - Bastion VM on `msb-pmc01-04` (vendor's only msb-pmc01 surface)
  - VLANs 37 (mgmt), 38 (cluster), 39 (CephFS) on msb-pmc03
  - AD domain controllers — all of them (Okta SSO is AD-tied; cannot subset)
- **Active design candidate (Sean Klette, Network):** make msb-pmc03 the **sole tenant** of VLANs 37/38/39 and add a new **VLAN 10** chokepoint for ingress/egress (Proxmox WebUI + SSH + VM access). If this lands, intra-cluster traffic is permitted by VLAN membership rather than per-IP allowlist, and VLAN 10 is the single chokepoint for the ~30–35 IP allowlist. Substantially simpler than per-host firewalls. **Open implication (DNS-confirmed 2026-05-06):** msb-pmc01 and msb-pmc03 currently share `10.1.37.0/24`; making msb-pmc03 sole-tenant of 37/38/39 may require renumbering one cluster — see `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Sean's VLAN Isolation Approach addendum for the four design paths.

#### 2026-05-07 progress (one sub-task complete)

- **Ksolves Horizon pool stood up** (Jason) — pool built and reachable via UAG; `ks_test` AD group attached for fqdn-side validation before vendor accounts come in.
- **Pool-egress firewall policies set** (Austin) — pool can reach DNS, AD, UAG, and Connection Servers; everything else blocked until further notice.
- **CIO declined still stands** — pool stand-up + initial allow/block posture is one BLOCKER.4 sub-task complete; all other vendor-isolation requirements remain open.
- **Alignment email circulated** — `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md` to Sean Klette and Austin asking for sync output on pool-↔-cluster-side design layering.

#### Layering hypothesis (working assumption — pending Sean + Austin sync)

Austin's pool-level egress policies constrain the **pool itself** (what the pool VMs can talk to). Sean's cluster-side work would constrain **what the pool can reach into msb-pmc03** (what the cluster accepts from the pool's allowed destinations). These layer rather than replace — pool-level controls bound the egress space; cluster-side controls bound the ingress space. Sean + Austin sync output (triggered by Rohn's 2026-05-07 alignment email) will confirm or correct this framing.

#### Gate status table (full sub-task view, mirrors `security/Notes/vendor-access-isolation-plan_2026-05-06.md`)

| Sub-task | Status | Owner |
|---|---|---|
| BLOCKER.1 Phase 1A — Vendor Windows-host hardware prerequisite | **Resolved 2026-05-06** (Webex active) | (closed) |
| Ksolves Horizon pool stand-up + initial firewall posture | **Done 2026-05-07** (pending validation) | Jason / Austin |
| Pool validation testing (`ks_test` group) | Open | Sean + Rohn |
| Sean + Austin sync on pool ↔ cluster-side layering | Open | Sean + Austin |
| Cluster-side isolation design (VLAN approach or alternative) | Open | Sean Klette |
| Snowflake / Azure egress allowlist mechanics | Open | Rohn (fqdn) |
| AD DC enumeration | **Closed 2026-05-06** (7 DCs documented) | (closed) |
| OPSWAT install request | **Closed 2026-05-07** (awaiting vendor) | Rohn / Ksolves |
| Vendor user list for VDI accounts | Open | Michelle (bridge) + Ksolves |
| Cyber review of final design | Open (downstream) | Paul Barber |
| CIO risk-acceptance sign-off | Open (downstream) | Rob Ball |
| Phase 1B exit-condition decision | Open | Rohn + Paul Barber |
| Phase 1B — Horizon VDI go-live | Open, **gated on rows above** | fqdn Cyber |

#### Sub-tasks by owner (full detail)

_Network (Sean Klette):_
- [ ] Develop the VLAN-isolation proposal — confirm tenancy on VLANs 37/38/39 exclusive to msb-pmc03; design VLAN 10 ingress/egress; document routing topology enforcing "only path out is via VLAN 10". **Open implication:** msb-pmc01 and msb-pmc03 share `10.1.37.0/24` (DNS-confirmed 2026-05-06) — sole-tenancy may require renumbering one cluster; see `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Sean's VLAN Isolation Approach addendum for the four design paths
- [ ] Sync with Austin on Horizon pool ↔ cluster-side design layering (triggered by Rohn's 2026-05-07 email; confirm or correct the layering hypothesis above)
- [ ] Confirm consistent IP blocks for vendor-created VMs (allowlist as CIDR vs. enumerated)
- [ ] Address the 10.1.37.0/24 cluster overlap if VLAN-isolation path is chosen (renumbering vs. one of the alternative paths)

_Network (Austin — Horizon pool admin):_
- [x] Stand up Ksolves Horizon pool — built 2026-05-07; UAG-reachable; `ks_test` AD group attached for pre-vendor validation
- [x] Set initial pool-egress firewall posture — DNS / AD / UAG / Connection Servers allowed; everything else blocked. Awaiting confirmation of policy enforcement layer (network FW vs NSX micro-seg vs host-level) per Rohn's 2026-05-07 email
- [ ] Sync with Sean on layering (joint with Sean Klette item above)
- [ ] Refine pool-egress allowlist as Snowflake/Azure egress mechanics land (Rohn's item below feeds this)

_fqdn (Rohn):_
- [x] Vendor-isolation email to Ksolves drafted + sent 2026-05-07 (`correspondence/Document/vendor_email_horizon_vdi_security_revision_2026-05-06.md`)
- [x] Alignment email to Sean + Austin on Horizon pool stand-up sent 2026-05-07 (`correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`)
- [x] Enumerate AD domain controllers in scope — closed 2026-05-06 (7 DCs across 4 sites: Windsor ×2, Garfield ×1, South ×2, MSB RW + RO; see security note)
- [x] Request Ksolves install OPSWAT security client — closed 2026-05-07 (requested; awaiting vendor confirmation of install across vendor devices)
- [ ] Pool validation testing (Sean + Rohn) — confirm session brokering through UAG → Connection Servers, AD authentication via `ks_test` group, intended destinations reachable, blocked destinations actually blocked. **Predates any Ksolves user provisioning** — flips the pool from test-ready to ready-for-vendor-accounts
- [ ] Investigate nftables-based outbound filtering as defense-in-depth (Proxmox `nftables` + RHEL VM `firewalld`)
- [ ] Investigate constrained vendor sudo (carve out `nft` / `iptables` / `firewall-cmd` from vendor sudoers)
- [ ] Decide cloud egress allowlist mechanics — Snowflake / Azure Blob endpoint IPs rotate (FQDN-based vs. published CSP IP ranges vs. egress proxy). Output feeds Austin's pool-egress allowlist refinement
- [ ] Validate `remote.corp.<fqdn>` test-account logins work on dev cluster RHEL servers (Item #7 from Harper's summary)
- [ ] Evaluate feasibility / legal implications of fqdn performing portions of the installation (Item #10 from Harper's summary)
- [ ] Provide Ksolves an updated estimate for when secure access will be available (Item #12)

_fqdn (Michelle — vendor user provisioning bridge):_
- [ ] Vendor user list for Horizon pool — provision Ksolves AD accounts on the pool. Predicated on pool validation testing (above) passing first

_Vendor (Ksolves):_
- [ ] Confirm OPSWAT install across vendor devices (vendor-side device-posture attestation)
- [ ] Vendor user list bridge — Ksolves supplies the names; Michelle provisions

_Reviewers (downstream):_
- [ ] Cyber review of final design (Paul Barber) — once Rohn + Sean have a candidate
- [ ] CIO risk-acceptance sign-off (Rob Ball) — once Cyber endorses
- [ ] Phase 1B exit-condition decision (Rohn + Paul Barber) — when does the design come off, what does cluster network posture revert to

- **Verification gate (lifts BLOCKER.4 → unblocks Phase 1B):** all open items above closed; design endorsed by Cyber; CIO risk-acceptance signed; pool validation testing passed.
- **Owner:** Rohn (coordination) + Sean Klette + Austin (Network design) + Michelle (vendor user bridge) + Paul Barber (Cyber endorsement) + Rob Ball (CIO sign-off) + Ksolves (OPSWAT, user list)
- **Estimated Effort:** Multi-week. Cluster-side design + Cyber review + CIO sign-off measured in weeks; pool validation 1–2 hours once vendor accounts are provisioned.
- **Critical Note:** Phase 1A (Webex) is the working interim access while BLOCKER.4 is sized; vendor work continues in the interim. Closing BLOCKER.4 is the gate that flips Ksolves from interim Webex screen-share to permanent multi-session VDI access. **The CIO declination still stands** — pool stand-up + initial firewall posture is one sub-task complete pending validation; the gate is reduced in scope, not lifted.

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

### ✅ P0.0a — Gather CSV File Information for Storage & Shuffle Verification — **CLOSED 2026-05-05**

- **Status:** ✅ CLOSED 2026-05-05 — vendor delivered the analysis themselves based on `csv_file_sizes.xlsx` shared by fqdn
- **Priority:** _Was CRITICAL_ — informed infrastructure sizing validation
- **Resolution (2026-05-05):** Ksolves performed the file inventory and compression analysis directly using `csv_file_sizes.xlsx`. Findings published in `Ksolves_Spark_YARN_Config_v1.0.pdf` (2026-05-04) § 1.1 Raw Data Characteristics:
  - **800 tables** total in mapping definition
  - **359 tables** with actual DEV data (size > 0)
  - **257 tables** are schema-only placeholders (size = 0)
  - **184 tables** with no files / no fileform (not yet populated)
  - **12,214 files total** in DEV batch
  - **1.52 TB compressed CSV** (revised down from the previously-assumed 4 TB; DEV is a subset of full prod load)
  - **Multi-file tables:** exactly 2 — Table A (527.95 GB, 293 cols, 5,800 files, ~97 MB/file avg) and Table B (113.10 GB, 94 cols, 5,800 files, ~21 MB/file avg)
  - **Single-file tables:** 1 KB – 145.57 GB (extreme variance)
  - **Widest schema:** 384 columns (one table); 14 tables have >100 cols (impacts sort memory)
- **SLA Implications (vendor § 1.3):**
  - Top 12 tables = 1,234.15 GB = **79.29% of total volume** — must run first
  - Multi-file Table A (527 GB) = ~32 min at 1 TB/hr — single largest job
  - SLA window 4 hours (240 min); critical path estimate ~159 min for top 12 tables; ~81 min buffer for 347 smaller jobs
  - Vendor recommended +1 node for 2-concurrent operation; **fqdn declined 2026-05-05** (budget) — 3-node posture is feasible-but-zero-buffer
- **Owner (was):** User (fqdn); _now: Vendor delivered_
- **Downstream impact:** Storage allocation, OSD capacity, and shuffle amplification estimates are now grounded in measured rather than assumed values. P0.1 (Worker VM creation) proceeds with confidence.

---

<a id="p0-0b-gzip-mitigation"></a>

### 🔴 P0.0b — GZIP Non-Splittability Mitigation Decision (Development-Team Owned)

- **Status:** OPEN (DEV-TEAM DECISION)
- **Priority:** CRITICAL — Vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 2 identifies GZIP non-splittability as the **single most critical technical constraint** for the workload. Configuration settings like `spark.sql.files.maxPartitionBytes` have no effect on non-splittable formats; a 145 GB single `.csv.gz` file becomes exactly 1 Spark partition = 1 task = 1 executor core reading the entire file sequentially. All 8 executor cores sit idle for that table until a `repartition()` call redistributes the data.
- **Owner:** **fqdn Development team** (this is an upstream / ETL design decision, not a cluster config)
- **Source:** `Ksolves_Spark_YARN_Config_v1.0.pdf` § 2
- **Decision required:** choose 1 of 4 mitigation strategies from the vendor doc:
  1. **Pre-split files upstream** (Best Practice / Zero SLA Risk) — source system splits massive tables into 100–200 MB chunks before compression. Trade-off: requires coordination + engineering with upstream data providers.
  2. **Change compression codec to bzip2** (Excellent / Low SLA Risk) — bzip2 has internal block markers, splittable in Spark. Trade-off: slightly slower compression/decompression, but parallel processing wins.
  3. **Send uncompressed CSVs** (Good / Medium SLA Risk) — raw text is natively splittable. Trade-off: 4–6× larger storage footprint on Ceph + network transfer time.
  4. **Post-read repartition** (Last Resort / High SLA Risk) — `df.repartition()` immediately after `spark.read.csv()`. Forces shuffle to all task slots for downstream transforms. Trade-off: does NOT fix the initial read bottleneck; OOM risk before repartition completes.
- **Vendor recommendation:** Option 1 (pre-split upstream) for zero SLA risk.
- **Conditional fallback:** if Option 1, 2, or 3 cannot be implemented for some tables, vendor's repartition formula `target_partitions = max(24, ceil(compressed_csv_mb / 50))` must be embedded in the Spark job code per § 7.2 (Repartition Code Template). Airflow DAG must inject `compressed_mb` per-table as a job parameter.
- **Impact on plan:** This decision affects ETL job design but does not block infrastructure provisioning. P0.0–P0.5a can proceed in parallel.
- **Estimated Effort:** Decision: 1–2 weeks (cross-team — Dev / upstream data team / vendor coordination). Implementation depends on chosen option.

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

### ✅ P0.3 — Confirm Cloud Staging Target — **CLOSED 2026-05-05: Azure Blob**

- **Status:** ✅ CLOSED 2026-05-05 — Azure Blob confirmed
- **Priority:** _Was CRITICAL_ — Stage 6 egress pipeline design
- **Resolution (2026-05-05):** Pipeline confirmed by vendor: `Airflow DAG → spark-submit per table → Ceph RGW (S3-compatible) → Parquet → Snowflake COPY INTO from Azure Blob` (per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1 Raw Data Characteristics: Pipeline row).
- **Implementation impact:** SAS token / managed identity / service principal authentication for Azure (TBD by fqdn data-platform team); network routing through exaBGP floating IP for Spark cluster → Azure egress; Snowflake `COPY INTO` reads from Azure stage.
- **Owner (was):** fqdn data-platform decision-maker; _now: closed_

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
- **Vendor Configuration Note (added 2026-05-05):** Per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 3.4 deployment note — Spark 3.5.x ships with Hadoop 3.3.x; this cluster uses Hadoop 3.4.1. Ksolves must set `HADOOP_HOME` → 3.4.1 + `spark.yarn.populateHadoopClasspath = true` in `spark-defaults.conf` so Spark uses the standalone Hadoop 3.4.1 libraries (not its bundled 3.3.x). **Owner: Vendor (Ksolves) during Spark install.**

<a id="p0-6-ceph-rgw-tuning"></a>

### 🔴 P0.6 — Ceph RGW Server-Side Tuning (Vendor-Owned)

- **Status:** PENDING P0.0 (CEPH BOOTSTRAP)
- **Priority:** HIGH — required for sustained S3 throughput at peak shuffle
- **Owner:** **Vendor (Ksolves)** — they are the Ceph admin until cluster sign-over
- **Source:** `Ksolves_Spark_YARN_Config_v1.0.pdf` § 6.4 ("Ceph-Side RGW Tuning — Ceph Admin Action Required")
- **Context:** Default Ceph RGW thread pool becomes a bottleneck when 3 executors × 8 cores simultaneously issue range reads against 3 RGW instances — especially during the 5,800-partition multi-file table jobs (Table A: 527 GB, Table B: 113 GB). Vendor's analysis recommends raising thread pool and concurrent request limits.
- **Vendor Actions Required:**
  - [ ] Apply Ceph cluster-side config: `ceph config set client.rgw rgw_thread_pool_size 512`
  - [ ] Apply Ceph cluster-side config: `ceph config set client.rgw rgw_max_concurrent_requests 1024`
  - [ ] Restart RGW daemons on all three nodes for config to take effect
- **Verification (fqdn post-install):**
  - [ ] `ceph config get client.rgw rgw_thread_pool_size` returns 512
  - [ ] `ceph config get client.rgw rgw_max_concurrent_requests` returns 1024
  - [ ] RGW daemons restarted post-config-change
- **Critical Note:** This tuning is on the **cluster sign-over verification checklist**; do not accept handover from Ksolves until this is in place and verified.

---

<a id="p0-7-network-connectivity-verification"></a>

### 🔴 P0.7 — Verify Network Connectivity: MSB-PMC01 ↔ MSB-PMC03 (Pre-requisite for P1.0)

- **Status:** OPEN (NETWORK TEAM COORDINATION) — MTU 1400/9000 mismatch resolved 2026-05-06; remaining verification steps still required
- **Priority:** CRITICAL — Gate for Remote Airflow Server provisioning (P1.0)
- **Context:** Remote Airflow server will be provisioned on MSB-PMC01 cluster. Ksolves requires verified network connectivity between MSB-PMC01 and MSB-PMC03 (Spark cluster nodes) with sufficient bandwidth for:
  - Airflow DAG submission to YARN ResourceManager (port 8032, low bandwidth)
  - Spark driver logs and monitoring (continuous, low-moderate bandwidth)
  - Ansible (running directly on Proxmox dev nodes per the 2026-05-07 topology decision; SSH key-based — low bandwidth)
- **User Actions Required:**
  - [ ] Coordinate with fqdn Network Team to verify/establish network path: MSB-PMC01 ↔ MSB-PMC03
  - [ ] Confirm routing between clusters (same VLAN, or routable via firewall)
  - [ ] Verify firewall rules allow:
     - MSB-PMC01 → MSB-PMC03 nodes (TCP 8032, 8088, 22, 9095 for JMX if monitoring)
     - MSB-PMC03 nodes → MSB-PMC01 (return traffic on same ports)
  - [ ] Test connectivity: ping from MSB-PMC01 to each MSB-PMC03 node; TCP port tests (`nc -zv`)
  - [x] **MTU mismatch resolved 2026-05-06** — fqdn networking team aligned the 1400/9000 MTU between MSB-PMC01 and MSB-PMC03 paths
  - [ ] Document network topology and firewall rules for audit trail
  - [ ] Share verification results with Ksolves before P1.0 provisioning begins
- **Verification:** 
  - [ ] Network team confirms connectivity in change ticket
  - [ ] Ping response times < 10ms (same datacenter assumed)
  - [x] MTU consistent end-to-end (resolved 2026-05-06)
  - [ ] TCP ports open: `nc -zv <node> 8032`, `nc -zv <node> 8088` succeed on all three MSB-PMC03 nodes
- **Owner:** fqdn Network Team
- **Estimated Effort:** 2-4 hours (coordination + testing + documentation)
- **Critical Note:** This is a hard gate. P1.0 cannot proceed until network connectivity verified and documented. **Ansible scope clarification:** Ansible no longer runs from a remote control node on the Airflow VM (decision 2026-05-07) — it runs directly from each Proxmox dev node. P0.7 connectivity remains required for Airflow → YARN, Spark driver logs, and other inter-cluster traffic, but the Ansible cross-cluster SSH path is no longer in scope.

---

<a id="phase-2b-high-priority-infrastructure-services"></a>

### Phase 2B — High Priority: Infrastructure Services & HA (P1)

<a id="p1-0-provision-remote-airflow-host"></a>

### 🟠 P1.0 — Provision Remote Airflow Server (Ksolves Open Item #8)

- **Status:** PENDING P0.7 NETWORK VERIFICATION (REMOTE INFRASTRUCTURE)
- **Priority:** HIGH — Prerequisite for Airflow orchestration and stable web-UI front-door
- **Context:** Remote Airflow host coordinates ETL job submission to Spark cluster. Spec: **6 vCPU / 24 GB RAM / 500 GB SSD**, RHEL 9.4. **Target node: `msb-pmc01-04`** — Intel Xeon Gold 6136 @ 3.00 GHz, 1 socket × 12 cores × 2 threads (24 logical CPUs), 130 GB RAM, single NUMA node, 6 Ceph OSDs. Cluster is fqdn-managed; Ksolves provisions services into it. See `phases/phase2/development/Document/MSB-PMC01_cluster_host_inventory.md` for full hardware inventory of all four nodes (msb-pmc01-01 through 04). **Topology change (2026-05-07):** Ansible no longer co-located on the Airflow VM (see P1.5 below) — Ansible runs directly on Proxmox dev nodes. The Airflow VM hosts Airflow + Nginx (install in scope; activation TBD by Ksolves).
- **Recommended Proxmox VM topology:** `sockets=1, cores=6`. Host is single-NUMA — no NUMA pinning required. 24 GB RAM ≈ 18% of host's 130 GB. 500 GB volume drawn from the `rbd_ssd` Ceph pool (visible in OSD tree as the dedicated SSD class).
- **Dependency:** **P0.7 (Network Connectivity) must be completed and verified first** — MSB-PMC01 and MSB-PMC03 clusters must be on same network with confirmed firewall rules.
- **Ksolves Actions:**
  - [ ] After network connectivity verified (P0.7), provision VM on `msb-pmc01-04`: `sockets=1, cores=6` / 24 GB RAM / 500 GB SSD (rbd_ssd pool), RHEL 9.4
  - [ ] Configure hostname: `airflow-prod-01` (or fqdn-assigned name)
  - [ ] Network setup: routable to all three MSB-PMC03 Spark nodes, to Snowflake, to cloud staging (Azure/AWS)
  - [ ] Install Okta SSO integration (requires OIDC client ID/secret from fqdn Okta tenant)
  - [ ] **Install Nginx** on the Airflow VM (RHEL package; not yet activated). Server activation / functional configuration is a Ksolves decision (see Nginx note below).
  - [ ] Verify network paths: Airflow → YARN RM (port 8032), Airflow → Ceph RGW (floating IP), Airflow → Snowflake
- **User Actions:**
  - [ ] Confirm MSB-PMC01 hosting and IP allocation (coordinate with Network Team)
  - [ ] Provide Okta OIDC credentials for Airflow SSO configuration
  - [ ] Ensure network connectivity verification (P0.7) complete before Ksolves begins provisioning
- **Prerequisites:** 
  - [ ] **P0.7 network connectivity verified and documented**
  - [ ] Okta SSO client provisioned
  - [ ] MSB-PMC01 networking and IP allocation finalized
- **Verification:** SSH to remote host successful; RHEL subscriptions active; network paths confirmed (ping tests to all three cluster nodes <10ms, TCP port tests succeed, Snowflake/cloud routing confirmed); `nginx -v` reports installed version
- **Owner:** Ksolves (provisioning + Nginx install) + fqdn (networking, SSO setup)
- **Estimated Effort:** 2-3 hours (provisioning + network setup + Nginx package install)
- **Critical Note:** Later P2 items depend on this host being live and network-connected. Ansible no longer runs from this host (see P1.5).

> **🌐 Nginx scope note (correction 2026-05-07):** Earlier "no HA → no Nginx" reasoning (used during the v1.3/v1.4 cycle) was wrong. The single YARN ResourceManager confirms there is no HA stable-endpoint requirement, but stable-endpoint-for-HA is only one of several potential Nginx roles. **Install** is in scope; **server activation / functional configuration is TBD by Ksolves** — candidate roles include reverse proxy for the YARN ResourceManager UI and other Spark/Airflow web UIs, TLS termination, SSO front-door (Okta), URL rewriting for a consistent UI surface, IP allowlisting, and access logging. Ksolves' design decision will determine which roles get activated post-install.

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

### 🟠 P1.5 — Ansible Cluster-Internal Automation (REVISED 2026-05-07 — runs from Proxmox dev nodes)

- **Status:** IN PROGRESS — Ansible + ansible-core installed on all three Proxmox dev nodes 2026-05-07; vendor playbook hierarchy unzipped; `--check`-mode testing underway
- **Priority:** HIGH — Required for infrastructure automation of cluster-internal config (Proxmox + CephFS + supporting OS config)
- **Context (revised 2026-05-07):** Original plan had Ansible on a separate VM (or co-located on the Airflow VM at P1.0). During the 2026-05-07 Webex collab session, vendor engineer 1 (Ksolves) and Rohn agreed Ansible can run **directly on each Proxmox dev node**. Latest Ansible + ansible-core were installed across all three nodes; Ksolves' playbook hierarchy was unzipped on-cluster; `--check`-mode validation has begun. **This removes a planned VM from the topology** and closes the prior msb-pmc01-04 Ansible-capacity TBD from 2026-05-06.
- **Scope clarification:** Playbooks cover **Proxmox config + CephFS install/config + supporting OS configuration** — cluster-internal operations only. If Ansible orchestration of remote services beyond the cluster (e.g., the Airflow VM at P1.0, future remote services on msb-pmc01) becomes needed, revisit this scope.
- **Vendor Actions:**
  - [x] Install Ansible + ansible-core (latest) on all three Proxmox dev nodes (2026-05-07)
  - [x] Unzip Ksolves' Ansible playbook hierarchy on the dev nodes (2026-05-07)
  - [ ] Continue `--check`-mode testing (vendor engineer 1, ongoing 2026-05-08+) — verify expected play behavior without applying changes
  - [ ] Transition to live-apply runs as `--check` confidence builds; capture per-play change diffs in audit trail
  - [ ] Verify SSH/local connectivity model used by playbooks (intra-node sudo + inventory) is consistent with on-cluster execution model
- **fqdn Actions:**
  - [ ] Review playbook hierarchy structure with vendor engineer 1 (joint Webex sessions ongoing)
  - [ ] Confirm any secrets management requirements (Proxmox API tokens, Ceph keys) — if needed, store in cluster-local secrets store (not in playbook tree)
- **Verification:**
  - [x] Ansible reachable from each dev node: `ansible --version` reports installed version
  - [ ] `--check`-mode runs complete without unexpected diffs against current state
  - [ ] Live runs on a single play (lowest-risk) succeed; rollback verified
  - [ ] Full Proxmox + CephFS playbook tree applied; cluster state matches design
- **Owner:** Vendor engineer 1 (Ksolves) — primary; Rohn — joint review and on-cluster validation
- **Estimated Effort:** Multi-session — `--check`-mode testing in progress; live-run timeline depends on test outcomes

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

<a id="p2-8-snowflake-load-completion"></a>

### 🟡 P2.8 — Snowflake Load Completion Confirmation Mechanism (NEW 2026-05-07 — fqdn-owned)

- **Status:** OPEN — added 2026-05-07; design owed by fqdn Development team
- **Priority:** MEDIUM — required to close the "Operational Gate" step in the Phase 1 dev data-flow diagram
- **Owner:** **fqdn Development team** + Murali / Rama (Snowflake side)
- **Source:** Vendor lead (Ksolves), email forwarded 2026-05-06 (referenced in TODO.md). Corroborated by the "Operational Gate Process → Move CSV files off → Designated Storage Node (Archive)" step (#10) in `phases/phase2/development/reference_images/dev_data_flow_diagram_2026-05-06.png`.
- **Context:** The current Snowflake side of the pipeline has no mechanism to confirm `COPY INTO` completion. Without a confirmation signal, the Airflow DAG cannot reliably trigger downstream actions: cleanup of Parquet files from Ceph (Stage 8 of the 8-stage pipeline), archive move of source CSV files, and the "Operational Gate" step that gates batch-cycle progression. Pipeline reliability and SLA accounting depend on this confirmation.
- **Proposed solutions (per vendor email):**
  1. **Audit / checkpoint table in Snowflake** — `COPY INTO` writes a row per load with `(table, file, rows_loaded, status, timestamp)`; Airflow DAG polls the table for the expected row before progressing.
  2. **Snowflake task / event-bridge** — Snowflake task fires on `COPY INTO` success; emits webhook / message that Airflow consumes.
  3. **Snowflake stored procedure wrapper** — Airflow calls a stored procedure that performs `COPY INTO` and returns load metadata directly to Airflow synchronously.
- **Decision required:** which mechanism (likely Option 1 unless infra exists for 2 or 3); auth model (Snowflake user / role / network); polling cadence (Option 1) or webhook endpoint (Option 2).
- **Implementation impact:** Affects Airflow DAG design (P2.2), Snowflake objects (out-of-scope per P2.3 Snowflake scope note — but the audit/checkpoint table itself sits on the Snowflake side and requires fqdn DDL), and Stage 7→8 transition logic. Does **not** block infrastructure provisioning (P0–P1).
- **Verification:** End-to-end test — Airflow triggers `COPY INTO`; load completes; confirmation signal received; downstream cleanup + archive move execute; "Operational Gate" closes correctly.
- **Estimated Effort:** Design + spec: 1–2 weeks (cross-team — Dev / Murali-Rama / vendor coordination). Implementation depends on chosen option.

<a id="p2-9-centralized-audit-logging"></a>

### 🟡 P2.9 — Centralized Audit Logging + Retention Policy (HIPAA-driven, NEW 2026-05-07)

- **Status:** OPEN — added 2026-05-07; placement may shift to `CP_HIPAA_Compliance_v1.0.md` once that sub-project's section taxonomy stabilizes
- **Priority:** MEDIUM (treated HIGH inside the HIPAA sub-project) — required for HIPAA audit-trail compliance
- **Owner:** **fqdn Development team** + fqdn Cyber/Security
- **Source:** Vendor lead (Ksolves), questionnaire Q1–Q3, email forwarded 2026-05-06 (referenced in TODO.md). Aligns with HIPAA § 164.316(b)(2).
- **Context:** HIPAA § 164.316(b)(2) requires audit logs to be retained for **at least 6 years**. Current cluster build has **no SIEM scoped** and no centralized audit-log destination — Spark, YARN, Ceph, RGW access, and Airflow logs are emitted to local filesystems on each VM/host. Without a central retention path, ePHI access events cannot be reliably reconstructed, and the Phase 1 → production transition will fail HIPAA audit.
- **Required design elements:**
  - **Sources to capture:** Spark application logs (driver + executors via History Server), YARN ResourceManager logs, Ceph RGW access logs (S3 calls), Airflow scheduler/webserver logs, Linux auth.log (sudo + SSH), Proxmox auth events, and any ePHI-touching application logs.
  - **Transport:** Promtail or Fluent Bit shippers from each source to the central store; encryption in transit.
  - **Central store:** Loki or equivalent — must support 6-year retention with WORM (write-once, read-many) protection on the audit bucket.
  - **Storage backing:** Likely a dedicated Ceph bucket with versioning + object lock (or external S3 with the same posture).
  - **Access controls:** Read/write segregated; only audit administrators can read; no delete privilege within the retention window.
  - **Integrity:** Periodic integrity checks (hash chain or signing) so log tampering is detectable.
- **Decisions required:**
  - SIEM selection (Loki + Grafana stack already partially in scope per the Grafana/Prometheus/Loki VM at P1.0) vs. Splunk vs. Sentinel vs. other.
  - WORM mechanism (Ceph object lock vs. external WORM-compliant storage).
  - Retention sub-policies (some sources may need >6 years; some may be fine with the floor).
  - Audit-administrator role assignment.
- **Implementation impact:** Likely co-locates with the existing Grafana/Prometheus/Loki VM mentioned in P1.0's host context. Requires Promtail agents on every cluster node + remote service VM. Does **not** block infrastructure provisioning (P0–P1) but **must** be in place before any ePHI processing runs.
- **Verification:** Logs from all enumerated sources land in central store; retention policy verified by attempting a delete (should be denied within retention window); integrity check passes; audit-administrator role can read all logs; non-admin roles cannot.
- **Estimated Effort:** Design: 1 week. Implementation: 2–3 weeks. Validation: 1 week. Likely runs in parallel with HIPAA encryption pillars (BLOCKER.3).
- **Cross-reference:** Once `CP_HIPAA_Compliance_v1.0.md` reaches a section taxonomy that has an "audit / retention" pillar, this task may move there with a back-reference here. For now it lives in the main CP for visibility.

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
- Ksolves technical contact: vendor lead (contact details on file with fqdn)
- Ksolves requires owner-level Proxmox access (BLOCKER.1) before any infrastructure work
- fqdn sign-off required at user checkpoints (P0.2, P1.8, P1.2, P2.3) before proceeding to next phase
- Cloud staging platform decision (P0.3) blocks Stage 6 pipeline implementation

**Critical Path Sequence:**
- **Phase 1 (Planning):** ✅ COMPLETE — All discovery & architecture finalized (Apr 24)
- **Phase 2 (Implementation):** PENDING
  - **Phase 1A active 2026-05-06** — vendor lead drives Proxmox provisioning over Webex screen share (interim access while Phase 1B is gated)
  - [ ] **BLOCKER.4 (NEW 2026-05-06):** Vendor-access isolation design + Cyber endorsement + CIO sign-off — gates Phase 1B (Horizon VDI). Partial progress 2026-05-07 (Horizon pool stood up, initial firewall posture set).
  - [ ] **BLOCKER.1 Phase 1B closure:** Multi-session VDI access via Ksolves Horizon pool — gated by BLOCKER.4 + pool validation testing + vendor user-list provisioning (Michelle owns)
  - [x] BLOCKER.2: User placed RHEL ISO(s) in Proxmox Directory storage at `/rpool/data/templates/iso/` on all three dev-cluster nodes (closed 2026-04-30 — decoupled from P0.0)
  - [ ] **BLOCKER.3:** HIPAA compliance gate — see `CP_HIPAA_Compliance_v1.0.md` sub-project; must close before any production ePHI processing
  - [ ] **P0.0: Ksolves bootstraps Ceph cluster** (MON, MGR, 9× OSD, RGW) — first Ksolves work after access granted
  - [ ] *Parallel user prerequisites:* P0.4 (RHEL subscriptions), P0.7 (network MSB-PMC01↔03; MTU resolved 2026-05-06)
  - [ ] *In-flight, fqdn-owned, parallel:* P0.0b (GZIP mitigation decision), P2.8 (Snowflake load-completion mechanism), P2.9 (centralized audit logging)
  - [ ] P0.1–P0.5: Ksolves provisions all VMs and base software (RHEL ISO already in place from BLOCKER.2)
  - [ ] P0.6: Ceph RGW server-side tuning (vendor-owned, on cluster sign-over checklist)
  - [ ] **P1.2: Ksolves deploys single-instance YARN ResourceManager on GKPR-YARN-RM-01** (manual recovery; no HA)
  - [ ] P1.0: Remote Airflow Server provisioning on `msb-pmc01-04` (Airflow + Nginx install — Nginx activation TBD by Ksolves)
  - [x] **P1.5 (revised 2026-05-07):** Ansible installed on all three Proxmox dev nodes; playbook tree on-cluster; `--check`-mode testing in progress (no separate Ansible VM — topology change)
  - [ ] P1.1: Spark History Server deployed on Node02 (depends on P0.0 RGW + P0.5a Spark)
  - [ ] **P1.8: Phase 1 integration milestone — run 5 sample jobs, measure shuffle amplification, OSD memory (P1.6), and WAN egress (P1.7)**
  - [ ] P2.2–P2.3: Ksolves deploys Airflow and validates end-to-end pipeline (Snowflake side is fqdn responsibility)
  - [ ] Phase 2 sign-off: fqdn approves for production if all P0–P2 items pass + BLOCKER.3 + BLOCKER.4 closed
- **Beyond Phase 2:** Pending Ksolves clarification — See "Actions Outside Present Known Scope"

---

<a id="reference-documents"></a>

## REFERENCE DOCUMENTS

- **Main Report:** phases/phase1/development/Incoming/fqdn Report Phase 1 (Updated).docx.pdf
- **Prerequisites:** phases/phase1/development/Incoming/vendor_prerequisites.docx.pdf
- **Vendor Configuration Baseline:** phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf (2026-05-04)
- **HIPAA Sub-project Critical Path:** phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md
- **Hardware Reference:** CLAUDE.md § Hardware Reference
- **Calculator:** phases/phase1/development/deliverables/dev_cluster_phase1_model.html
- **Ksolves Walkthrough:** phases/phase1/development/research/ksolves-directory-walkthrough.md
- **Vendor Questions:** phases/phase1/development/vendor_comms/phase1_vendor_questions.txt
- **Companion CP — Okta Integration:** phases/phase2/development/Document/CP_Okta_v1.1.md
- **Companion — Remote Airflow Host Briefing:** phases/phase2/development/Document/MSB-PMC01_airflow_host_briefing_v1.1.md
- **Schedule Tracker:** phases/phase2/development/Document/SOW_timeline_status.md
- **Cluster Sizing Tool:** calculators/Document/cluster_sizing_tool.html
- **Math Reference:** calculators/Document/dev_cluster_math_reference.html
- **Storage Reference:** calculators/Document/dev-cluster-storage-reference.html
- **Visual Tracker (HTML):** phases/phase2/development/Document/phases_critical_path_development_tracker_v1.5.html
- **Vendor-isolation source documents (security context, on-site only):** security/Notes/vendor-access-isolation-plan_2026-05-06.md · security/Document/vendor_security_design_overview_v1.0.md · security/Notes/harper_meeting_summary_vdi_security_2026-05-06.md
- **Horizon pool alignment email (2026-05-07):** correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md
- **Vendor security email (2026-05-07):** correspondence/Document/vendor_email_horizon_vdi_security_revision_2026-05-06.md

---

<a id="footnotes"></a>

## FOOTNOTES

¹ Apache Software Foundation, "Running Spark on YARN," in *Apache Spark Documentation*, accessed April 25, 2026, https://spark.apache.org/docs/latest/running-on-yarn.html. The documentation establishes the prerequisite installation order for Spark on YARN: (1) Java/JDK with `JAVA_HOME` set, (2) Hadoop/YARN cluster operational with ResourceManager running, (3) `HADOOP_CONF_DIR` or `YARN_CONF_DIR` pointing to client-side Hadoop configuration, (4) Spark binary distribution built with YARN support. Java compatibility note: "Apache Hadoop 3.4.1 does not support Java 17, but Spark 4.0.0+ requires Java 17+" — for Spark 3.5.3 + Hadoop 3.4.1, Java 11 is the recommended common version. Confirmed with secondary sources: Cloudera/Hortonworks HDP documentation, "Spark Prerequisites," accessed April 25, 2026, https://docs-archive.cloudera.com/HDPDocuments/HDP3/HDP-3.1.5/installing-spark/content/installing_spark.html, which states "HDFS and YARN deployed on the cluster" as Spark prerequisites.

---

---

_Updated: 2026-05-07 (v1.5: BLOCKER.4 vendor-isolation gate added; BLOCKER.1 Phase 1A activated 2026-05-06; Horizon pool stand-up 2026-05-07; Ansible topology revised; Nginx scope corrected; P2.8 Snowflake load completion + P2.9 centralized audit logging added; MTU resolution noted)_  
_Phase 1 status reflected per ksolves_april_24_process_report.txt_  
_Location: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md_  
_Status: Promoted to Document/ on 2026-05-07_
