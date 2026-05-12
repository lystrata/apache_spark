# Phases Critical Path — Development Cluster — v1.4 → v1.5 Changelog

_Updated 2026-05-07 — Phase 1A activation, vendor-isolation gate, Horizon pool, Ansible topology, Nginx correction, two new tasks, RAM cascade, calculator toggles_

The v1.5 bump consolidates events from 2026-05-06 / 2026-05-07 plus catches up the tracker HTML on content already landed in the v1.4 markdown but deferred from the v1.3→v1.4 tracker cycle. Five intersecting workstreams produced the bump:

1. **Vendor-access posture** — A 2026-05-06 meeting with the CIO declined Phase 1B (Horizon VDI) on the originally-proposed terms. A new BLOCKER.4 captures the vendor-access isolation design + Cyber endorsement + CIO sign-off requirement. Ksolves' Horizon pool was stood up 2026-05-07 and pool-egress firewall policies set, completing one BLOCKER.4 sub-task pending validation. NUC hardware prerequisite for Phase 1A resolved 2026-05-06; Phase 1A activated.
2. **Ansible topology change (2026-05-07)** — Ansible no longer co-located on the Airflow VM (or a separate VM). Ansible + ansible-core installed directly on Proxmox dev nodes; vendor playbook tree on-cluster; `--check`-mode testing in progress. Removes a planned VM from the topology.
3. **Nginx scope correction (2026-05-07)** — Earlier "no HA → no Nginx" reasoning (used in the v1.3 P1.4 removal, propagated through v1.4) was wrong. Nginx **install** is restored as a P1 task on the Airflow VM; **activation TBD by Ksolves** (candidate roles enumerated).
4. **Two new tasks (2026-05-07)** — P2.8 Snowflake Load Completion Confirmation Mechanism (fqdn Dev team owned; design pending); P2.9 Centralized Audit Logging + Retention Policy (HIPAA-driven, 6-year floor; placement may shift to HIPAA sub-project).
5. **Calculator + reference cascades** — RAM 384 GB → 320 GB across the math reference, both phase1+phase2 deliverable models, and the calculator guide (dev cluster has 10 × 32 GB DIMMs, not 12). NUMA-pinning toggle and AQE/skew-join/shuffle-partitions toggles landed in `cluster_sizing_tool.html` (deferred from the v1.3→v1.4 cycle).

## Section-by-section changes

| Section | Change |
| ------- | ------ |
| Title block | v1.4 → v1.5, dated 2026-05-07; status line gains BLOCKER.4 (NEW 2026-05-06), explicit Phase 1A active note, Horizon pool stood-up note |
| Schedule & SOW Status | New 2026-05-06/07 bullets: NUC resolved, CIO declined Phase 1B, Horizon pool stand-up, MTU mismatch resolved |
| BLOCKER.1 | Full rewrite — Phase 1A active 2026-05-06; Phase 1B gated by BLOCKER.4; pool stand-up captured; Action / Verification matrices restructured; cross-ref to BLOCKER.4 |
| **BLOCKER.4 (NEW)** | New section after BLOCKER.3 — Phase 1B vendor-access isolation gate. Allowed-surface constraints (CIO directive 2026-05-06); active design candidate (Sean Klette VLAN approach); 2026-05-07 progress (Horizon pool stand-up + initial firewall posture); full sub-task matrix (Network / fqdn / Vendor / Reviewers); verification gate. |
| P0.7 (Network) | MTU 1400/9000 mismatch resolved 2026-05-06 noted; Ansible cross-cluster scope removed (Ansible now on Proxmox dev nodes per P1.5) |
| P1.0 (Remote Airflow) | **Nginx install restored** as a P1 task; activation TBD-Ksolves; candidate role list (reverse proxy, TLS termination, SSO front-door, URL rewriting, IP allowlisting, access logging); Ansible-on-host language removed |
| **P1.5 (Ansible — REVISED)** | Full rewrite. No standalone or co-located Ansible VM. Ansible + ansible-core on all three Proxmox dev nodes; playbook hierarchy on-cluster; `--check`-mode testing in progress. Scope: Proxmox config + CephFS install/config — cluster-internal ops only. |
| **P2.8 (NEW)** | New task — Snowflake Load Completion Confirmation Mechanism. Owner: fqdn Dev team + Murali / Rama. Three proposed solutions (audit table / event-bridge / stored procedure); decision tracker. Closes the "Operational Gate" step in the dev data-flow diagram. |
| **P2.9 (NEW)** | New task — Centralized Audit Logging + Retention Policy (HIPAA-driven). 6-year retention floor per § 164.316(b)(2); WORM on the audit bucket; sources / transport / store / access controls / integrity. May co-locate with the Grafana/Prometheus/Loki VM. May move to HIPAA sub-project once that taxonomy stabilizes. |
| Critical Path Sequence | Updated to reflect BLOCKER.4 + BLOCKER.3, Phase 1A active, P0.7 MTU resolution, P1.0 Nginx, P1.5 topology change, P0.6 Ceph RGW tuning, P2.8/P2.9, BLOCKER.3+BLOCKER.4 closure as Phase 2 sign-off requirement |
| References list | Expanded — adds vendor configuration baseline, HIPAA sub-project, companion files (CP_Okta, MSB-PMC01_airflow_host_briefing v1.2), SOW timeline tracker, calculator HTMLs (sizing tool, math reference, storage reference), security source documents (on-site only), recent correspondence |
| Footer | `_v1.4.md_` → `_v1.5.md_`; updated note summarising the v1.5 deltas |

## Tracker HTML overhaul (`phases_critical_path_development_tracker_v1.5.html`)

The tracker carried a deferred-content banner from the v1.3→v1.4 cycle. v1.5 overhaul:

- Title bar / header version markers / export-link bumped to v1.5 / 2026-05-07; deferred-content banner removed.
- BLOCKER.1 fully rewritten (Phase 1A active, Phase 1B BLOCKER.4-gated, pool stand-up).
- **BLOCKER.3 (HIPAA)** card added (deferred from v1.4) — points to `CP_HIPAA_Compliance_v1.0.md` sub-project; carries the gate.
- **BLOCKER.4 (Vendor isolation)** card added (NEW 2026-05-06) — full sub-task matrix.
- **P0.0a** status flipped 🔴 → ✅ (vendor delivered analysis 2026-05-04 via `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1); findings + SLA implications captured.
- **P0.0b (GZIP)** card added (deferred from v1.4) — fqdn Dev decision; 4 mitigation options; vendor recommends pre-split upstream.
- **P0.3** status flipped 🔴 → ✅ (Azure Blob confirmed by vendor § 1.1).
- **P0.5a** vendor configuration note added (Hadoop 3.4.1 vs Spark's bundled 3.3.x).
- **P0.6 (Ceph RGW Tuning)** card added (deferred from v1.4) — vendor-owned; on cluster sign-over checklist.
- **P0.7** MTU resolution checkbox added; Ansible cross-cluster scope clarification.
- **P1.0** Nginx install action added; Ansible-on-host language removed; Nginx scope note.
- **P1.5** fully rewritten — Ansible installed on Proxmox dev nodes 2026-05-07; `--check`-mode testing.
- **P2.8 + P2.9** cards added (NEW 2026-05-07).
- Phase 2 status sub-line updated; Critical Path Sequence rewritten; Reference table expanded.

## Calculator cascades (RAM 384 GB → 320 GB)

Per `CLAUDE.md § Hardware Reference`, the dev cluster has 10 × 32 GB DIMMs (320 GB), not 12 × (384 GB). All four downstream files updated:

- `calculators/Document/dev_cluster_math_reference.html` — RAM Note callout, AVAIL_RAM row (337 GB → 273 GB), Tier 2 RAM-per-node slider table, Revisions section
- `phases/development/phase1/deliverables/dev_cluster_phase1_model.html` — hardware-spec table, solver grid, worker spec rows, `RAM_NODE` constant, physical-RAM warning threshold, Revisions section
- `phases/development/phase2/deliverables/dev_cluster_phase1_model.html` — identical to phase1 (cp; diff confirmed)
- `calculators/Document/dev_calculator_guide.html` — doc subtitle, Section A intro, slider description, Worker VM example, pre-scale walkthrough

## Cluster sizing tool toggles (deferred from v1.3→v1.4)

`calculators/Document/cluster_sizing_tool.html` — landed:

- **Section A — NUMA pinning** select (on/off; default on). Drives a smarter dual-socket warning that distinguishes pinning-on (info) from pinning-off (warning). New warning when VCPU/VM > 32 with pinning on.
- **Section C — AQE** select (on/off; default on); shuffle.partitions slider (default 4096 per vendor); skew-join select (default on). New advisories: AQE-off (warn), AQE-on with skew-off (info).

## Companion files bumped

- `MSB-PMC01_airflow_host_briefing_v1.1.md` → `_v1.2.md` — Nginx scope correction lands here. Header version + v1.2 update note describing Nginx as install-in-scope / activation-TBD-by-Ksolves; candidate role list; pairing with main CP § P1.0.

## Cross-references bumped to v1.5

- `TODO.md` (CP cross-ref + v1.5 OVERDUE bullet annotated)
- `phases/development/phase2/Document/CP_HIPAA_Compliance_v1.0.md` (4 v1.4 → v1.5)
- `phases/development/phase2/Document/CP_Okta_v1.1.md` (7 v1.4 → v1.5)
- `phases/development/phase2/Document/SOW_timeline_status.md` (v1.3 → v1.5)
- `phases/development/phase1/README.md` (v1.3 → v1.5)
- `phases/development/phase1/Notes/ksolves-april24-status-review.md` (v1.3 → v1.5)
- `phases/development/phase1/vendor_comms/phase1_vendor_questions.txt` (v1.3 → v1.5)
- `security/Notes/vendor-access-isolation-plan_2026-05-06.md` (v1.4 → v1.5; on-site only)

## Cross-references _not_ bumped (deferred / intentional)

- The four prior changelog files (`_v1.1_changelog.md`, `_v1.2_changelog.md`, `_v1.3_changelog.md`) remain as historical records.
- `Phases_Critical_Path_Development_v1.4.md` is replaced by `_v1.5.md` (git mv); v1.4 retained in git history.
- Production-side `Phases_Critical_Path_Production_v0.1.md` — unchanged; that fork has its own evolution.
- `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` — held in Ready_For_Review pending Rama-side coordination per the 2026-05-07 stand-up; not bumped.

## Not changed

- Prior versions (`_v1.4.md`, `_v1.3.md`, `_v1.2.md`, `_v1.1_changelog.md`, etc.) remain as historical records.
- `phases_critical_path_development_tracker_v1.4.html` left intact in git history; v1.5 is the working tracker.

## Promotion note

v1.5 was created as a `git mv` of v1.4 + targeted edits, following the convention used at the v1.3 → v1.4 bump. The v1.4 set is preserved in git history (final state at `dccfdfb`'s parent).

## Commits

- `dccfdfb` — Phase A: CP v1.5 markdown bump
- `d85d565` — Phase B: tracker HTML overhaul
- `21db11a` — Phase C: RAM 384 → 320 cascade
- `adb7ada` — Phase D: cluster_sizing_tool NUMA + AQE toggles
- `48e9b7f` — Phase E: cross-references + companion bumps (MSB-PMC01_airflow_host_briefing v1.1 → v1.2)
- _Phase F (this changelog + PDF regen) follows_
