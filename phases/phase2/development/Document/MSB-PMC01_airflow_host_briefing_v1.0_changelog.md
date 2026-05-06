# MSB-PMC01 Airflow Host Briefing — v1.0 → v1.1 Changelog

_Updated 2026-05-05 — Vendor configuration baseline rollover + open-items finalization_

The v1.1 bump aligns the briefing with two events that landed between 2026-04-29 (when v1.0 was published) and 2026-05-05:

1. The **Ksolves Spark/YARN Configuration document v1.0** (delivered 2026-05-04, `Ksolves_Spark_YARN_Config_v1.0.pdf`) — built from the actual DEV environment measurement (`csv_file_sizes.xlsx`: 800 tables, 359 with data, 12,214 files, ~1.52 TB compressed). It introduces concrete DAG-design expectations that the team provisioning the Airflow host should know about even though they are P2.2 inputs, not P1.0 sizing inputs.
2. The **3-node cluster decision** finalized 2026-05-05. Vendor's § 1.3 SLA Risk Summary recommended +1 node for 2-concurrent-job operation; fqdn declined on budget grounds; the cluster runs **1 concurrent Spark job** with mitigation via large-first table ordering and a placeholder size-check gate.

| Section | Change |
| ------- | ------ |
| Title block | `Version 1.0 · 2026-04-29` → `Version 1.1 · 2026-05-05`; Subject line expanded to mention DAG behavior expectations carried over from the vendor config baseline |
| § 1 Purpose | New "v1.1 update (2026-05-05)" paragraph at end summarizing the bump |
| § 4 Network Prerequisites (P0.7 Gate) | Cross-reference `Phases_Critical_Path_Development_v1.3.md` → `..._v1.4.md` |
| **§ 5.1 (NEW)** | New sub-section — `Airflow DAG Behavior Expectations`. Six expectations table covering: (1) large-first table ordering with top-12 = 79.29 % volume; (2) placeholder-table size-check gate skipping the 184 empty tables; (3) per-table `target_partitions = max(24, ceil(compressed_csv_mb / 50))` runtime parameter injection; (4) static `spark.sql.shuffle.partitions = 4096` fallback; (5) retry handling owned by Airflow, not Spark; (6) `max_active_runs=1` (or pool-of-1) to enforce the single-concurrent-Spark-job constraint |
| § 6 Open Items Affecting Final Sizing | Two of three items closed: max concurrent Spark jobs **= 1** (was open) and cloud staging target **= Azure Blob** (was leading candidate). Outbound network path (MPLS/DIA/DIA+VPN) remains open. Heading + leading paragraph reworded to frame the section as resolution log + remaining-open. |
| § 7 Source Data and References | Cross-reference `Phases_Critical_Path_Development_v1.3.md` → `..._v1.4.md`; new entries for `Ksolves_Spark_YARN_Config_v1.0.pdf` (with section pointers) and `CP_HIPAA_Compliance_v1.0.md` |
| Companion PDF | `MSB-PMC01_airflow_host_briefing_v1.0.pdf` → `_v1.1.pdf` (regenerated via pandoc + lualatex with TOC) |

**Cross-references bumped to v1.1:**
- `TODO.md` (the Vendor Configuration Baseline section's existing reference to this file is path-versioned)

**Cross-references _not_ bumped (deferred):** The Phases Critical Path v1.4 markdown does not currently link to this briefing by versioned filename, so no edit is required there. If a versioned link is added in a later edit, point it to `_v1.1.md`.

**Not changed:**
- `phases/phase2/development/Document/MSB-PMC01_airflow_host_briefing_v1.0.md` and `_v1.0.pdf` are removed in favor of the renamed v1.1 set (git history preserves the v1.0 state via the `git mv` rename detection).

**Promotion note:** v1.1 was created via `git mv` on both the `.md` and `.pdf`, then targeted edits to the markdown, then PDF regeneration. The git rename detection keeps blame contiguous across the version bump.
