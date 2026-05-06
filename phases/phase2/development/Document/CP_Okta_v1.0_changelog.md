# Critical Path — Okta + AD — v1.0 → v1.1 Changelog

_Updated 2026-05-05 — Cross-reference to HIPAA sub-project + main CP rolled v1.3 → v1.4_

The v1.1 bump aligns this document with two structural events on 2026-05-05:

1. The main critical path was bumped to **v1.4** (incorporating the vendor configuration baseline, GZIP P0, Hadoop classpath / Ceph RGW tuning vendor-owned tasks, HIPAA BLOCKER, and 3-node decision finalization). All references inside this document to `Phases_Critical_Path_Development_v1.3.md` were rolled to `..._v1.4.md`.
2. The HIPAA workstream was **forked into a separate sub-project** at `CP_HIPAA_Compliance_v1.0.md`. That sub-project owns inter-daemon Kerberos + RPC AES-GCM + SSL/TLS shuffle / IO encryption + Web UI ACL via custom javax servlet filter + SSE on Ceph buckets. Those items are **not** owned by this Okta document — Okta sits at the user-facing edge only — but they intersect at the Web UI ACL and SSH/ASA seams. The cross-reference in § Scope makes the boundary explicit so a reader of either document doesn't think the same work is being tracked twice.

| Section | Change |
| ------- | ------ |
| Title block | `Version 1.0 · 2026-04-26` → `Version 1.1 · 2026-05-05`. Companion line broadened: previously listed only `Phases_Critical_Path_Development_v1.3.md`; now lists `..._v1.4.md` and `CP_HIPAA_Compliance_v1.0.md`. |
| § Document Overview | Cross-reference `..._v1.3.md` → `..._v1.4.md` (×1) |
| § Methodology | Cross-reference `..._v1.3.md` → `..._v1.4.md` (×1, on the "matching the style of" line) |
| § Scope (Out of scope) | Existing line about Spark's native Kerberos/delegation-token machinery extended with a cross-reference paragraph: HIPAA-driven inter-daemon Kerberos / RPC encryption / SSL on shuffle / IO encryption / Web UI ACL / SSE on Ceph buckets is tracked in `CP_HIPAA_Compliance_v1.0.md`. Boundary stated: that sub-project owns on-cluster identity protocol; this document owns user-facing SSO. Intersection points (Web UI ACL, SSH/ASA) are called out in the relevant `O1.x` task. |
| § Scope (Snowflake bullet) | Cross-reference `..._v1.3.md` → `..._v1.4.md` |
| § Cross-References to Phase 1 TODO | All three `..._v1.3.md` references rolled to `..._v1.4.md` (`The following items in...`, `Update group/role mapping matrix in...`, `Update Bibliography in...`). The semantic content of these items is unchanged; only the target document version moved. |
| § Reference Documents | Existing `Phases_Critical_Path_Development_v1.3.md` line rolled to `..._v1.4.md`. Two new entries added: `CP_HIPAA_Compliance_v1.0.md` (companion sub-project, with one-line scope-boundary description) and `Ksolves_Spark_YARN_Config_v1.0.pdf` (vendor configuration baseline; § 8 is the upstream source for the HIPAA workstream). |
| Companion PDF | `CP_Okta_v1.0.pdf` → `_v1.1.pdf` (regenerated via pandoc + lualatex with TOC) |

**Cross-references not bumped (deferred):**
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.4.md` — the main CP currently does not reference `CP_Okta_v1.0.md` by versioned filename, so no edit was required. If a versioned link is added in a later edit, point it to `_v1.1.md`.
- `phases_critical_path_development_tracker_v1.4.html` — same as above.
- `TODO.md` — the master TODO references Okta tasks by `O0.x`/`O1.x` IDs rather than by file path, so no file-path edit needed.

**Not changed:**
- The substantive content of the document (auth surface inventory, architecture decisions AD-1 through AD-4, every `O0.x`/`O1.x`/`O2.x` task body, Group/Role Mapping Matrix, Network Egress Requirements, Open Questions for fqdn Cyber Security, Assumptions & Dependencies, all Footnotes 1–10, full Bibliography) is **unchanged**. v1.1 is purely a cross-reference rollover plus a HIPAA sub-project boundary statement.

**Promotion note:** v1.1 was created via `git mv` on both the `.md` and `.pdf`, then targeted edits to the markdown, then PDF regeneration via pandoc. Git rename detection keeps blame contiguous across the version bump.
