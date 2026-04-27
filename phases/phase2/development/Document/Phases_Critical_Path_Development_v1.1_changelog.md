# Phases Critical Path — Development Cluster — v1.0 → v1.1 Changelog

_Vendor adjustments applied 2026-04-27_

The vendor confirmed three architectural simplifications for the development cluster: single YARN ResourceManager VM (no HA), no ZooKeeper, no nginx reverse proxy. All three reduce to a manual-recovery posture for YARN.

| Section | Change |
|---|---|
| Title block | v1.0 → v1.1, dated 2026-04-27 |
| Document Overview | Removed ZK-as-HA-prereq research note |
| TOC | Dropped P1.3 + P1.4; P1.2 renamed to "Single Instance, Manual Recovery" |
| P0.4 license check | `5 RHEL (3 Worker + 2 YARN RM)` → `4 RHEL (3 Worker + 1 YARN RM)` |
| P0.2 | Single VM (GKPR-YARN-RM-01), no standby; sign-off gate moved from P1.3 → P1.2 |
| P0.5 | `yarn-site.xml` note now references single RM, not "after HA deployment" |
| P0.5a | Prerequisite changed from P1.3 (ZK) → P1.2 (RM) |
| P1.0 | Dropped nginx-proxy bandwidth line |
| P1.1 | Removed Nginx mentions in priority/context/critical-note |
| P1.3 | **Removed entirely** (ZooKeeper) |
| P1.2 | Rewritten as single-instance with manual-recovery runbook |
| P1.4 | **Removed entirely** (Nginx) |
| P1.8 | Status, context, and infra-live checklist updated |
| Critical Path Sequence | P1.3 line removed; P1.2 reworded; P1.4 removed from "Ksolves provisions" line |
| Footnotes | ¹ (RM HA) removed as orphan; old ² (Spark on YARN) renumbered to ¹ |

**Cross-references bumped to v1.1:** `TODO.md`, `CLAUDE.md`, `phases/phase1/development/README.md`, `phases/phase1/development/Notes/ksolves-april24-status-review.md`, `phases/phase1/development/vendor_comms/phase1_vendor_questions.txt`, `phases/phase2/development/Ready_For_Review/CP_Okta_v1.0.md`, and the production doc's path references.

**Not changed:** `Phases_Critical_Path_Production_v0.1.md` still carries inherited HA/ZK/nginx content — production scope is revised separately.

**Source commit:** `11e9dda`
