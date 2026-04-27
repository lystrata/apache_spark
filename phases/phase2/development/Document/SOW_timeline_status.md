# SOW Timeline vs. Actual Status

_As of 2026-04-27. Source: March 16, 2026 Ksolves SOW V1.0 § 5 Indicative Timelines (in `phases/phase2/development/Incoming/`)._

**Project start (per user):** 2026-03-13
**Total SOW duration:** 12 weeks → indicative completion 2026-06-04 (no Halt Period assumed)
**Elapsed:** ~6.4 weeks · currently mid-Week 7

---

## Week Calendar (from 2026-03-13 start)

| Week | Dates | SOW Phase |
|---|---|---|
| 1 | 2026-03-13 → 2026-03-19 | Phase 1 — Discovery & Setup Planning |
| 2–4 | 2026-03-20 → 2026-04-09 | Phase 2 — Proxmox & VM Creation |
| 5 | 2026-04-10 → 2026-04-16 | Phase 3 — Dev Environment Implementation |
| 6–7 | 2026-04-17 → 2026-04-30 | Phase 4 — Production Environment Implementation |
| 8–11 | 2026-05-01 → 2026-05-28 | Phase 5 — UAT |
| 12 | 2026-05-29 → 2026-06-04 | Phase 6 — Handoff & KT |

---

## SOW Phase → Repo Critical Path Mapping

| SOW Phase | Indicative Window | Status | Repo Tasks |
|---|---|---|---|
| **1. Discovery & Setup Planning** (1 wk) | 2026-03-13 → 2026-03-19 | **Completed 2026-04-24** (~5 wks late) | Ksolves Phase 1 Report (Apr 24); critical-path planning crystallised in `phases/phase2/development/Ready_For_Review/Phases_Critical_Path_Development_v1.1.md` |
| **2. Proxmox & VM Creation** (3 wks) | 2026-03-20 → 2026-04-09 | **Not started.** BLOCKER.1 (Ksolves remote access) open; BLOCKER.2 (RHEL ISO) gated by P0.0 | dev: P0.0 Ceph bootstrap, P0.1 Worker VMs, P0.2 YARN RM VM. prod: equivalents pending — `Phases_Critical_Path_Production_v0.1.md` is a draft fork |
| **3. Dev Environment Implementation** (1 wk) | 2026-04-10 → 2026-04-16 | Not started | dev: P0.5 Hadoop, P0.5a Spark, P1.0 Airflow host, P1.1 History Server, P1.2 YARN RM (single-instance per v1.1 vendor change), P1.5 Ansible, P1.8 sample jobs |
| **4. Production Environment Implementation** (2 wks) | 2026-04-17 → 2026-04-30 | Not started | prod: full Phase 4 plus HIPAA controls (audit logging, RBAC, encryption in transit, KMS/Vault, network isolation, bastion, OS hardening) — not yet reflected in `Phases_Critical_Path_Production_v0.1.md` |
| **5. UAT** (4 wks) | 2026-05-01 → 2026-05-28 | Future | End-to-end validation against ~2 TB datasets per source; client sign-off; aligns with dev P1.8 sample-job battery |
| **6. Handoff & KT** (1 wk) | 2026-05-29 → 2026-06-04 | Future | Configuration docs, runbooks (incl. manual YARN RM recovery runbook from v1.1), KT sessions |

---

## Where We Stand (2026-04-27)

- Today is **mid-Week 7**. Per SOW we should be wrapping **Phase 4 (Production Implementation)** and about to enter Phase 5 (UAT).
- In reality, we are at the **start of SOW Phase 2 (Proxmox & VM Creation)** — three full SOW phases behind. Phase 1 alone consumed roughly **6 weeks vs. the 1 week budgeted** (5-week overrun).
- Net slippage at this point: **~5–6 weeks behind** the SOW indicative timeline, with Phases 2–6 entirely untouched.
- **Halt Period (SOW §7.2)** plausibly covers the BLOCKER.1 / RHEL ISO gate (client-side hardware/access readiness). If formally invoked, the gated duration is excluded from the schedule, milestones, and SLA. Whether to invoke is a contracting decision — see Project Change Control (SOW §9.2).
- **Vendor change pending:** the 2026-04-27 verbal reversal (single YARN RM, no ZooKeeper, no nginx) is not yet captured in a SOW V1.1 — the SOW Document History table is still blank past V1.0. Tracked under `TODO.md § Waiting for Vendor Reply`.

---

## Caveats

- "Indicative" per SOW: durations are estimates, not contractual SLAs.
- SOW § 2.2 (Out of Scope) excludes "user load or performance testing" — the dev critical path's P1.8 (5 sample jobs / shuffle amplification) likely needs a Change Order or separate SOW.
- The 12-week sequence assumes continuous work; observed pattern is sequential phase gating, so Phase 5–6 cannot start before Phase 4 completes.
- Calculations use a 7-day week (no working-day adjustment).
