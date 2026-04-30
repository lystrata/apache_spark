# Phases Critical Path — Development Cluster — v1.2 → v1.3 Changelog

_Updated 2026-04-30 — Phase 1A re-opened due to vendor Webex Linux/Windows interop limitation_

The v1.2 promotion captured the state of the critical path through 2026-04-29 (Phase 1A previously thought cleared). On 2026-04-30, testing confirmed the Webex Linux desktop client cannot remote-control a Windows Webex share (or vice-versa). Because Ksolves is a Linux shop and fqdn shares from a Windows host, this re-opens BLOCKER.1: Ksolves must provision a Windows host on their side to drive Phase 1A remote-control sessions.

| Section | Change |
| ------- | ------ |
| Title block | v1.2 → v1.3, dated 2026-04-30 |
| Status line | Added "(re-opened 2026-04-30 — see Phase 1A hardware prerequisite)" qualifier on BLOCKER.1 status |
| BLOCKER.1 status field | `OPEN` → `OPEN — re-opened 2026-04-30 due to newly identified Phase 1A hardware prerequisite` |
| BLOCKER.1 Phase 1A timeline | `Ready immediately; no infrastructure dependencies` → `Pending Ksolves Windows host provisioning (see hardware prerequisite below)` |
| BLOCKER.1 Phase 1A | Added 🪟 **Hardware Prerequisite** callout explaining Webex Linux/Windows remote-control limitation and vendor obligation to provision a Windows host |
| BLOCKER.1 actions | Added new **Vendor Actions Required (Hardware Prerequisite)** subsection with four sub-tasks |
| BLOCKER.1 user actions | Reframed Immediate user actions as "pending vendor hardware prerequisite" |
| BLOCKER.1 verification | Added two new Phase 1A verification rows for Windows host + remote-control test |
| BLOCKER.1 owner | Added Ksolves as owner for the hardware prerequisite |
| BLOCKER.1 effort | Added vendor Windows-host provisioning as a new effort line; reworded Phase 1A as "post-vendor-prereq" |
| Footer | `_Prepared for Review: Ready_For_Review/Phases_Critical_Path_Development_v1.2.md_` → updated to v1.3; updated date and reason line |
| Manual TOC | Removed `## Table of Contents` block from the markdown body. PDF clickable TOC is preserved via pandoc auto-generation; markdown viewers (Obsidian, GitHub) lose the in-doc TOC but rely on heading-pane navigation instead |
| Phase 1A / 1B | Promoted from bold paragraph labels to proper `####` headings: `#### Phase 1A — Interim: Shared Webex Desktop with fqdn Team Oversight` and `#### Phase 1B — Permanent: VMware Horizon Desktop Access`. New explicit anchor IDs `blocker1-phase-1a-interim-webex` and `blocker1-phase-1b-permanent-horizon` added for cross-referencing |
| Access Strategy wrapper | Removed `#### Access Strategy (Phased)` h4 heading — now redundant since Phase 1A and Phase 1B are themselves h4 headings. Replaced with a single intro sentence |
| PDF generation | Pandoc command updated to `--toc --toc-depth=4` so the auto-TOC reaches BLOCKER.x, Phase 1A/1B, P0.x, P1.x, P2.x — matching the depth of the removed manual TOC |
| BLOCKER.2 | **CLOSED 2026-04-30** — User decoupled RHEL ISO placement from the original P0.0 (Ceph HEALTH_OK) dependency by placing ISOs on node-local ZFS storage. Workflow: registered `/rpool/data` as Proxmox Datacenter Directory storage with ISO content type enabled (Proxmox auto-created `templates/iso/`), moved ISOs into that path, replicated across all three dev-cluster nodes. Both **RHEL 9.4 (committed)** and **RHEL 9.7 (held)** placed. Status icon changed `🔒 → ✅`; section retitled with `— CLOSED 2026-04-30`; full resolution detail captured inline. |
| RHEL version decision | RHEL 9.4 committed for Phase 1 (vendor-requested). User will not block on Ksolves' Spark 3.5.3 / RHEL 9.7 compatibility research; the 9.7 ISO is held on disk for possible future migration. P0.4 references and downstream tasks already assumed 9.4 — no changes needed there. |
| P0.0 priority line | `gates BLOCKER.2 and all P0.1+ items` → `gates RGW-dependent tasks (P1.1, P2.3) and Spark scratch allocation` (since BLOCKER.2 is decoupled) |
| P0.0 user-sign-off line | Removed `before proceeding to BLOCKER.2 (RHEL ISO placement)` clause — replaced with `before proceeding to downstream tasks that depend on RGW` |
| P0.0 Critical Note | Removed `BLOCKER.2 (RHEL ISO upload)` from the must-precede list; added a closing sentence noting BLOCKER.2 closed via node-local Directory storage |
| P0.2 status | `PENDING REMOTE ACCESS, BLOCKER.2 (RHEL ISO)` → `PENDING REMOTE ACCESS (BLOCKER.1) — RHEL ISO already in place per BLOCKER.2 closure` |
| Critical Path Sequence | BLOCKER.2 line moved up and marked `[x]`; P0.1–P0.5 line updated to note RHEL ISO already in place |
| Interactive HTML tracker | Updated to mirror v1.3 content (BLOCKER.1 reopening + Hardware Prerequisite callout + Vendor Actions block + new Phase 1A verification rows; BLOCKER.2 closure with full Resolution block; P0.0 / P0.2 / Phase 2 overview / Critical Path Sequence cleanup). **Filename version-tagged** lockstep with source: `phases_critical_path_development_tracker.html` → `phases_critical_path_development_tracker_v1.3.html` |

**Cross-references bumped to v1.3:** `TODO.md`, `CLAUDE.md`, `phases/phase1/development/README.md`, `phases/phase1/development/Notes/ksolves-april24-status-review.md`, `phases/phase1/development/vendor_comms/phase1_vendor_questions.txt`, `phases/phase2/development/Ready_For_Review/CP_Okta_v1.0.md`, `phases/phase2/development/Ready_For_Review/MSB-PMC01_airflow_host_briefing_v1.0.md`, `phases/phase2/development/Document/phases_critical_path_development_tracker_v1.3.html`, `phases/phase2/development/Document/SOW_timeline_status.md`.

**Not changed:**
- `phases/phase2/production/Ready_For_Review/Phases_Critical_Path_Production_v0.1.md` retains its `_Forked from Phases_Critical_Path_Development_v1.2.md_` reference (historical fork lineage; production scope to be revised separately when production work begins). Production-side BLOCKER.1 will be inherently satisfied by then since Ksolves' Windows host will already be in place from dev.
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.2.md` (the now-promoted v1.2) is left as-is — it accurately represents the state at promotion.
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.1_changelog.md` (the prior v1.0 → v1.1 changelog) remains as a separate historical record.

**Promotion note:** v1.2 was promoted from `Ready_For_Review/` to `Document/` on 2026-04-30 as part of the v1.3 bump, capturing the pre-reopening state for archival reference.
