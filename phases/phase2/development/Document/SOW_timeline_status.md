# SOW Timeline vs. Actual Status

_As of 2026-04-27. Source: March 16, 2026 Ksolves SOW V1.0 § 5 Indicative Timelines (in `phases/phase2/development/Incoming/`)._

**Project start (per user):** 2026-04-14
**Total SOW duration:** 12 weeks → indicative completion 2026-07-06 (no Halt Period assumed)
**Elapsed:** ~1.9 weeks · currently mid-Week 2

---

## Week Calendar (from 2026-04-14 start)

| Week | Dates | SOW Phase |
|---|---|---|
| 1 | 2026-04-14 → 2026-04-20 | Phase 1 — Discovery & Setup Planning |
| 2–4 | 2026-04-21 → 2026-05-11 | Phase 2 — Proxmox & VM Creation |
| 5 | 2026-05-12 → 2026-05-18 | Phase 3 — Dev Environment Implementation |
| 6–7 | 2026-05-19 → 2026-06-01 | Phase 4 — Production Environment Implementation |
| 8–11 | 2026-06-02 → 2026-06-29 | Phase 5 — UAT |
| 12 | 2026-06-30 → 2026-07-06 | Phase 6 — Handoff & KT |

---

## SOW Phase → Repo Critical Path Mapping

| SOW Phase | Indicative Window | Status | Repo Tasks |
|---|---|---|---|
| **1. Discovery & Setup Planning** (1 wk) | 2026-04-14 → 2026-04-20 | **Completed 2026-04-24** (~4 days late, end of Week 2 instead of end of Week 1) | Ksolves Phase 1 Report (Apr 24); critical-path planning crystallised in `phases/phase2/development/Ready_For_Review/Phases_Critical_Path_Development_v1.2.md` |
| **2. Proxmox & VM Creation** (3 wks) | 2026-04-21 → 2026-05-11 | **In window, not started.** BLOCKER.1 (Ksolves remote access) open; BLOCKER.2 (RHEL ISO) gated by P0.0 | dev: P0.0 Ceph bootstrap, P0.1 Worker VMs, P0.2 YARN RM VM. prod: equivalents pending — `Phases_Critical_Path_Production_v0.1.md` is a draft fork |
| **3. Dev Environment Implementation** (1 wk) | 2026-05-12 → 2026-05-18 | Future | dev: P0.5 Hadoop, P0.5a Spark, P1.0 Airflow host, P1.1 History Server, P1.2 YARN RM (single-instance per v1.1 vendor change), P1.5 Ansible, P1.8 sample jobs |
| **4. Production Environment Implementation** (2 wks) | 2026-05-19 → 2026-06-01 | Future | prod: full Phase 4 plus HIPAA controls (audit logging, RBAC, encryption in transit, KMS/Vault, network isolation, bastion, OS hardening) — not yet reflected in `Phases_Critical_Path_Production_v0.1.md` |
| **5. UAT** (4 wks) | 2026-06-02 → 2026-06-29 | Future | End-to-end validation against ~2 TB datasets per source; client sign-off; aligns with dev P1.8 sample-job battery |
| **6. Handoff & KT** (1 wk) | 2026-06-30 → 2026-07-06 | Future | Configuration docs, runbooks (incl. manual YARN RM recovery runbook from v1.1), KT sessions |

---

## Where We Stand (2026-04-27)

- Today is **mid-Week 2**. Per SOW we should be in early **Phase 2 (Proxmox & VM Creation)** — Phase 1 wrapped, Ceph bootstrap and VM provisioning underway.
- Phase 1 (Discovery & Setup Planning) **finished 2026-04-24, ~4 days past the SOW Week-1 boundary** — essentially on plan given the 1-week phase budget.
- Phase 2 has not yet started. We are **still inside its 3-week indicative window** (ends 2026-05-11), so work can begin without slippage if BLOCKER.1 closes promptly. Each week BLOCKER.1 stays open consumes ~1/3 of the Phase 2 budget.
- **Halt Period (SOW §7.2)** still applicable to BLOCKER.1 / RHEL ISO if the gate persists — the gated duration would excise from schedule, milestones, and SLA. Decision point if BLOCKER.1 is not closed by ~2026-05-04 (end of Week 3).
- **Vendor change pending:** the 2026-04-27 verbal reversal (single YARN RM, no ZooKeeper, no nginx) is not yet captured in a SOW V1.1 — the SOW Document History table is still blank past V1.0. Tracked under `TODO.md § Waiting for Vendor Reply`.

---

## Caveats

- "Indicative" per SOW: durations are estimates, not contractual SLAs.
- SOW § 2.2 (Out of Scope) excludes "user load or performance testing" — the dev critical path's P1.8 (5 sample jobs / shuffle amplification) likely needs a Change Order or separate SOW.
- The 12-week sequence assumes continuous work; observed pattern is sequential phase gating, so Phase 5–6 cannot start before Phase 4 completes.
- Calculations use a 7-day week (no working-day adjustment).
