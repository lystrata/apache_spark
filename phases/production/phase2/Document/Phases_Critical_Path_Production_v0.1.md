


# Phases Critical Path — fqdn Production Cluster

_Version 0.1 · Last updated 2026-04-27 · v1.5-sync header refresh 2026-05-08 · v0.2 framework sync 2026-05-11 · clean-slate body rewrite 2026-05-12_  
_Originally forked 2026-04-27 from `Phases_Critical_Path_Development_v1.2.md`; clean-slate rewrite 2026-05-12 — body content replaced with a production-specific scaffold to remove inherited dev statuses. Parallel sibling doc on the dev side is now `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md`; cross-referenced where applicable but NOT inherited from._  
_Status: **CLEAN-SLATE 2026-05-12 — production-cluster scaffold.** All four phases (1–4) currently NOT YET STARTED / NOT YET PLANNED for the production cluster. Phase status on the dev cluster does NOT imply phase status on the production cluster — each cluster's phases are distinct. The "Update 2026-05-XX" sections below capture dev-cluster events with production-side implications (forward-looking notes for production planning, not retroactive status of the production cluster). Production-specific scope (hardware spec confirmation, traffic profile, HA SLOs, backup/DR, Pre-Flight Gates) will be filled in when production planning starts._

---

## v1.5 Sync Status (added 2026-05-08 per CLAUDE.md § Critical Path Document Synchronization rule)

This document was forked from `Phases_Critical_Path_Development_v1.2.md` (2026-04-27) and has not been updated since the original draft. The development-side critical path has advanced through v1.3, v1.4, and v1.5 in the interim. The following development-side events have occurred and need to be evaluated for production-side impact during the next revision pass:

**v1.2 → v1.3 (2026-04-30):**
- BLOCKER.2 closed (RHEL ISO placement via node-local Directory storage at `/rpool/data/templates/iso/`)
- Phase 1A re-opened 2026-04-30 due to Webex Linux/Windows remote-control limitation

**v1.3 → v1.4 (2026-05-05):**
- 3-node cluster finalized (vendor recommended +1 node, fqdn declined on budget)
- HIPAA scope forked into sub-project: `CP_HIPAA_Compliance_v1.2.md` (BLOCKER.3 added)
- GZIP non-splittability mitigation elevated to P0 decision (P0.0b)
- P0.0a closed (vendor delivered CSV analysis in `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1)
- P0.3 closed (Azure Blob confirmed)
- P0.6 added (Ceph RGW server-side tuning, vendor-owned)
- P0.5a vendor configuration note (Hadoop 3.4.1 vs Spark's bundled 3.3.x classpath fix)

**v1.4 → v1.5 (2026-05-07):**
- BLOCKER.1 Phase 1A active 2026-05-06 (NUC issue resolved; user shifted to fqdn-office Windows host for Webex)
- **BLOCKER.4 added 2026-05-06 — Phase 1B vendor-access isolation gate.** CIO declined Phase 1B on the originally-proposed terms. Production-side equivalent: vendor access for production environment installation will require a similar (or stricter) isolation design. **Production-specific decision needed: does production allow vendor access at all post-handover, or does fqdn perform Phase 4 work directly?** This is one of the items in Harper's 2026-05-06 summary (Item #10).
- Ksolves Horizon pool stood up 2026-05-07 (Jason); pool-egress firewall posture set 2026-05-07 (Austin)
- Ansible topology revised — no separate Ansible VM; runs from Proxmox dev nodes. Production equivalent TBD: same model on production cluster, or separate Ansible control infrastructure?
- Nginx scope correction — install-yes / activation-TBD-by-Ksolves on the Airflow VM. Production equivalent: assume same posture unless production-specific role drives different decision.
- MTU 1400/9000 mismatch resolved 2026-05-06 between MSB-PMC01 and MSB-PMC03 networking paths.
- P2.8 (NEW) — Snowflake Load Completion Confirmation Mechanism. Production-side: the same mechanism is required (probably more stringent for production audit trail).
- P2.9 (NEW) — Centralized Audit Logging + Retention Policy (HIPAA-driven, 6-year floor). Production-side: this is **mandatory** for ePHI processing in production; HIPAA audit-trail compliance is the production gate.
- Calculator cascade RAM 384 GB → 320 GB (dev hardware spec correction; production has 768 GB so does not apply).
- `cluster_sizing_tool.html` NUMA + AQE toggles landed (production has dual-NUMA so the NUMA-pinning advisory is more material; AQE toggles apply to both).

**Companion documents bumped (cross-references that this document should refresh during the production pass):**
- `MSB-PMC01_airflow_host_briefing_v1.1.md` → `_v1.2.md` (Nginx correction)
- `Phases_Critical_Path_Development_v1.4.md` → `_v1.5.md`
- All cross-references in production fork should be updated v1.2 → v1.5 when the body is revised

**Production-specific items still to land** (forward-looking, not v1.5-sync):
- Production hardware spec rewrite (64c/768GB/9× 3.2TB NVMe vs dev's 32c/320GB/7× 3.84TB)
- Dual-NUMA topology implications for VM sizing
- HA SLO definitions
- Backup/DR architecture
- Production-grade audit logging (ties to P2.9)
- Production Phase 4 sequencing (per SOW)

## Update 2026-05-08 — additional items from the review punch-list

The 2026-05-08 review of the v1.5 cycle surfaced material for the production-side revision pass:

**Phase 2 closure status (Dev — applies to production-side as cumulative learning):**
- BLOCKER.1, P0.0, P0.1a, P0.4 (pre-req), P0.7 closed 2026-05-08 on the dev cluster
- P0.1b (Worker VM OS install + base config) still open on dev
- BLOCKER.3 split 2026-05-08 into 3a (hardware compliance — vendor-claimed-closed pending verification) + 3b (software/network compliance — open)
- Pool validation testing + IP blocks for vendor-created VMs closed 2026-05-08 via Sean's email exchange

**Production-side implications:**

1. **msb-pmc04 third-cluster proposal** (non-blocking) — under consideration to add to the Spark cluster infrastructure, removing msb-pmc01 from the security equation. Affects production architecture: orchestration / Airflow / monitoring services would migrate from msb-pmc01-04 to msb-pmc04. Bastion VM also migrates. Material for the production-side architecture diagram revision. See dev CP v1.5 § BLOCKER.4 msb-pmc04 note + `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Status (2026-05-08 — msb-pmc04 third-cluster idea captured).

2. **HIPAA scope split (BLOCKER.3 → 3a + 3b)** — production must close both sub-gates plus the dev-side three-pillar work before any production ePHI processing. Production-side adds: drive-encryption posture verification (3a) on production hardware; full Spark RPC + TLS + Web UI ACL build-out (3b) on production cluster.

3. **Production HIPAA-driven items NOT yet captured anywhere** (from the 16-point production architecture questionnaire in `phases/development/phase2/Incoming/Vario\us_Email/Hi Rohn,.md`):
   - **Q4 — Existing secrets management platform** (Vault/Secrets Mgr/Key Vault/CyberArk) — affects whether production deploys a new Vault or extends existing
   - **Q5 — PKI / internal CA for TLS** — production requires TLS on all Spark RPC, Ceph RGW, service-to-service
   - **Q8 — PAM solution** (BeyondTrust/CyberArk) for privileged server access
   - **Q9 — Existing VPN / ZTNA for admin access** — affects WireGuard / remote service host design
   - **Q11 — Formal HIPAA Risk Assessment** per § 164.308(a)(1)
   - **Q12 — BAAs with Snowflake + Azure** — REQUIRED before PHI flows; gates production go-live; not in any CP doc
   - **Q13 — Incident Response / breach notification runbook** per § 164.308(a)(6)
   - **Q14 — Vulnerability scanning / patch management process**
   - **Q15 — On-call / IR capability** — affects monitoring alert design
   - **Q16 — Application-level backup/DR** (Airflow metadata DB, Vault, Ranger policies) — Ceph HA covers storage but not app state

   These are production-only / production-stricter items not present in the dev CP. Production-side revision pass should add them as a "Production Pre-Flight Gates" section or equivalent.

4. **Phase 2 vendor sign-off claim under review** — vendor declared Phase 2 completed under their framing on 2026-05-08; user is verifying against the SOW's Phase 2 outline before signing off (HIPAA was bundled under their Phase 2 declaration; user questions whether it covers full three-pillar HIPAA or just hardware-level LUKS). This affects the production-side fork's understanding of what "Phase 2" means in the SOW context.

5. **NIC redundancy (Sean) for dev cluster** — listed in the email thread Apr 21 action items + Section 2 summary. Production-side equivalent: NIC redundancy on production nodes; needs explicit task on the production fork's revision pass.

6. **Apache Ranger evaluation** — for Spark-level RBAC + column masking on PHI vs. de-identified data. Mentioned in dev TODO; production implementation gates Q7 (RBAC) of the questionnaire.

---

## Update 2026-05-11 — vendor isolation framework v0.2 circulated; production-side scope material

The Vendor Access Isolation Framework was finalized as **v0.2** (`security/Document/Vendor_Access_Isolation_Framework_v0.2.md`, on-site only) and circulated to fqdn Network (Sean Klette, Austin), Cyber (Paul Barber), CIO (Rob Ball), AD admins, and Michelle on 2026-05-11 afternoon. Email body sent + sanitized rendering committed to git audit trail at `ready_for_delivery/vendor_access_framework_email_body_2026-05-11.html` (commit `be1e4ae`).

**Production-side implications of v0.2 (material for the production revision pass):**

1. **msb-pmc02 (production) is explicitly in vendor scope** — the framework places production alongside dev and the new msb-pmc04 inside a unified Spark Cluster Network (VLAN 37). This is **scope expansion #1** vs. the 2026-05-06 CIO directive; CIO risk-acceptance is now pending. **Material for production-side BLOCKER.4 equivalent:** the question "does production allow vendor access at all post-handover" (raised in the 2026-05-08 update above) is partially answered for the install / configuration phase — yes, vendor needs access. Whether that scope persists past handover (Phase 4) is a separate decision still owed.

2. **msb-pmc04 committed as third Spark cluster** — promoted from "under consideration" (2026-05-08) to **committed** on 2026-05-11. msb-pmc04 hosts Airflow + ancillary services (Grafana / Prometheus / Loki, Bastion, Ansible source) + additive Ceph cluster + CephFS / RGW frontend gateways. The msb-pmc01 orchestration cluster is being retired; services migrate to msb-pmc04. **Production-side architecture impact:** orchestration and monitoring services that touch production now target msb-pmc04, not msb-pmc01-04. Production-fork architecture diagram revision pass must reflect this.

3. **VLAN 37 unified across msb-pmc02 / 03 / 04** — single Spark Cluster Network spans all three Spark clusters. Supersedes the earlier "msb-pmc03 sole tenant of 37/38/39 + new VLAN 10 chokepoint" candidate from 2026-05-06. **Production-side implication:** prod cluster joins the same L2 broadcast domain as dev. Network sizing (IP space) must accommodate prod hosts + VMs. Comfortably within /24 today; expand to /23 if host/VM density outgrows envelope.

4. **Dev ↔ Prod cluster isolation explicitly deferred** — **scope expansion #2** vs. the 2026-05-06 CIO directive. v0.2 states: "Facilitating vendor access across all three clusters is the priority; tighter dev/prod posture is deferred." For the production fork, this means **no L2 / L3 separation between dev and prod at this design stage** — both share VLAN 37, both reachable from the same Horizon pool, both with the same vendor allow-list. CIO risk-acceptance is pending. Production-fork must note this as a deferred-control item to revisit before production ePHI processing begins.

5. **Primary / secondary control framing** — Austin's network firewall (single chokepoint at pool's default gateway) is **primary**; host-level `nftables` (Proxmox / Debian) + `firewalld` (RHEL 9.4 VMs) + vendor sudo carve-out is **defense-in-depth secondary**. Production hosts will adopt the same posture; production-fork should mirror the control structure when its body is revised.

6. **Vendor accounts and groups provisioned in the Horizon pool** — Michelle's bridge sub-task **closed 2026-05-11**. Same pool serves both dev and production vendor work. No further provisioning action needed; pool credentials work for production access too once the broader gate clears.

**Awaiting team responses (cross-doc — applies to both forks):**

- **Sean Klette + Austin (Network):** confirm VLAN 37 can be made a single fabric-wide L2 broadcast domain spanning msb-pmc02 + 03 + 04; confirm pool-egress allowlist content matches the framework's Enterprise Services section
- **Paul Barber (Cyber):** endorse the framework or surface gaps; confirm host-firewall pattern; sign off on vendor sudo carve-out approach
- **Rob Ball (CIO):** risk-accept the 3 scope expansions vs. the 2026-05-06 directive: (1) msb-pmc02 in vendor scope; (2) Dev↔Prod isolation deferred; (3) msb-pmc04 in vendor scope. **All three have production-side implications.**
- **fqdn AD admins:** confirm vendor AD reach approach — DC-pool-wide (any-of-7) vs. steered (e.g., MSB-RO read, MSB-RW writeback)
- **Ksolves:** confirm OPSWAT device-posture client installed across all vendor devices

**Companion documents bumped 2026-05-11:**

- `MSB-PMC01_airflow_host_briefing_v1.2.md` → `_v1.3.md` (msb-pmc01 retirement / msb-pmc04 commitment)
- `CP_HIPAA_Compliance_v1.0.md` → `_v1.1.md` (HIPAA scope split: 3a closes Phase 2, 3b reassigned to Phase 3; see below)
- `Phases_Critical_Path_Development_v1.6.md` updated in place with 2026-05-11 progress (framework v0.2 circulated; BLOCKER.3a closed; BLOCKER.3b → Phase 3; VLAN 37 recognition issue)
- `phases_critical_path_development_tracker_v1.6.html` updated in place to mirror the v1.5 status changes
- This document (production fork) updated 2026-05-11 with v0.2 production-side implications

---

## Update 2026-05-11 (EOD) — Phase 2 audit closures + HIPAA scope split + VLAN 37 recognition issue

**Production-side implications:**

1. **HIPAA scope split — Phase 2 hardware compliance (BLOCKER.3a) vs Phase 3 software/network compliance (BLOCKER.3b).** Per joint fqdn–Ksolves decision 2026-05-11, the HIPAA scope splits across phase boundaries. **Production-side reading:**
   - **Phase 2 hardware compliance** for production = drive-encryption posture on production hardware (768 GB RAM, 64-core nodes, 9× 3.2 TB NVMe — note hardware differs from dev). When production cluster is provisioned, the same LUKS double-encryption issue should be checked at install time. **Mitigation:** apply the dev-cluster lesson — direct vendor to use existing hardware encryption only (no software LUKS layer on hardware-encrypted drives).
   - **Phase 3 software/network compliance** = transmission security, Web UI ACL, SSE on Ceph buckets, local Spark I/O encryption, Kerberos service auth. **Production-side reading:** production cluster must satisfy the full Phase 3 HIPAA posture before ePHI processing. Canonical scope tracked in `CP_HIPAA_Compliance_v1.2.md` (which now scopes Phase 3 work for both dev and production).

2. **Phase 2 audit § 13 items all closed (dev cluster).** Production-side equivalent: same audit script should run on the production cluster post-install. Action items the script flags (mclock IOPS calibration, RGW server-side tuning, OSD device class, LUKS posture, pool naming intent, CephFS MDS state, Ceph version) need to be verified on production hardware before production sign-off.

3. **VLAN 37 Proxmox recognition issue (NEW 2026-05-11) — RESOLVED 2026-05-12 via re-segmentation.** The recognition problem on the dev cluster was resolved by moving cluster VMs to **VLAN 27 (10.1.27.0/24)** rather than fixing VLAN 37. **Production-side implication:** when production (msb-pmc02) VMs are provisioned, they will also land on VLAN 27 — same VLAN, same /24, IPs to be assigned. Per Sean Klette's 2026-05-12 email thread, all three Spark clusters (msb-pmc02, msb-pmc03, msb-pmc04) end up in VLAN 27 as a phased rollout. Cross-reference: main CP v1.5 § BLOCKER.4 + `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Status (2026-05-12 morning) + framework v0.3 draft at `security/Ready_For_Review/`.

3a. **VLAN topology pivot — framework v0.2 &rarr; v0.3 (NEW 2026-05-12).** v0.2's unified-VLAN-37 model is superseded by v0.3's two-layer model: **L3 firewall policy** restricting VLAN 157 (Ksolves Horizon pool) &rarr; VLAN 27 (Spark cluster VMs), **plus remote-domain AD permissions** as user-level authorization. **Production-side implication:** the same two-layer model will apply to production. The three CIO scope expansions (msb-pmc02 in vendor scope; Dev↔Prod isolation deferred; msb-pmc04 in vendor scope) are substantively unchanged — only the VLAN labels shift.

4. **Phase 3 work begun (<vendor-engineer>).** VM-config tasks initiated on dev cluster 2026-05-11. Production-side: production Phase 3 work is sequenced after dev Phase 3 completes (per the SOW phase ordering). The production CP body revision pass should mirror dev Phase 3 task taxonomy when it stabilizes.

---

## Document Overview

This document is the Critical Path for the fqdn **Production** Spark cluster (`msb-pmc02`). It is structurally a sibling to the development cluster's Critical Path (`phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md`), but the two clusters have **distinct phase progressions** — completion on dev does NOT imply completion on prod.

**Current production-cluster state (as of 2026-05-12):**

- **Phase 1 (Planning & Discovery):** NOT YET STARTED. Production-specific planning has not been initiated. Some dev-cluster planning artifacts will inform production scope (e.g., HIPAA framework, vendor configuration baseline, audit-script template), but production discovery, sizing, and architecture have not been done.
- **Phase 2 (Implementation):** NOT YET STARTED. Production hardware not yet provisioned; production VMs not created.
- **Phase 3 (Configuration / Bring-up):** NOT YET STARTED. Awaits Phase 2 completion.
- **Phase 4 (Production Handover, per SOW):** NOT YET PLANNED. Awaits Phase 3 completion.

The four "Update 2026-05-XX" sections at the top of this document capture **dev-cluster events that have production-side implications** — they are forward-looking notes to inform production planning when it begins, not retroactive status of the production cluster itself.

### Methodology

When production planning starts, this document will be revised to:

- Define production-specific scope (hardware spec confirmation, traffic profile, HA SLOs, backup/DR architecture)
- Mirror dev's phase taxonomy (BLOCKERS + P0.x + P1.x + P2.x) where applicable, but ONLY where production conditions match dev — items will not be marked closed/completed on the production side merely because they closed on dev
- Add production-only items (per the 16-point production architecture questionnaire — see Pre-Flight Gates section below)
- Cross-reference dev as a parallel sibling, not inherited parent
- Add a Production Phase 4 (Handover) sequence per the SOW

For now, the body below is a placeholder scaffold; phase-specific task lists will be populated when production planning begins.

---

## Table of Contents

- [Phase 1 — Planning & Discovery](#phase-1-planning-discovery)
- [Phase 2 — Implementation](#phase-2-implementation)
- [Phase 3 — Configuration / Bring-up](#phase-3-configuration-bring-up)
- [Phase 4 — Production Handover](#phase-4-production-handover)
- [Production Pre-Flight Gates (HIPAA-driven; production-only)](#production-pre-flight-gates)
- [Reference Documents](#reference-documents)
- [Revisions](#revisions)

---

<a id="phase-1-planning-discovery"></a>

## PHASE 1 — Planning & Discovery

**Status: NOT YET STARTED (production cluster).**

Production-cluster Phase 1 (planning + discovery + sizing + architecture) has not been initiated. When started, this phase will produce:

- Production traffic profile (peak / sustained / burst expectations beyond the dev pilot)
- Production hardware spec confirmation (expected per dev/prod fork notes: 64-core nodes, 768 GB RAM, 9× 3.2 TB NVMe; dual-NUMA topology)
- Production-specific architecture decisions (HA SLO definitions, backup/DR architecture, audit logging at production scale)
- Production-side adaptation of the vendor configuration baseline (Ksolves_Spark_YARN_Config_v1.0.pdf sections relevant to production)
- NIC redundancy decision on production hardware (Update 2026-05-08 item 5)

Inputs that will inform production Phase 1 — these are already in hand from dev-side work and listed in the "Update 2026-05-XX" sections above:

- HIPAA scope split (Phase 2 hardware / Phase 3 software-network) per the 2026-05-11 joint decision
- VLAN topology pivot (VLAN 27 cluster + VLAN 157 Ksolves Horizon pool) per the 2026-05-12 Network team email thread
- Vendor Access Isolation Framework v0.3 (applies to both clusters)
- Vendor configuration baseline (Ksolves_Spark_YARN_Config_v1.0.pdf)
- Audit-script template + outputs from dev cluster
- LUKS-double-encryption lesson learned (don't apply software LUKS on already-hardware-encrypted drives)

Reuse vs. revise will be assessed at Phase 1 start.

---

<a id="phase-2-implementation"></a>

## PHASE 2 — Implementation

**Status: NOT YET STARTED (production cluster).**

Production-cluster Phase 2 (infrastructure provisioning) has not been initiated. Provisioning will follow the dev-cluster taxonomy where production conditions match. Anticipated scope when started:

- Network / firewall / VLAN posture — likely VLAN 27 per the 2026-05-12 re-segmentation; production VMs assigned IPs in `10.1.27.0/24` once provisioned
- Proxmox cluster bootstrap on production hardware
- Ceph cluster bootstrap (production scale; same vendor pattern as dev — Squid 19.2.3, RGW, CephFS standby MDS)
- Worker VM provisioning on production hardware (counts + sizing per production traffic profile)
- YARN ResourceManager + History Server provisioning
- RHEL 9.4 license activation on production VMs
- Hardware encryption posture (LUKS verification — apply dev-cluster lesson re: avoiding double-encryption)
- NIC redundancy (Sean) on production nodes

Phase 2 sign-over verification on production will mirror the dev-cluster checklist (post-VM-creation cluster audit, VLAN 27 connectivity verification, RHEL licensing, hardware encryption, vendor baseline conformance, audit-trail capture). Production-specific additions:

- HA SLO acceptance test
- Backup/DR readiness verification
- Production traffic-profile validation (vs. dev pilot)

**Cross-reference**: dev-side Phase 2 sign-over verification checklist is in development on the dev CP (see `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md` — current focus area as of 2026-05-12 afternoon).

---

<a id="phase-3-configuration-bring-up"></a>

## PHASE 3 — Configuration / Bring-up

**Status: NOT YET STARTED (production cluster).**

Production-cluster Phase 3 (Spark / YARN / Hadoop installation + HIPAA software/network compliance + integration + bring-up) has not been initiated. Scope will mirror the dev-cluster Phase 3 taxonomy where production conditions match:

- Spark 3.5.3 + YARN 3.4.1 + Hadoop 3.4.1 installation per vendor config baseline
- HIPAA software/network compliance per `CP_HIPAA_Compliance_v1.2.md` — Phase 3 scope items: transmission security (§ 8.1), Web UI ACL (§ 8.3), SSE on Ceph buckets, local Spark I/O encryption, Kerberos service auth
- Custom javax servlet filter for Spark Web UI / History Server ACL (§ 8.3) — fqdn-side vs vendor-side ownership pending resolution on dev (HIGH priority letter re-sent 2026-05-12)
- Apache Airflow 2.10.4 deployment + DAG integration (production DAGs may differ from dev pilot)
- Apache Ranger evaluation + integration for PHI/de-identified entitlement model (drives column masking)
- RGW server-side tuning (per vendor doc § 6.4) — applied on dev 2026-05-12; production equivalent at Phase 3 install time
- Sample-job validation at production scale (mirroring dev's P1.8 "5 production sample jobs" pattern but with production traffic profile)

**Phase 3 dependencies on dev cluster:** lessons learned during dev Phase 3 will inform production Phase 3 (e.g., javax filter ownership outcome, Apache Ranger configuration, audit-trail capture patterns). Production Phase 3 should not start until dev Phase 3 has surfaced and resolved the major unknowns.

---

<a id="phase-4-production-handover"></a>

## PHASE 4 — Production Handover

**Status: NOT YET PLANNED (production cluster).**

Production-cluster Phase 4 (formal handover from vendor + go-live + ePHI processing authorization) is sequenced per the SOW and has not been planned in detail. Scope to be defined when Phase 3 closes. Will include at minimum:

- Vendor cluster sign-over (formal acceptance ceremony)
- HIPAA Risk Assessment per § 164.308(a)(1) — completed and signed by fqdn Compliance
- Business Associate Agreements (BAAs) with Snowflake + Azure — REQUIRED before any PHI flows (Update 2026-05-08 item 3 flagged this is not currently in any CP doc)
- Incident Response / breach notification runbook per § 164.308(a)(6)
- Vulnerability scanning / patch management process — operationalized for production
- On-call / IR capability — staffed and tested
- Application-level backup/DR (Airflow metadata DB, Vault, Ranger policies) — Ceph HA covers storage at the cluster level but not app state
- Production go-live and first ePHI processing run
- Vendor post-handover access decision (raised in v1.5 sync 2026-05-07; partially answered in 2026-05-11 update — install/configuration scope confirmed; post-handover scope still open)

---

<a id="production-pre-flight-gates"></a>

## Production Pre-Flight Gates (HIPAA-driven; production-only)

These items are surfaced from the 16-point production architecture questionnaire (Update 2026-05-08 item 3 above) and are production-only (not in the dev CP). They block ePHI processing in production and must close before or during Phase 4:

| # | Item | Production-side gate |
|---|---|---|
| Q1 | Centralized log management (SIEM) | HIPAA § 164.316(b)(2) 6-year audit-log retention. Platform TBD (Splunk / OpenSearch / Datadog / Wazuh + ELK). |
| Q4 | Secrets management platform | CyberArk confirmed in use at fqdn corporate; integration with Spark/Airflow/Ceph stack TBD. |
| Q5 | Internal CA / PKI for TLS | Production requires TLS on all Spark RPC, Ceph RGW, service-to-service. Corporate PKI scope TBD. |
| Q7 | PHI vs. de-identified entitlement model | Drives Apache Ranger column-masking policies. Requires a one-page entitlement matrix mapping AD/Okta groups to data tiers. |
| Q8 | PAM solution for privileged server access | BeyondTrust / CyberArk — fqdn Cyber/Security to confirm. |
| Q9 | Existing VPN / ZTNA for admin access | Affects WireGuard / remote service host design. |
| Q11 | Formal HIPAA Risk Assessment | Per § 164.308(a)(1). |
| Q12 | BAAs with Snowflake + Azure | **REQUIRED before PHI flows.** Not currently in any CP doc. Production go-live blocker. |
| Q13 | Incident Response / breach notification runbook | Per § 164.308(a)(6). |
| Q14 | Vulnerability scanning / patch management process | Operationalized for production. |
| Q15 | On-call / IR capability | Affects monitoring alert design. |
| Q16 | Application-level backup/DR | Airflow metadata DB, Vault, Ranger policies — Ceph HA covers storage but not app state. |

**Draft responses being developed at:** `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` (1.0 draft pending Cyber/Security + Networking input).

---

<a id="reference-documents"></a>

## Reference Documents

**Production-cluster-specific:**

- This document — `phases/production/phase2/Document/Phases_Critical_Path_Production_v0.1.md`
- Production architecture questionnaire responses (draft) — `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md`

**Cross-references to dev cluster (parallel, NOT inherited):**

- Dev Critical Path — `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md`
- Dev Critical Path visual tracker — `phases/development/phase2/Document/phases_critical_path_development_tracker_v1.6.html`
- HIPAA sub-project (applies to both clusters at Phase 3 — single canonical scope) — `phases/development/phase2/Document/CP_HIPAA_Compliance_v1.2.md`
- Okta sub-project (applies to both clusters) — `phases/development/phase2/Document/CP_Okta_v1.1.md`
- Airflow host briefing (msb-pmc01 → msb-pmc04 supersession 2026-05-12) — `phases/development/phase2/Document/MSB-PMC01_airflow_host_briefing_v1.3.md`
- Vendor configuration baseline — `phases/development/phase2/Document/Ksolves_Spark_YARN_Config_v1.0.pdf`
- SOW Phase timeline status — `phases/development/phase2/Document/SOW_timeline_status.md`

**Security context (on-site only; NOT in git):**

- Vendor Access Isolation Framework v0.3 — `security/Document/Vendor_Access_Isolation_Framework_v0.3.md`
- Vendor isolation planning note — `security/Notes/vendor-access-isolation-plan_2026-05-06.md`

**SOW reference (in Incoming, gitignored):**

- Mar 16 Scope of Work — vendor-provided SOW PDF, in `phases/development/phase2/Incoming/Archive/` (filename includes `Mar16th_Scope_of_Work` — vendor filename retained as-supplied per project rule on Incoming/ files)

---

<a id="revisions"></a>

## Revisions

| Date | Summary |
|---|---|
| 2026-04-27 | Initial v0.1 cut. Forked from `Phases_Critical_Path_Development_v1.2.md` as a starting-point fork; body inherited from dev plan with header noting "DRAFT — pending production-specific revision". |
| 2026-05-08 | v1.5-sync header refresh — dev-side advanced to v1.5; this doc's body still reflected v1.2 fork point. Added v1.5 Sync Status section + Update 2026-05-08 section capturing dev events with production-side implications (msb-pmc04 third-cluster proposal, HIPAA scope split, 10 production-only items from the 16-point questionnaire, vendor sign-off claim under review, NIC redundancy, Apache Ranger). |
| 2026-05-11 | Update 2026-05-11 section added — vendor isolation framework v0.2 circulated; six production-side implications (msb-pmc02 in vendor scope, msb-pmc04 committed, VLAN 37 unified, dev↔prod isolation deferred, primary/secondary control, vendor accounts provisioned). |
| 2026-05-11 (EOD) | Update 2026-05-11 (EOD) section added — Phase 2 audit closures, HIPAA scope split (3a closes Phase 2 / 3b → Phase 3), VLAN 37 recognition issue. Companion document `CP_HIPAA_Compliance_v1.0.md` → `_v1.1.md`. |
| 2026-05-12 | Update content (folded into Update 2026-05-11 EOD section) — VLAN topology pivot framework v0.2 → v0.3 (VLAN 27 cluster + VLAN 157 Ksolves Horizon pool + L3 firewall + remote-domain AD permissions). |
| 2026-05-12 (clean-slate body rewrite) | **Body rewrite — clean slate for the production cluster.** Stripped dev-inherited body content (Document Overview, Methodology, TOC, all Phase 1/2 task sections marked COMPLETED or with dev-specific BLOCKER.X / P0.x / P1.x / P2.x details). Replaced with a production-specific scaffold: 4 phases (1–4) all marked NOT YET STARTED / NOT YET PLANNED, production-specific Pre-Flight Gates section (Q1–Q16 from the architecture questionnaire), cross-references to dev as parallel sibling not inherited parent. Kept the v1.5 Sync Status + Update 2026-05-XX sections at the top as forward-looking dev-event context for production planning. Status line updated to reflect clean-slate. Restructured under the new `phases/production/phase2/` directory layout (per the 2026-05-12 phases/ restructure commit `2e5fa12`). |
