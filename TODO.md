#  Master TODO — All Contexts
_Last updated 2026-05-07_

---

## PHASE 1 — PRIORITY ITEMS

### BLOCKING — Ksolves Remote Access (Phase 1A re-opened 2026-04-30)

- [x] [Phase1] [correspondence] Establish Ksolves Webex desktop access for Phase 1A interim infrastructure provisioning **(closed 2026-04-29 — Ksolves connecting via Webex)** — **superseded; reopened 2026-04-30 due to Webex Linux/Windows remote-control limitation, see entry below**
  - Phase 1A (interim): Shared Webex desktop with fqdn team oversight — **was active; now blocked**
  - Phase 1B (permanent): VMware Horizon VDI — still pending fqdn Cyber Security approval (tracked under Pending Tasks > Correspondence; non-blocking for Phase 1/2 work)
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.1

- [x] [Phase1] [correspondence] **Phase 1A re-opened 2026-04-30** — Ksolves must provision Windows host (vendor-side, in India) to run Webex Desktop client with remote control enabled
  - **Cause:** Webex's Linux desktop client does not support remote control of a Windows Webex share (verified by user — set up Linux Webex and confirmed remote-control unavailable). Ksolves is a Linux shop; fqdn shares from Windows. Without a Windows host on Ksolves' side, Phase 1A cannot proceed.
  - **Vendor responsibility:** Ksolves provisions and maintains the Windows host on their side (in India)
  - Vendor sub-tasks:
    - [x] Ksolves provisions Windows host capable of running Webex Desktop with remote-control support
    - [x] Ksolves installs and licenses Webex Desktop on the Windows host
    - [x] Joint connectivity test: Ksolves' Windows host → fqdn-shared Windows Webex session, with remote-control verified
    - [x] Ksolves notifies fqdn when Windows host is ready, so Phase 1A kickoff can be scheduled
  - **Critical path impact:** All Phase 2 infrastructure provisioning is gated on this until vendor's Windows host is operational. Halt Period decision point (2026-05-04) may need re-evaluation depending on vendor turnaround.
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.1 (Hardware Prerequisite)

### Security — Credential Rotation (URGENT, 2026-05-01)

- [x] [Phase1] [security] **🚨 Rotate exposed iLO administrator credentials** — the iLO admin password used by Ksolves on `msb-pmc03-01-ilo` (10.1.32.64) appears in plain text inside the vendor's bash history. Rotate the iLO password on all three msb-pmc03 nodes; if the same credential is reused for any corporate-AD account, rotate that as well; scrub `~/.bash_history` on each node (and any vendor workstation copies); coordinate with corporate IT.
  - Source: `phases/phase2/development/Incoming/ksolves_node1_commands.txt` (occurrences at lines 82–87, 121, 138–142, 168–172)

### Vendor Configuration Baseline — Ksolves Spark & YARN Config v1.0 (2026-05-04)

Ksolves delivered an authoritative configuration document on 2026-05-04 (`phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf`) based on actual DEV environment data (`csv_file_sizes.xlsx`). It establishes the Spark 3.5.3 / YARN 3.4.1 config baseline, answers prior P0.0a items, and surfaces several new decisions.

**Decisions captured 2026-05-05:**

- **Cluster size — finalized at 3 nodes.** Vendor recommended +1 node for 2-concurrent-job operation; user decided 3 nodes only (budget constraint). The vendor's "feasible-but-zero-buffer" SLA analysis at 3 nodes is the accepted posture.
- **GZIP non-splittability mitigation** — owner: **Development team**. Choose 1 of 4 options from § 2: pre-split upstream (best) / bzip2 codec / raw uncompressed CSV / post-read repartition (last resort).
- **Hadoop 3.4.1 vs Spark 3.5.x classpath** — owner: **Vendor (Ksolves)** (they're doing the install). Captured for tracking only; no fqdn-side action.
- **Ceph RGW server-side tuning** (`rgw_thread_pool_size 512`, `rgw_max_concurrent_requests 1024`) — owner: **Vendor (Ksolves)** until cluster sign-over. Captured for tracking only.
- **HIPAA compliance** — forked into a separate sub-project: `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` (forthcoming). Main Critical Path gains a BLOCKER pointing to it. **NVMe disks are already LUKS-encrypted on this side** — must remind Ksolves before they start Spark install so they don't redo it.
- **RAM hardware update** — RAM/node spec'd at **320 GB** (was 384). CLAUDE.md hardware reference updated; calculator defaults to follow.

**New tasks (open):**

- [x] [Phase1] [correspondence] **GZIP mitigation strategy decision** — Development team picks the upstream/codec/raw/repartition option. Vendor recommends pre-split upstream as the zero-SLA-risk path. See `Ksolves_Spark_YARN_Config_v1.0.pdf` § 2.
- [x] [Phase1] [correspondence] **Notify Ksolves — NVMe disks already LUKS-encrypted** — vendor's HIPAA guide (§ 8.2) recommends LUKS on NVMe drives 4–7. They are already encrypted. Communicate before Spark install so they don't reformat.
- [ ] [correspondence] **SOW Change Order coordination** — capture HIPAA scope addition + 3-node decision (no additional node) + vendor configuration guide rollover. Coordinate with Mirali.
- [x] [calculators] **Update calculator defaults** — RAM/node 384 → 320 GB ✅ (cluster_sizing_tool, 2026-05-05); daily ingest default 5 TB → ≤1.5 TB ✅ (cluster_sizing_tool, 2026-05-05); embed repartition formula `target_partitions = max(24, ceil(compressed_csv_mb / 50))` _(pending — math reference + phase1 model)_; add `spark.sql.shuffle.partitions = 4096` to reference docs _(pending — math reference)_; cascade RAM 384 → 320 GB through `dev_cluster_math_reference.html` (337 GB hard ceiling → 273 GB recompute), `dev_cluster_phase1_model.html` (×2 — phase1 + phase2 deliverables), `dev_calculator_guide.html` _(pending — defer to separate job, downstream values need recomputation)_.
- [x] [calculators] **Add NUMA pinning + AQE enable/disable toggles to `cluster_sizing_tool.html`** — per user direction 2026-05-05 (Batch 3 deferred). NUMA pinning toggle should reflect single-NUMA dev hardware (one CPU socket = 32 cores) so the constraint may be informational rather than gating. AQE toggle should align with `spark.sql.adaptive.enabled` and surface the implications for shuffle.partitions when AQE is off (vendor doc § 4 / § 7.2).
- [ ] [Phase1] **Bump Phases_Critical_Path_Development to v1.4** — incorporate vendor config baseline, GZIP P0, Hadoop classpath / Ceph RGW tuning as vendor-owned tasks, HIPAA BLOCKER pointing to sub-project, 3-node decision finalization. _(In progress — see batch 2.)_

**Cross-references:**
- `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` — the vendor doc itself
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md` — main CP (cut 2026-05-07)
- `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` — HIPAA sub-project

### Production Architecture Prep — Ksolves Email + Apr 27–May 01 Status (forwarded 2026-05-06)

vendor lead (Ksolves) forwarded a multi-section email on 2026-05-06 that bundles: (a) a Phase 2 / VDI status update, (b) the Apr 27–May 01 weekly Ksolves status report, (c) the 16-point production architecture questionnaire, (d) a 4/21/26 daily-meeting summary, and (e) two architecture diagrams (dev + prod). Source email and supporting markdown are at `phases/phase2/development/Incoming/Vario\us_Email/Hi Rohn,.md`. Diagrams promoted to `phases/phase2/development/reference_images/`.

**Action items assigned to Rohn (with attribution):**

- [ ] [correspondence] **Review and confirm production architecture diagram and update as needed** — source: vendor lead (Ksolves), email forwarded 2026-05-06. Reference: `phases/phase2/development/reference_images/prod_data_flow_diagram_2026-05-06.png`.
- [ ] [correspondence] **Validate production infrastructure requirements and complete architecture inputs** — source: vendor lead (Ksolves), email forwarded 2026-05-06. Companion to the 16-point questionnaire response doc (in Ready_For_Review).
- [ ] [correspondence] **Define centralized logging approach + retention policy for production** — Splunk vs ELK/Wazuh vs Datadog; HIPAA § 164.316(b)(2) requires 6-year minimum with WORM on the audit bucket. Source: vendor lead (Ksolves), questionnaire Q1–Q3, email forwarded 2026-05-06. Coordinate with fqdn corporate IT and Cyber/Security. **Linked CP item below.**
- [ ] [correspondence] **Confirm IAM/RBAC model — specifically PHI vs de-identified entitlement boundaries** — directly informs Apache Ranger column-masking policy. Source: vendor lead (Ksolves), questionnaire Q7, email forwarded 2026-05-06. Coordinate with fqdn Cyber/Security.
- [ ] [correspondence] **Evaluate Apache Ranger or equivalent for Spark-level access control + compliance** — source: vendor lead (Ksolves), email forwarded 2026-05-06. Coordinate with fqdn Cyber/Security. Already named as the column-masking option in `CP_HIPAA_Compliance_v1.0.md`; this item is the formal evaluation/sign-off.
- [x] [correspondence] **Test and complete remote access setup for environment** — partner: vendor engineer (Ksolves). Source: vendor lead (Ksolves), email forwarded 2026-05-06. Tracks alongside BLOCKER.1; this is the user-facing verification once vendor's Windows host is live.
- [ ] [correspondence] **Confirm production baseline configuration for resource sizing** — source: vendor lead (Ksolves), email forwarded 2026-05-06. Owns the production calculator inputs once dev cluster scales settle.
- [ ] [correspondence] **Share updated production configuration details for parallel work planning** — joint with vendor lead (Ksolves). Source: vendor lead, email forwarded 2026-05-06. Likely a shared spreadsheet or doc exchange.
- [ ] [correspondence] **Send network-related questions and requirements to fqdn infrastructure/network team** — source: vendor lead (Ksolves), email forwarded 2026-05-06. Coordinate with Sean Klette + the network team.

**Architectural constraints captured 2026-05-06 (do not lose):**

- **Edge/Gateway VM topology — not feasible inside the cluster.** The Ksolves email proposes an Edge/Gateway VM inside Proxmox to bridge MTU 9000 (cluster) ↔ MTU 1400 (remote path) and front Spark submissions for the remote Airflow host. **fqdn lacks spare cluster resources to host this as a VM on the cluster** (3-node cluster sized to 1 concurrent Spark job, no headroom). MTU mismatch issue itself was resolved 2026-05-06 by fqdn networking team, so the immediate driver is gone. If MTU bottleneck recurs or a similar architecture decision arises, the Edge VM would need to live off-cluster (MSB-PMC01 or a dedicated host) — capture this as a constraint when revisiting.

**Pending Critical Path additions (queued for Phases_Critical_Path_Development v1.5 bump):**

- [ ] [Phase1] **CP v1.5 cut 2026-05-07** — autonomous bump cycle landed in commits `dccfdfb` (markdown), `d85d565` (tracker HTML), `21db11a` (RAM 384→320 cascade across math reference + phase1+2 models + calculator guide), `adb7ada` (cluster_sizing_tool NUMA + AQE toggles). Companion file `MSB-PMC01_airflow_host_briefing_v1.1` → `_v1.2` (Nginx correction). Cross-references in CP_HIPAA / CP_Okta / phase1 README / phase1 ksolves-april24-status-review / phase1 vendor questions / SOW_timeline_status all bumped. Changelog `Phases_Critical_Path_Development_v1.4_changelog.md` and v1.5 PDF regen pending. **Comprehensive list of what v1.5 picked up (left for verification):**
  - **Tracker HTML overhaul** — `phases_critical_path_development_tracker_v1.4.html` still has the deferred-content banner from the v1.3→v1.4 bump. Needs new section cards for BLOCKER.3 (HIPAA), P0.0a closure status, P0.0b (GZIP mitigation), P0.3 closure status, P0.6 (Ceph RGW tuning). ~200–250 lines of new/updated HTML.
  - **BLOCKER.1 refinement** — clarify the cause as NUC-reliability in Ksolves' DC, plus the interim Webex hosting arrangement (note: NUC issue resolved 2026-05-06).
  - **NEW: Vendor-isolation Phase 1B security gate** — capture as a parallel gate to BLOCKER.1, pointing to `security/Notes/vendor-access-isolation-plan_2026-05-06.md` and the distribution brief at `security/Document/vendor_security_design_overview_v1.0.md`. Both new gates ({vendor-isolation design + Cyber endorsement, CIO sign-off}) must close before Phase 1B VDI access goes live.
  - **NEW: Horizon pool stand-up (2026-05-07)** — Jason built the pool + UAG access; Austin set firewall-style policies (DNS/AD/UAG/CS's allowed; rest blocked). One CIO sub-task complete pending validation. Adds new gates to the Phase 1B critical path: pool validation testing (Sean + Rohn), Sean+Austin sync on pool↔cluster-side design layering, Ksolves user list (Michelle), OPSWAT install confirmation. CIO declined still stands. See TODO § Vendor Access Isolation for the 2026-05-07 status update and the alignment email at `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`.
  - **NEW: Ansible topology decision (2026-05-07)** — no standalone Ansible server, no co-located Ansible VM. Ansible + ansible-core (latest) installed on all Proxmox dev nodes; playbooks run from the nodes themselves. Removes one VM from the planned topology and closes the msb-pmc01-04 Ansible-capacity TBD from 2026-05-06. Scope: Proxmox config + CephFS install/config — cluster-internal ops only. Currently `--check` mode; transition to live runs as testing matures with vendor engineer 1. v1.5 should reflect the topology change in any architecture-diagram references and remove standalone-Ansible-host language from earlier sections.
  - **CORRECTION: Nginx scope reopened (2026-05-07)** — earlier "no HA → no Nginx" reasoning (captured in v1.3 P1.4 removal and propagated through v1.4) was wrong. **Nginx installation** on the remote Airflow host stays in scope. **Server activation / configuration is TBD by Ksolves** — which functional roles get turned on (reverse proxy for YARN UI and other web UIs / endpoints, TLS termination, SSO front-door (Okta), URL rewriting, IP allowlisting, access logging) is the vendor's call. Single YARN RM confirmed (no HA), but stable-endpoint-for-HA is only one of Nginx's potential roles. v1.5 must restore Nginx **install** as a P1 task on the remote Airflow host, capture activation as TBD-Ksolves, and correct the v1.3/v1.4 closure language.
  - **NEW task — Snowflake Load Completion Confirmation Mechanism** (queued above).
  - **NEW task — Centralized Audit Logging + Retention Policy (HIPAA-driven)** (queued above; placement TBD between main CP and `CP_HIPAA_Compliance_v1.0.md`).
  - **MTU resolution note** — fqdn networking team resolved the 1400 / 9000 MTU mismatch on 2026-05-06; close out as completed if it was implicitly carried in any v1.4 task.
  - **Cascade RAM 384 → 320 GB** through the calculator math reference and phase1 model deliverable (HTML files: `dev_cluster_math_reference.html`, `dev_cluster_phase1_model.html` ×2 for phase1 + phase2 deliverables, `dev_calculator_guide.html`). Downstream values need recomputation (337 GB hard ceiling → 273 GB).
  - **Add NUMA pinning + AQE toggles** to `cluster_sizing_tool.html` (queued from 2026-05-05 Batch 3 deferral).
  - **Cross-references to refresh** to v1.5 across the project: phase1 README, phase1 ksolves April 24 status review, phase1 vendor questions, CP_Okta_v1.1, MSB-PMC01_airflow_host_briefing_v1.1, SOW_timeline_status, calculators (cluster_sizing_tool, dev_cluster_math_reference, dev-cluster-storage-reference, phase1+phase2 dev_cluster_phase1_model HTML).
  - **Companion files to bump** if their internal cross-refs touch v1.4: `MSB-PMC01_airflow_host_briefing_v1.1.md` may need v1.2 if VDI-security or production-questionnaire context lands; `CP_Okta_v1.1.md` may need v1.2 if AD DC enumeration changes the egress story.
  - **Changelog file** — write `Phases_Critical_Path_Development_v1.4_changelog.md` capturing v1.4 → v1.5 deltas; commit alongside the version-bumped artifact.
  - **PDF regeneration** for the bumped CP markdown.
- [ ] [Phase1] **CP v1.5: New task — Snowflake Load Completion Confirmation Mechanism** — owner: **Development team (fqdn)** + Murali / Rama. The current pipeline has no mechanism to confirm Snowflake `COPY INTO` completion and trigger downstream actions (CSV cleanup, archive move, "Operational Gate" step in the dev data-flow diagram). Proposed solution from the email: audit/checkpoint table in Snowflake or a logging mechanism that the Airflow DAG polls. Source: vendor lead (Ksolves), email forwarded 2026-05-06; corroborated by the "Operational Gate Process → Move CSV files off → Designated Storage Node (Archive)" step (#10) in `phases/phase2/development/reference_images/dev_data_flow_diagram_2026-05-06.png`.
- [ ] [Phase1] **CP v1.5: New task — Centralized Audit Logging + Retention Policy (HIPAA-driven)** — owner: **Development team (fqdn)** + fqdn Cyber/Security. HIPAA § 164.316(b)(2) requires audit logs retained ≥ 6 years; WORM-protected audit bucket recommended. No SIEM currently scoped. This may live in `CP_HIPAA_Compliance_v1.0.md` (HIPAA-driven) rather than the main CP — placement TBD when v1.5 is cut. Source: vendor lead (Ksolves), questionnaire Q1–Q3, email forwarded 2026-05-06.

**Follow-ups from this email (not action items, just tracked):**

- [ ] [correspondence] **Reconcile table count: 814 (Apr 27–May 01 Ksolves status) vs. 800 (vendor `csv_file_sizes.xlsx`, 2026-05-04)** — the 814 figure dates to Ksolves' Apr 27–May 01 weekly status report; the 800 figure is the vendor's actual measurement on 2026-05-04 and is the authoritative number. The 14-table delta is likely placeholder / mapping noise. Confirm with Rama on next CSV inventory delivery. Source: same email, 2026-05-06.
- [ ] [security] **Redact AD-group screenshot before tracking** — `phases/phase2/development/Incoming/eedfd24e-3c00-4d15-a7aa-19bfb61b1d70.png` shows `the corporate AD domain` in seven AD group strings and "an admin user" in the title bar. Useful as a corroboration of the AD group taxonomy that `CP_Okta_v1.1.md` § O0.3 will consume. Redact (blur or replace) FQDN + name, then move to `phases/phase2/development/reference_images/` with name `ad_group_membership_admin_user_example_2026-05-06.png`.
- [x] [correspondence] **NUC-failure refinement of BLOCKER.1** — Ksolves' email clarifies that the BLOCKER.1 vendor-Windows-host hardware prerequisite is specifically NUCs failing in their data center; Ksolves is debugging. The user has shifted to hosting Webex from his office host until they resolve hardware. Refine BLOCKER.1 wording in CP v1.5 to capture the specific cause (NUC reliability) and the interim host arrangement.

### Vendor Access Isolation — Phase 1B VDI Security Gate (NEW 2026-05-06)

CIO declined to authorize Phase 1B VDI access on the proposed terms in a 2026-05-06 meeting. Phase 1B is now gated on a vendor-isolation design that constrains the vendor's network exposure to a documented IP allowlist + host-level Linux firewalls. Phase 1A (Webex screen sharing) continues as the interim. **See `security/Notes/vendor-access-isolation-plan_2026-05-06.md` for the full meeting capture, CIO position, vendor lead Cyber's mitigation brainstorm, ruled-out approaches, and open architecture questions.**

**Allowed-surface constraints (CIO directive 2026-05-06; list expected to grow):**
- Spark Proxmox cluster (msb-pmc03) — all 3 hosts
- VMs created on msb-pmc03
- Bastion VM on `msb-pmc01-04` (vendor's only msb-pmc01 surface)
- VLANs 37 (mgmt), 38 (cluster), 39 (CephFS) on msb-pmc03
- AD domain controllers — all of them (Okta SSO is AD-tied; cannot subset)

**Status (2026-05-06 update):** the meeting was a brainstorm — no path is yet committed. Rohn + Sean Klette are the active planners; Paul Barber + CIO are later reviewers. NUC issue **resolved** 2026-05-06 — Phase 1A Webex screen-sharing is active and vendor work is progressing during the design phase. OS context: Proxmox hosts are Debian; all VMs are RHEL 9.4.

**Status update (2026-05-07):** Ksolves Horizon pool stood up by Jason — built and reachable via UAG; `ks_test` AD group attached for fqdn-side validation before any vendor accounts come in. Austin set firewall-style policies on the pool: pool can reach **DNS, AD, UAG, and Connection Servers** (assumed); everything else blocked until further notice. **CIO declined still stands** — this completes one CIO sub-task (pool stand-up + initial allow/block posture, pending validation), with all other vendor-isolation requirements still open. Rohn drafted alignment email to Sean + Austin on 2026-05-07 (`correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`); awaiting their sync output to fold into CP v1.5.

**Status update (2026-05-08):** Austin replied to the alignment email (`correspondence/Document/email_austin_response_horizon_pool_2026-05-08.md`). Two of three confirmation questions answered: **CS's = Horizon Connection Servers** (confirmed); **policy enforcement layer = network firewall** (confirmed; not NSX micro-seg, not host-level). **New fact:** the Horizon pool uses the firewall as its default gateway → all egress flows through one chokepoint at Austin's firewall. Implication: when Snowflake/Azure egress allowlist mechanics land (Rohn's open sub-task), the deployment surface is this single firewall — Austin adds the rules, no per-VM/per-route configuration needed.

**Status update (2026-05-08, later):** **Sean replied to the alignment email** (`correspondence/Document/email_sean_response_horizon_pool_2026-05-08.md`): "This does not change the cluster side and related VM isolation as planned." **All three confirmation questions now answered.** Layering hypothesis **confirmed by both parties**: Austin's pool-level (egress) and Sean's cluster-side (ingress + VM isolation) controls operate orthogonally — pool-level decisions don't reduce or expand cluster-side scope. The "Sean + Austin sync on pool ↔ cluster-side layering" sub-task is **closed 2026-05-08**. Sean's cluster-side design (the actual proposal — VLAN approach or alternative; resolution of the `10.1.37.0/24` cluster-overlap) remains the next major BLOCKER.4 sub-task. Mirrored in `Phases_Critical_Path_Development_v1.5.md` § BLOCKER.4 + `security/Notes/vendor-access-isolation-plan_2026-05-06.md`.

**Status update (2026-05-08, EOD send batch):** All five 2026-05-08 vendor letters / emails sent to Ksolves:
- `correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md` — Phase 2 closure verification (3 questions: scope, HIPAA-under-Phase-2 framing, LUKS software on already-hardware-encrypted drives). Awaiting vendor response.
- `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md` — § 8.3 ownership verification (custom javax servlet filter for Spark Web UI / History Server ACL — fqdn-side or Ksolves-delivered?). Flagged HIGH PRIORITY. Awaiting vendor response.
- `correspondence/Document/nvme_luks_already_encrypted_followup_to_ksolves_2026-05-08.md` — written follow-up to the verbal already-given on NVMe scratch-drive LUKS posture. Don't-reformat instruction. Awaiting vendor confirmation.
- `correspondence/Document/proxmox_audit_findings_cover_email_to_ksolves_2026-05-08.md` — cover email for the audit findings; 7-row verification-items table; references both attachments.
- `correspondence/Document/proxmox_audit_findings_to_ksolves_2026-05-08.md` — audit detail HTML attachment (rendered to `proxmox_audit_findings_to_ksolves_2026-05-08.html`). 14 sections; § 13 verification items; § 14 audit-run methodology.
- Plus reference attachment: sanitized raw bash output (auth keys redacted) — `proxmox_audit_raw_output_2026-05-08.txt`.

Each letter's source MD has Status updated to "Sent 2026-05-08 — awaiting vendor response". `ready_for_delivery/` folder emptied (audit trail preserved in git history at commits `d0acfde` / `5143e60` / `f380845` / `a01074c`). `html_review/` folder also emptied (gitignored; rebuildable from sources via pandoc).

**Status update (2026-05-08, EOD review punch-list landed):** Major Phase 2 closures via the 2026-05-08 user review of the html_review folder. **Closed via 5/8 email exchange:** pool validation testing (Sean + Rohn), confirm consistent IP blocks for vendor-created VMs. **New non-blocking item captured:** msb-pmc04 third-cluster idea — under consideration to add to the Spark cluster infrastructure, removing msb-pmc01 from the security equation. Material implications: orchestration / Airflow / monitoring services migrate from msb-pmc01-04 to msb-pmc04; Bastion VM also migrates; `10.1.37.0/24` cluster-overlap simplifies; vendor allowlist scope shrinks. Captured in CP v1.5 § BLOCKER.4 + `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Status (2026-05-08 — msb-pmc04) + `MSB-PMC01_airflow_host_briefing_v1.2.md`. **Structural splits:** P0.1 → P0.1a (closed) + P0.1b (open); BLOCKER.3 → 3a (vendor-claimed-closed pending fqdn verification) + 3b (open). **Cross-doc follow-ups:** CP_Okta v1.1 has new note flagging follow-up with Paul Barber; Production CP v0.1 v1.5-sync section expanded with new info from review doc.

- [x] [calculators] [security] **Self-contain native HTMLs — remove Google Fonts dep** — **closed 2026-05-08** via path (a). Stripped Google Fonts `<link>` references (preconnect tags + stylesheet link) from 11 native HTML files using `tmp/strip_google_fonts.py` — 27 `<link>` tags removed in total. Fonts fall back to the listed system fonts (Cascadia Code, Fira Mono, Consolas, system-ui, etc.). All 11 files now zero external resource references. Files modified: `calculators/Document/{cluster_sizing_tool,dev_cluster_math_reference,dev_calculator_guide,dev_slider_guide,dev-cluster-storage-reference,development_spark_calculator,production_spark_calculator,prod_calculator_guide,spark_flows,spark_glossary}.html` (10 git-tracked) + `security/Document/compliance_frameworks_reference.html` (1 on-site only, not git-tracked). Per project rules, styling-only changes don't require Revisions section updates.

**Active design lead under exploration (Sean Klette, 2026-05-06):** make msb-pmc03 the **sole tenant** of VLANs 37 / 38 / 39, and add a new **VLAN 10** providing controlled public ingress/egress (Proxmox WebUI + SSH + VM access). If this lands, intra-cluster traffic is permitted by VLAN membership rather than per-IP allowlist, and VLAN 10 becomes the single chokepoint for the ~30–35 IP allowlist. Substantially simpler than per-host firewalls. Open items in the security note.

**New action items (open):**

_Owned by Sean Klette (Network):_
- [ ] [Phase1] [security] **Develop the VLAN-isolation proposal** — confirm tenancy on VLANs 37/38/39 exclusive to msb-pmc03; design VLAN 10 for ingress/egress; document routing topology enforcing "only path out is via VLAN 10". See `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § "Sean's VLAN Isolation Approach".
- [x] [Phase1] [security] **Sync with Austin on Horizon pool ↔ cluster-side design layering** — **closed 2026-05-08**: Sean replied "This does not change the cluster side and related VM isolation as planned." (`correspondence/Document/email_sean_response_horizon_pool_2026-05-08.md`). Layering confirmed orthogonal: Austin's pool-level (egress, enforced at the network firewall = pool's default gateway, single chokepoint) and Sean's cluster-side (ingress + VM isolation, designed independently) operate as separate layers. Austin's reply 2026-05-08 (`correspondence/Document/email_austin_response_horizon_pool_2026-05-08.md`); Sean's reply 2026-05-08. All three confirmation questions from the 2026-05-07 alignment email answered.
- [ ] [Phase1] [security] **Confirm consistent IP blocks for vendor-created VMs** — would let the allowlist use a CIDR rather than enumerated per-VM IPs. Carries either way the design lands. **Substantial progress 2026-05-06 (DNS-confirmed):** all 7 Proxmox hosts now mapped (msb-pmc03 at 10.1.37.31–33, msb-pmc01 at 10.1.37.48–51); 5 Spark VMs at 10.1.37.10–14. **Both clusters share `10.1.37.0/24`** — resolves the VLAN-scoping question in favor of "global VLAN namespace" reading. The 3 VMs on msb-pmc01-04 (Bastion, Airflow, GPL) and the 2 vendor Horizon VDI IPs remain TBD. Major implication for Sean's VLAN-isolation approach: msb-pmc03 cannot be the "sole tenant" of 37/38/39 without renumbering one cluster — see `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Sean's VLAN Isolation Approach addendum for the four design paths.

_Owned by Rohn (fqdn):_
- [x] [Phase1] [security] **Draft vendor-isolation email to Ksolves** — Murali reviews + forwards. Don't commit to a date until the design is sized. **— Drafted 2026-05-06; promoted to `correspondence/Document/vendor_email_horizon_vdi_security_revision_2026-05-06.md`; sent to Ksolves 2026-05-07.**
- [x] [Phase1] [security] **Draft alignment email to Sean + Austin on Horizon pool stand-up** — frames our current interpretation of Jason's + Austin's 2026-05-07 updates, asks three confirmation questions (CS's = Connection Servers? policy enforcement layer? interaction with Sean's cluster-side design?), and lists open CIO-directive sub-tasks. **— Drafted 2026-05-07; promoted to `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`; sent by Rohn 2026-05-07.**
- [ ] [Phase1] [security] **Pool validation testing** — Sean + Rohn validate the Ksolves Horizon pool via the `ks_test` AD group: confirm session brokers correctly through UAG → Connection Servers, AD authentication works, intended destinations reachable, blocked destinations actually blocked. Output feeds the next vendor-isolation milestone. Predates any Ksolves user provisioning.
- [ ] [Phase1] [security] **Investigate nftables-based outbound filtering** as fallback / defense-in-depth — Proxmox layer (Debian, `nftables`) + VM layer (RHEL 9.4, `firewalld`). Confirm rule structure, package-manager update handling, blocked-outbound logging.
- [ ] [Phase1] [security] **Investigate constrained vendor sudo** — verify `nft` / `iptables` / `ufw` / `firewall-cmd` can be carved out of vendor sudo without breaking install workflow (sudoers `Cmnd_Alias`, AppArmor on Debian, SELinux on RHEL).
- [x] [Phase1] [security] **Enumerate AD domain controllers in scope** — pull from fqdn AD inventory. Needed regardless of design. **— Closed 2026-05-06: 7 DCs across 4 sites (Windsor ×2, Garfield ×1, South ×2, MSB RW + RO). See `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § AD domain controllers. Open follow-up: confirm with fqdn AD admins whether vendor traffic should be DC-pool-wide or steered to specific DCs (e.g., MSB-RO for query, MSB-RW for writeback).**
- [ ] [Phase1] [security] **Decide cloud egress allowlist mechanics** — Snowflake/Azure Blob endpoint IPs rotate. FQDN-based (DNS trust at firewall) vs published CSP IP ranges (periodic refresh) vs egress proxy.
- [x] [Phase1] [security] **Request Ksolves install OPSWAT security client on all vendor devices** — vendor-side device-posture attestation (patch status, password protection, screen-saver requirements, no screen-capture / keylogger software). Doesn't grant fqdn control of vendor devices; provides assurances of secure state. Item #6 from Harper's 2026-05-06 meeting summary. Owner: Rohn (vendor coordination). **— Closed 2026-05-07: requested.**
- [ ] [Phase1] [security] **Validate remote-domain credentials against required dev servers** — confirm that `remote.corp.<fqdn>` test-account logins work on the dev cluster RHEL servers Ksolves will console into. Item #7 from Harper's summary. Owner: Rohn / team.
- [ ] [Phase1] [security] **Evaluate feasibility / legal implications of fqdn performing portions of the installation** — alternative path if VDI design doesn't land in time. Contract requires Ksolves to certify the build; if fqdn does the work, certification path needs review. Item #10 from Harper's summary. Owner: Rohn / leadership.
- [ ] [Phase1] [security] **Provide Ksolves an updated estimate for when secure access will be available** — once Sean's design is sized + Cyber review timeline is clearer. Item #12 from Harper's summary. Owner: Rohn. Tracks alongside the email draft (now sent / awaiting Murali review).
- [ ] [correspondence] **Review DNS & Firewall questions response from Ksolves** — vendor engineer 1 to share the question sheet with vendor answers via Google Drive on 2026-05-07; walkthrough scheduled for next session. Source: 2026-05-07 daily stand-up; see `correspondence/Notes/ksolves_meeting_notes_2026-05-07.md`. Closes part of the existing "Awaiting Ksolves reply on network, firewall, and DNS access matrix" item under Waiting for Vendor Reply.
- [ ] [correspondence] **Reconcile production questionnaire response paths** — `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` was drafted as Rohn's solo pass; per 2026-05-07 stand-up, Rama's team is leading the formal response (filled out + internal second-opinion review + then to Ksolves). Sync with Rama before promoting / sending the Ready_For_Review draft. Owner: Rohn.

_Owned by reviewers (not yet ready):_
- [ ] [Phase1] [security] **Cyber review of final design** — Paul Barber. Once Rohn + Sean have a candidate.
- [ ] [Phase1] [security] **CIO risk-acceptance sign-off** — Rob Ball. Once Cyber endorses.
- [ ] [Phase1] [security] **Phase 1B exit-condition decision** — when does the design come off / what does the cluster's network posture revert to. Owner: Rohn + Paul Barber.

**Critical-path implication:** This adds gates to Phase 1B, parallel to BLOCKER.1's vendor-Windows-host issue (now resolved on the NUC side). Capture in CP v1.5 alongside the other queued additions. All of {BLOCKER.1, pool validation testing, vendor-isolation firewall design, Cyber endorsement, CIO sign-off, Ksolves user list, OPSWAT install confirmation} must close before VDI access goes live.

### RHEL ISO Provisioning (CLOSED 2026-04-30)

- [x] [Phase1] [correspondence] Confirm RHEL version: 9.4 (current assumption) vs. 9.7 (pending Ksolves Spark compatibility research) **— resolved 2026-04-30: proceeding with RHEL 9.4 (vendor-requested); 9.7 ISO held on disk for future evaluation but not blocking**
  - Decision: RHEL 9.4 committed for all Phase 1 VM provisioning
  - 9.7 compatibility research with Ksolves is no longer on the critical path
  - See: phases/phase1/development/vendor_comms/phase1_vendor_questions.txt § RHEL Version Decision

- [x] [Phase1] [remote_services] Provision RHEL ISO to Proxmox local storage (user action) **— closed 2026-04-30: ISOs placed on all three dev-cluster nodes via local Directory storage at `/rpool/data/templates/iso/`; decoupled from P0.0 dependency**
  - Resolution path: User added `/rpool/data` as Datacenter → Storage → Directory entry with ISO content type enabled; Proxmox auto-created `templates/iso/` subdirectory; ISOs moved there and visible in Create-VM wizard on all three nodes
  - Versions placed: RHEL 9.4 (committed) + RHEL 9.7 (held)
  - Original blocker (waiting for P0.0 / Ceph HEALTH_OK before placing ISOs) was bypassed by using node-local ZFS storage instead of Ceph-backed shared storage
  - See: phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md § BLOCKER.2 (CLOSED)

### P0 — Critical Path (This Week)

- [x] [Phase1] [correspondence] **Gather CSV file information for Ksolves storage/shuffle verification** — **Closed 2026-05-05**: vendor delivered the analysis themselves in `Ksolves_Spark_YARN_Config_v1.0.pdf` (2026-05-04), based on `csv_file_sizes.xlsx`. Numbers: 800 tables / 359 with data / 12,214 files / 1.52 TB compressed / 2 multi-file tables (5,800 files each) / top 12 tables = 79.29% of volume.

- [x] [Phase1] [correspondence] Confirm cloud staging target — Azure Blob or AWS S3 — for Snowflake COPY INTO path. **Closed 2026-05-05: Azure Blob confirmed**. Pipeline: `Airflow DAG → spark-submit per table → Ceph → Parquet → Snowflake COPY INTO from Azure` (per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1).
- [ ] [Phase1] [correspondence] Confirm RHEL 9.4 subscriptions active on all Worker VMs and YARN RM VM
- [ ] [Phase1] [remote_services] Install Hadoop 3.4.1 separately on all Worker VMs and configure HADOOP_HOME — **Owner: Vendor (Ksolves)**. Note for vendor: Spark 3.5.x ships with Hadoop 3.3.x; install must set `HADOOP_HOME` → 3.4.1 + `spark.yarn.populateHadoopClasspath = true` per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 3.4 deployment note.
- [ ] [Phase1] [calculators] Run first 5 production jobs and measure actual shuffle amplification factor (update phases/phase1/development/deliverables/dev_cluster_phase1_model.html default once measured)

- [x] [Phase1] [remote_services] **Determine max concurrent Airflow task slots** — **Closed 2026-05-05: 1 concurrent job** (3-node cluster final). Vendor recommended +1 node for 2-concurrent operation but user decided 3 nodes only (budget). Per `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.2: "The cluster supports 1 concurrent Spark job with the current 3-node configuration." Airflow host sizing at P1.0 (6c / 24 GB / 500 GB SSD) remains valid for single-job orchestration.

### P1 — Phase 1 Support & Validation

- [x] [Phase1] [correspondence] Evaluate Phase 1 node addition timeline — 40-job SLA fails without a 4th node. **Closed 2026-05-05: NOT adding a 4th node (budget constraint)**. Vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.3 confirms 3-node operation is feasible-but-zero-buffer at the 4-hour SLA. Mitigations: schedule top 12 largest tables first (79.29% of volume); add Airflow size-check gate to skip the 184 placeholder tables.
- [ ] [Phase1] [remote_services] Validate WAN egress throughput (1 Gbps ≈ 125 MB/s) is sufficient for Parquet → cloud staging transfer
- [ ] [Phase1] [remote_services] Monitor Ceph OSD memory under peak ingest — increase osd_memory_target if latency spikes
- [ ] [Phase1] [remote_services] Deploy Spark History Server on Node02 (1 vCPU / 4 GB VM — confirmed in Phase 1 report)
- [x] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover. **Closed 2026-05-05**: scope dropped — single YARN RM final (no HA → no ZooKeeper). See Vendor Configuration Baseline above + v1.3 P1.3 removal.
- [x] [Phase1] [remote_services] Deploy YARN ResourceManager HA: active VM on Node01, standby VM on Node03. **Closed 2026-05-05**: scope dropped — single YARN RM final (3-node decision; no 4th node available for HA pair). See Vendor Configuration Baseline above.
- [ ] [Phase1] [remote_services] **Install Nginx on remote Airflow host.** **REOPENED 2026-05-07** — user confirmed Nginx **installation** stays in scope. **Server activation / configuration is TBD by Ksolves** (which functional roles get turned on — e.g., reverse proxy for YARN UI and other web UIs / endpoints, TLS termination, SSO front-door, URL rewriting, IP allowlisting, access logging). Single YARN RM on cluster confirmed (no HA → not the driver for stable endpoint), but the earlier "no HA → no Nginx needed" reasoning was wrong: stable-endpoint-for-HA is only one of Nginx's potential roles. Original 2026-05-05 closure reverted. _Original closure note (now superseded): "scope dropped — no HA → no need for stable endpoint. See Vendor Configuration Baseline above + v1.3 P1.4 removal."_
- [ ] [Phase1] [remote_services] Deploy Ansible control node on remote Airflow host

---

## Waiting for Vendor Reply

- [x] [Phase1] RHEL version compatibility: Is Apache Spark 3.5.3 compatible with RHEL 9.7? (Ksolves researching) **— no longer blocking as of 2026-04-30; user committed to RHEL 9.4 for Phase 1**
  - Decision: Proceeding with RHEL 9.4 (vendor-requested, confirmed compatible)
  - 9.7 ISO is on disk at `/rpool/data/templates/iso/` for future use if Ksolves' compatibility research lands favorably
  - Vendor reply still welcome but does not gate any Phase 1 work
  - See: phases/phase1/development/vendor_comms/phase1_vendor_questions.txt § RHEL Version Decision

- [ ] [correspondence] [remote_services] [security] Awaiting Ksolves reply on network, firewall, and DNS access matrix for msb-pmc01 / msb-pmc02 / msb-pmc03 — vendor assumptions and scope (combined ACL matrix: network/firewall + switch VLAN + RGW S3 IAM; dev/prod isolation; Azure egress) — see correspondence/Document/Ksolves Network Firewall DNS Query.md
  - Sent: 2026-04-30
  - Held for separate follow-up after this reply: ExaBGP compatibility — does Ksolves' Spark/RGW client config support a single VIP with ExaBGP failover, or does it hardcode per-node RGW addresses?

- [x] [Phase1] [correspondence] Revisit YARN HA / ZooKeeper / Nginx decision with Ksolves. **Closed 2026-05-05** (PARTIAL — see correction below): vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 4 implicitly confirms single-RM posture (no HA settings in `yarn-site.xml`). Single YARN RM VM is final. The 3-node decision (no 4th node) further validates: there is no 4th node available for active/standby pair anyway. **CORRECTION 2026-05-07:** ZooKeeper scope drop stands (no HA → no leader-election ensemble). **Nginx scope drop was wrong** — Nginx **installation** stays in scope; **server activation / configuration is TBD by Ksolves**. See reopened Nginx entries in P1 + Pending Tasks above.

- [ ] [Phase1] [security] **Awaiting Ksolves user list for VDI account provisioning** — vendor to deliver list of individual users who need accounts in the `remote.corp.<fqdn>` subdomain. Required regardless of design (host firewall vs Sean's VLAN approach). Item #8 from Harper's 2026-05-06 meeting summary. Owner: Ksolves.

- [ ] [Phase1] [security] **Awaiting Ksolves confirmation: OPSWAT security client installed on all vendor devices** — fqdn requested install 2026-05-07; vendor to confirm install completion across all devices that will participate in Phase 1B VDI access. Required for the device-posture attestation chain (patch status, password protection, no screen-capture / keylogger software). Owner: Ksolves.

---

## Open Questions

- [ ] [remote_services] "Monitoring Apache" — Airflow dashboards, Spark dashboards, or both? Scopes Grafana build-out
- [x] [remote_services] Second Proxmox host specs (vCPU, RAM, storage) — sets VM allocation ceiling **— Closed 2026-05-06: MSB-PMC01 specs captured in `phases/phase2/development/Document/MSB-PMC01_cluster_host_inventory.md` and Airflow target node detailed in `MSB-PMC01_airflow_host_briefing_v1.1.md`**
- [ ] [remote_services] Ingest batch window timing — validates job concurrency assumptions
- [ ] [remote_services] Is exaBGP floating S3 IP routable from bastion host's network segment?
- [x] [remote_services] Existing Grafana instance scope — what does it currently monitor? **— Closed 2026-05-06**
- [ ] [remote_services] Prometheus — new instance or already running on monitoring cluster?
- [x] [remote_services] YARN executor VM count per node — refines Prometheus series count and Promtail agent deployment **— Closed 2026-05-06: superseded by final architecture (1 YARN ResourceManager VM + 3 Worker VMs running NodeManager + Spark executors as processes; no separate executor VMs). Prometheus series count scopes to the 4 VMs.**
- [ ] [remote_services] Loki disk allocation on the new Grafana/Prometheus/Loki VM (`msb-pmc01-04`) — size for cluster log sources (Promtail agents on bastion + 3-node Spark cluster + monitoring VMs). Reworded 2026-05-06: Loki will be a fresh deploy on the new VM, not an existing instance to expand.

---

## Pending Tasks

**Configuration & Hardware Updates:**
_(All configuration items completed - see Completed section)_

**Correspondence & Project Coordination:**
- [x] [correspondence] Work on Proxmox access method (screen sharing vs. direct) — **resolved 2026-04-29: Webex desktop sharing active for Phase 1A; VDI for Phase 1B**
- [ ] [correspondence] Phase 1B — VMware Horizon VDI provisioning for Ksolves (permanent replacement for Webex sharing; pending fqdn Cyber Security approval; non-blocking for Phase 1/2 work)
- [ ] [correspondence] Decide cluster outbound network path: **MPLS** (single Lumen MPLS cloud) vs. **DIA direct** (multiple Lumen DIA handoffs, paid redundancy) vs. **DIA + VPN** (VPN over DIA, traffic-engineered redundancy) — gates WAN egress throughput validation and cloud staging target choice; cluster confirmed sited at ALG Brooks with redundant ingress from Garfield + Windsor — see `phases/phase2/development/Document/ETL_outbound_map.pdf`
- [ ] [correspondence] Define required interconnections between remote Airflow server and Spark cluster — coordinate with Sean Klette **— In progress as of 2026-05-06 (network connections discussion underway)**
- [ ] [correspondence] Review updated resource calculation document from vendor lead (pending receipt)
- [x] [correspondence] Review and provide feedback on dev cluster resource calculations and mappings — see `calculators/Document/dev_cluster_math_reference.html` **— Closed 2026-05-06**
- [ ] [correspondence] Confirm directory structure for incoming and archived CSV files (date-based vs. flat)
- [ ] [correspondence] Identify where in the pipeline CSV compression occurs and update mapping logic — see `calculators/Document/etl-data-flow-diagram.html`
- [x] [correspondence] Resolve authentication approach (Keycloak vs. Okta) with Cyber/Security **— Closed 2026-05-06: Okta selected; see `phases/phase2/development/Document/CP_Okta_v1.1.md`**

**Remote Services Provisioning:**
- [ ] [remote_services] Provision bastion VM on `msb-pmc01-04` — **Owner: Vendor (Ksolves)**. Host placement confirmed 2026-05-06; co-locates with Airflow VM and the planned Grafana/Prometheus/Loki VM on the same Tier-A node.
- [ ] [remote_services] Provision Grafana + Prometheus VM on monitoring cluster
- [ ] [remote_services] **Spin up new Grafana / Prometheus / Loki VM on `msb-pmc01-04`** — added 2026-05-06. Replaces / supersedes the generic "monitoring cluster" entry above; `msb-pmc01-04` is the designated host (Tier-A node, co-locates with Airflow VM per `MSB-PMC01_airflow_host_briefing_v1.1.md` § 3 — capacity headroom available since Airflow uses 6c/24GB of host's 24c/130GB). Loki bundled into this same VM per decision 2026-05-06.
- [ ] [remote_services] Deploy Airflow (webserver, scheduler, PostgreSQL)
- [x] [Phase1] [remote_services] Deploy ZooKeeper ensemble for YARN RM automatic failover — **Closed 2026-05-05**: dropped (single YARN RM, no HA). Duplicate of P1 entry above; see Vendor Configuration Baseline.
- [ ] [Phase1] [remote_services] **Install Nginx on remote Airflow host** — **REOPENED 2026-05-07**: see P1 entry above. Install stays in scope; server activation / configuration TBD by Ksolves. Duplicate of P1 entry above.
- [x] [Phase1] [remote_services] Deploy Ansible control node — install playbooks, configure SSH key + Proxmox API token access (confirmed 2026-04-23). **Closed 2026-05-07: NO standalone Ansible server / no co-located VM.** Decision per Webex collab session with vendor engineer 1 (Ksolves): Ansible + ansible-core (latest versions) installed directly on **all Proxmox dev nodes**; playbooks run from the nodes themselves. Removes a planned VM from the topology and removes the msb-pmc01-04 capacity question for Ansible. **Scope caveat:** these playbooks cover Proxmox node configuration + CephFS install/config — cluster-internal ops only. Ansible orchestration of remote services beyond the cluster (e.g., Airflow VM on msb-pmc01-04) is not in scope of this decision and would require revisiting if needed.
- [ ] [Phase1] [remote_services] **Continue Ansible playbook testing with vendor engineer 1 (2026-05-08+)** — vendor engineer 1 unzipped his playbook hierarchy on Proxmox dev nodes 2026-05-07; testing has been `--check` (dry-run) only so far, no actual changes applied. Tomorrow continues `--check` verification with transition to live runs as confidence builds. Scope: Proxmox configuration + CephFS install/config. Owner: vendor engineer 1 (Ksolves) executes; Rohn observes/validates.
- [ ] [remote_services] Deploy Promtail agent on bastion VM
- [ ] [remote_services] Deploy Promtail agents on 3-node Spark cluster
- [ ] [remote_services] Deploy Promtail agents on any other source-side VMs that ship logs to Loki — clarified 2026-05-06: Promtail runs on **source-side VMs (Spark cluster, bastion, anywhere we want logs from)**, **NOT** on the new Grafana/Prometheus/Loki VM on `msb-pmc01-04` (that VM is the Loki destination, not a Promtail source).
- [ ] [remote_services] Configure Prometheus scrape targets (node_exporter, pve_exporter, ZFS, YARN JMX, Ceph, Airflow StatsD)
- [ ] [remote_services] Build Grafana dashboards for Proxmox nodes, YARN/Spark, Ceph, bastion services — **Owner: Vendor (Ksolves)** (assigned 2026-05-06)
- [ ] [remote_services] Verify network path: bastion → YARN RM port 8032
- [ ] [remote_services] Verify network path: bastion → Ceph RGW floating IP
- [ ] [remote_services] Verify network path: Promtail → Loki port 3100
- [x] [remote_services] Add CLAUDE.md entry for remote_services directory structure **— Closed 2026-05-06: already covered in CLAUDE.md (lines 12, 21–26 plus context-rule references)**

**Security & Compliance:**
- [x] [security] Review and promote security/Ready_For_Review/compliance_frameworks_reference.html → security/Document/ — **Closed 2026-05-07**: promoted with conventions retrofit (theme toggle + global expand/collapse controls + scoped sub-section controls + warm-amber light-mode palette + light-mode overrides for hardcoded `#fff`). Establishes HTML conventions baseline for security/Document/. Per project rule, file is on-site only (not git-tracked). See Revisions section in the file for the 2026-05-07 entry.
- [x] [security] Archive `security/Ready_For_Review/AD_identity_architecture_analysis.html` — **Closed 2026-05-07**: untracked file referencing Keycloak (ruled out — Okta selected per CP_Okta_v1.1.md). Moved to `security/Notes/archive/AD_identity_architecture_analysis_2026-04-21.html`. Establishes `security/Notes/archive/` as the archive subdirectory convention going forward.
- [ ] [calculators] **HTML conventions sweep — calculators/Document/ retrofit** — apply CLAUDE.md HTML Document Conventions (theme toggle + global expand/collapse + scoped sub-controls) to existing reference HTML in `calculators/Document/`. Convention enforcement is currently aspirational not enforced; survey 2026-05-07 found: `cluster_sizing_tool.html`, `dev_cluster_math_reference.html`, `dev_slider_guide.html`, `dev-cluster-storage-reference.html`, `etl-data-flow-diagram.html` need both; `dev_calculator_guide.html` and `development_spark_calculator.html` have theme toggle but lack global controls. Use `security/Document/compliance_frameworks_reference.html` as the reference implementation. (Defer behind v1.5 CP bump.)
- [ ] [security] Define document categories within authentication scope
- [ ] [security] Decide on-site revision control approach (deferred)

---

## Follow-Ups (from Ksolves msb-pmc03-01 baseline review, 2026-05-01)

- [ ] [Phase1] [security] **Follow-Up:** Verify the `fqdn-vendor-admins` PVE group ACL was actually downgraded along with the per-user ACLs. The vendor's command history shows the group was granted `Administrator` role at `/`, then `<vendor-user-a>@pam` was set to `PVEAuditor` and `<vendor-user-b>@pam` to `PVEUser` via direct user ACLs — but the group-level grant was not visibly revoked. Run `pveum acl list | grep -i fqdn-vendor-admins`; if the Administrator entry is still present, remove it (`pveum acl delete / --group fqdn-vendor-admins --role Administrator`).
  - Source: `phases/phase2/development/Incoming/ksolves_node1_commands.txt` (lines 196–308 group/role setup; lines 385–388 per-user downgrade)

- [ ] [Phase1] [remote_services] **Follow-Up (network team):** msb-pmc03-01 bond0 is degraded — `nic1` is DOWN with LACP `churned` state, no LACP partner. Bond is currently 25 Gbps not 50. User has noted this will be resolved when new cables are run. Schedule with the network team; re-verify with `cat /proc/net/bonding/bond0` once cabling is in place; confirm `-02` and `-03` are similarly cabled (their baseline runs are scheduled today and will reveal their state).
  - Source: `phases/phase2/development/Incoming/ksolves_session_capture.txt` (lines 84–92 ip link, 235–312 bond status)

- [ ] [Phase1] [calculators] **Follow-Up:** Confirm the underlying media class for the 7× 3.5 TiB data drives on each msb-pmc03 node. `nvme list` returned empty on `-01`, and the HPE Smart Array presents all data drives as `LOGICAL VOLUME` (single-disk RAID0 LVs — Smart Array does not support JBOD/passthrough, so individual LVs is the only path to meet the Proxmox JBOD requirement). The CLAUDE.md hardware reference states "7× 3.84 TB NVMe per node"; verify whether the underlying media is actually NVMe or SAS/SATA, and update CLAUDE.md plus `calculators/Document/dev-cluster-storage-reference.html` if the spec was wrong. Throughput math may need revising if SAS.
  - Source: `phases/phase2/development/Incoming/ksolves_session_capture.txt` (lines 16–58 lsblk + nvme list)

---

## Next Session

- [calculators] Review any pending calculator changes
- [remote_services] Resolve open questions (host specs, executor type, event log location) to finalize VM sizing; decide on Grafana dashboard scope
- [security] Promote compliance_frameworks_reference.html after review; define document categories for authentication scope — see `security/Ready_For_Review/compliance_frameworks_reference.html`
- [correspondence] Follow up on vendor replies and finalize configuration decisions

---

## Completed

- [x] [calculators] Review any calculator changes pending in Ready_For_Review/
- [x] [remote_services] Airflow executor type — CeleryExecutor confirmed (Ksolves directory walkthrough 2026-04-22)
- [x] [remote_services] Spark event log location — s3a://spark-history/ confirmed (Ksolves directory walkthrough 2026-04-22)
- [x] [correspondence] Update YARN Node Manager core allocation from 14 to 18 cores
- [x] [correspondence] Confirm 3-OSD storage allocation strategy (OSD utilization max 80%)
- [x] [correspondence] Revisit and confirm JBOD vs. RAID 5 for scratch drives decision
- [x] [correspondence] Confirm Spark version 3.5.3 in production calculator
- [x] [correspondence] Provide answers to Production Cluster Q&A questionnaire
- [x] [correspondence] Confirm JBOD + XFS as final disk strategy for dev
- [x] [calculators] Dev cluster: no hardware RAID — NVMe scratch drives run JBOD; only Proxmox OS SSDs use ZFS
- [x] [calculators] Dev cluster: scratch OSDs formatted with XFS
- [x] [calculators] Update all related HTML files to reflect JBOD/XFS storage decisions
