# Phases Critical Path — Development Cluster — v1.3 → v1.4 Changelog

_Updated 2026-05-05 — Vendor configuration baseline incorporated + HIPAA forked to sub-project + 3-node decision finalized_

The v1.4 bump captures three substantive changes the project decided on 2026-05-05 in response to Ksolves' authoritative configuration document delivered 2026-05-04 (`phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf`):

1. **3-node cluster finalized.** Vendor's § 1.3 SLA Risk Summary recommended adding a 4th node to enable 2-concurrent-job operation. fqdn declined the +1 node on budget grounds; the 3-node cluster proceeds with 1 concurrent Spark job. Vendor's "feasible-but-zero-buffer" SLA analysis at 3 nodes is the accepted posture, with mitigations: schedule the 12 largest tables first (79.29 % of total volume) and add an Airflow size-check gate to skip the 184 placeholder tables.
2. **HIPAA scope forked into a separate critical-path sub-project.** Vendor's § 8 (HIPAA Compliance Architecture & Guidelines) introduces a substantial cross-team workstream — Kerberos / RPC encryption / SSE / a custom javax servlet filter for Web UI ACL. Tracking it in the main CP would obscure the cross-team coordination, so it lives at `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` with a BLOCKER pointing back to it.
3. **GZIP non-splittability mitigation** elevated to a P0 decision item. Vendor's § 2 identifies GZIP as the dominant technical constraint for the workload; the choice between pre-splitting upstream / changing codec to bzip2 / sending raw uncompressed CSV / post-read repartition is a Development-team decision that gates ETL job design.

| Section | Change |
| ------- | ------ |
| Title block | v1.3 → v1.4, dated 2026-05-05; Config Source line added pointing to `Ksolves_Spark_YARN_Config_v1.0.pdf`; Status line gains BLOCKER.3 + 3-node finalization note |
| Schedule & SOW Status | Expanded SOW V1.1 bullet to capture (a) 3-node finalization, (b) HIPAA sub-project addition, (c) rollover to vendor's config v1.0 baseline; new "3-node cluster decision (2026-05-05)" bullet explaining vendor's +1-node recommendation and fqdn's decline + mitigation strategies |
| BLOCKER.2 (CLOSED) | Downstream impact line updated to reference both BLOCKER.1 and the new BLOCKER.3 as remaining production gates |
| **BLOCKER.3 (NEW)** | New section after BLOCKER.2 — `HIPAA Compliance (Spark / YARN / Ceph encryption + Web UI ACL)`. Carries the gate; full detail in `CP_HIPAA_Compliance_v1.0.md`. Quick summary captures vendor-owned vs fqdn-owned items + already-done LUKS encryption. |
| P0.0a | Status icon `🔴 → ✅`; retitled with `— CLOSED 2026-05-05`; resolution notes that vendor delivered the analysis themselves in `Ksolves_Spark_YARN_Config_v1.0.pdf` § 1.1 (based on `csv_file_sizes.xlsx`); full numbers captured: 800 tables / 359 with data / 12,214 files / 1.52 TB compressed / 2 multi-file tables (5,800 files each) / top 12 = 79.29 % of volume |
| **P0.0b (NEW)** | New section — `GZIP Non-Splittability Mitigation Decision (Development-Team Owned)`. Owner: fqdn Development team. Sources vendor § 2; lists the 4 mitigation options + vendor's recommendation (pre-split upstream); references the repartition formula from § 7.2 as conditional fallback |
| P0.3 (Cloud staging target) | Status icon `🔴 → ✅`; retitled with `— CLOSED 2026-05-05: Azure Blob`; resolution captures the pipeline confirmed by vendor § 1.1 (Pipeline row); implementation impact noted (SAS / managed identity / network routing) |
| P0.5a | Added new "Vendor Configuration Note (added 2026-05-05)" bullet citing vendor § 3.4 deployment note about Hadoop 3.4.1 vs Spark 3.5.x bundled 3.3.x; Ksolves must set `HADOOP_HOME` → 3.4.1 + `spark.yarn.populateHadoopClasspath = true` |
| **P0.6 (NEW)** | New section after P0.5a — `Ceph RGW Server-Side Tuning (Vendor-Owned)`. Owner: Vendor (Ksolves). Sources vendor § 6.4. Vendor applies `rgw_thread_pool_size 512` + `rgw_max_concurrent_requests 1024` + RGW daemon restart. fqdn verifies post-install. Listed on the cluster sign-over verification checklist. |
| Footer | `_Location: …_v1.3.md_` → `_Location: …_v1.4.md_` |
| Tracker HTML (`phases_critical_path_development_tracker_v1.4.html`) | Filename version-tagged lockstep with source: `tracker_v1.3.html` → `tracker_v1.4.html`. Title bar + header version markers updated to "v1.4 · 2026-05-05". **Content additions (BLOCKER.3, P0.0a closure, P0.0b, P0.3 closure, P0.6) are not yet reflected in the tracker body** — see source markdown for full v1.4 content. Tracker content overhaul deferred to a follow-up commit. |
| New companion file | `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` (and `.pdf`) — sub-project critical path for the HIPAA encryption + Web UI ACL workstream. Promoted from `Ready_For_Review/` to `Document/` as part of this v1.4 bump. |

**Cross-references bumped to v1.4:** `TODO.md` (Vendor Configuration Baseline section + closures), `CLAUDE.md` (hardware reference RAM/node 384 → 320 GB).

**Cross-references _not_ bumped (deferred to a follow-up):** `phases/phase1/development/README.md`, `phases/phase1/development/Notes/ksolves-april24-status-review.md`, `phases/phase1/development/vendor_comms/phase1_vendor_questions.txt`, `phases/phase2/development/Document/CP_Okta_v1.0.md`, `phases/phase2/development/Document/MSB-PMC01_airflow_host_briefing_v1.0.md`, `phases/phase2/development/Document/SOW_timeline_status.md`, `calculators/Document/cluster_sizing_tool.html`, `calculators/Document/dev_cluster_math_reference.html`, `calculators/Document/dev-cluster-storage-reference.html`, `phases/phase{1,2}/development/deliverables/dev_cluster_phase1_model.html`. These will be updated in subsequent commits as needed.

**Not changed:**
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.3.md` (the now-archival v1.3) is left as-is — it accurately represents the state at the v1.3 promotion.
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.2.md` and `_v1.1_changelog.md`, `_v1.2_changelog.md` remain as historical records.
- `phases/phase2/development/Document/phases_critical_path_development_tracker_v1.3.html` left intact alongside the new v1.4 tracker (archival reference).

**Promotion note:** v1.4 was created as a copy of v1.3 + targeted edits, following the convention used at the v1.3 bump. The v1.3 set is preserved in `Document/` for archival reference.
