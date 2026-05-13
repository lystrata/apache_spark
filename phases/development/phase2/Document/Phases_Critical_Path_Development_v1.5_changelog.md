# Changelog — Phases_Critical_Path_Development v1.5 → v1.6

_Captures the deltas from v1.5 (2026-05-07 / in-place 2026-05-11) to v1.6 (cut 2026-05-13)._

## Trigger

Joint fqdn–Ksolves meeting on **2026-05-13** landed five substantive items that collectively warrant a MINOR bump per project versioning policy:

1. Phase 2 — Ksolves-side obligations COMPLETE (joint confirmation).
2. **javax servlet filter DROPPED from SOW** (joint agreement with fqdn concurrence); Web UI security to be enforced via Kerberos + AD logins instead.
3. Team expansion — Kevin onboarded (fqdn-side; Linux/Ansible/Proxmox).
4. Phase 3 target start **2026-05-20** (one-week slip from SOW indicative).
5. Ansible-driven Spark install/configuration scope — Ksolves granted upfront prep time due to vendor-access isolation constraints.

## Header changes

- `_Version_` bumped 1.5 → 1.6
- `_Last updated_` bumped 2026-05-11 → 2026-05-13
- Status line rewritten: removed v1.5 long-form "in progress" enumeration; added "Phase 2 — Ksolves-side obligations COMPLETE as of 2026-05-13" + Phase 3 May-20 target + javax-drop one-liner + Kevin onboarding note.

## Body changes

- **§ PHASE 2 — IMPLEMENTATION** banner — title reframed from "IN PROGRESS — gated by BLOCKER.4; BLOCKER.3a closed 2026-05-11, BLOCKER.3b reassigned to Phase 3" to "Ksolves-side COMPLETE 2026-05-13; fqdn-side closure pending BLOCKER.4 + Phase 2 closing letter".
- **§ PHASE 2 → Update (2026-05-13)** — new sub-section covering all five items in detail. Cross-doc impact list points at `CP_HIPAA_Compliance_v1.2.md`, `SOW_timeline_status.md`, `TODO.md`, `security/Notes/vendor-access-isolation-plan_2026-05-06.md`.
- **§ Schedule & SOW Status — SOW V1.1 pending bullet** — expanded from items (a)–(f) to (a)–(h); added (g) javax filter dropped + (h) Ansible-driven Spark install/config replacing implicit manual posture.
- **§ BLOCKER.3 — Phase 3 scope (now in sub-project)** — "custom javax servlet filter" replaced by "Kerberos + AD logins (Spark SPNEGO filter)".
- **§ Final BLOCKER.3 dependency note** — javax filter line rewritten: "Web UI ACL via Kerberos + AD logins (replaces dropped javax servlet filter per 2026-05-13 SOW change)".
- **§ Reference Documents** — Visual Tracker reference bumped v1.5.html → v1.6.html; HIPAA sub-project ref bumped v1.1.md → v1.2.md.
- **Trailing footer** — `_Updated:` bumped 2026-05-07 → 2026-05-13 with v1.6 delta summary; `_Location:` bumped to v1.6.md; `v1.5 RAM cascade` note reworded to "v1.5/v1.6 RAM cascade".

## Companion files updated lockstep with v1.6 cut

- `phases_critical_path_development_tracker_v1.5.html` → `_v1.6.html` (rename + title + Source ref + Version line + Export markdown label + new v1.6 update banner card; internal `CP_HIPAA_Compliance` ref bumped v1.1 → v1.2)
- `Phases_Critical_Path_Development_v1.5.pdf` → `_v1.6.pdf` (regen)
- `CP_HIPAA_Compliance_v1.1.md` → `_v1.2.md` (rename + content):
  - Header `_Version 1.1_` → `_Version 1.2_`; `_Status_` line updated to flag #H1 DROPPED + #H1-rev added.
  - New `v1.2 Update (2026-05-13)` banner block at top describing the javax → Kerberos+AD pivot, mapping § 8.3 framing, and listing impact across #H1 / #H1-rev / #H2 / #H4.
  - **§ #H1** — status changed to **CLOSED 2026-05-13 (DROPPED FROM SOW)**; rationale captured; original fqdn actions struck through with "no longer required — for record" framing; reference notes superseded for fqdn implementation.
  - **§ #H1-rev (NEW)** — Kerberos + AD logins on Spark Web UI / History Server via Spark's bundled Hadoop SPNEGO filter; depends on #H4; AD-group-driven ACLs via `spark.admin.acls.groups` / `spark.modify.acls.groups`; configuration-only (no fqdn Java code).
  - **§ #H2** — status changed to **RESOLVED 2026-05-13 (Kerberos + AD)**; decision rationale documented; note about Airflow/SHS-Okta divergence captured.
  - **§ #H4** — title amended to "SCOPE EXPANDED 2026-05-13"; Web UI HTTP service principals (`HTTP/<host>@<REALM>`) added to fqdn actions; coordination with Michelle (AD groups) added.
- `CP_HIPAA_Compliance_v1.1.pdf` → `_v1.2.pdf` (regen)

## Cross-reference cascade

Active-doc cross-refs bumped from v1.5 → v1.6 and HIPAA v1.1 → v1.2 in:

- `phases/development/phase2/Document/MSB-PMC01_airflow_host_briefing_v1.3.md`
- `phases/development/phase2/Document/CP_Okta_v1.1.md` (header line annotated "cross-refs bumped on 2026-05-13; no Okta scope change")
- `phases/development/phase2/Document/SOW_timeline_status.md` (plus new 2026-05-13 update section; SOW V1.1 list expanded)
- `phases/development/phase1/Notes/ksolves-april24-status-review.md`
- `phases/development/phase1/README.md`
- `phases/development/phase1/vendor_comms/phase1_vendor_questions.txt`
- `phases/production/phase2/Document/Phases_Critical_Path_Production_v0.1.md` (CP + HIPAA + tracker refs)
- `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md`
- `TODO.md` (new 2026-05-13 status section + last-updated bump; historical status-update sections retain their point-in-time v1.5/v1.1 refs intentionally)

**Intentionally NOT bumped** (point-in-time historical artifacts):

- `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md`
- `correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md`
- `correspondence/Document/email_sean_response_horizon_pool_2026-05-08.md`
- `correspondence/Document/email_austin_response_horizon_pool_2026-05-08.md`
- `correspondence/Document/nvme_luks_already_encrypted_followup_to_ksolves_2026-05-08.md`
- `correspondence/Ready_For_Review/weekly_status_2026-05-11.md` (Monday-status moment)
- `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.4_changelog.md` (historical changelog about the v1.4→v1.5 cut)

## Memory updates

- New: `~/.claude/projects/-Users-rohn-Serve/memory/project_team_kevin.md` — Kevin role + skills + Phase 3 review duty.
- Index: `MEMORY.md` index gained the corresponding pointer line.

## Files NOT changed

- `CLAUDE.md` — no project conventions affected
- Calculator HTMLs — no calculator math change
- Production CP `_v0.1.md` other than cross-ref bumps — clean-slate scaffold framing already separates production timeline from dev; the 2026-05-13 dev event is referenced via the v1.6 main-CP path, not folded into the production scaffold
- Historical correspondence in `correspondence/Document/` — kept as point-in-time records
