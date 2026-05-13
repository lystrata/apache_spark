# SOW Timeline vs. Actual Status

_As of 2026-05-13. Source: March 16, 2026 Ksolves SOW V1.0 § 5 Indicative Timelines (in `phases/development/phase2/Incoming/`)._

**Project start (per user):** 2026-04-14
**Total SOW duration:** 12 weeks → indicative completion 2026-07-06 (no Halt Period assumed)
**Elapsed:** ~4.3 weeks · entering Week 5 — **Phase 3 target start 2026-05-20** (joint agreement 2026-05-13; SOW indicative was 2026-05-12, slip of one week)

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
| **1. Discovery & Setup Planning** (1 wk) | 2026-04-14 → 2026-04-20 | **Completed 2026-04-24** (~4 days late, end of Week 2 instead of end of Week 1) | Ksolves Phase 1 Report (Apr 24); critical-path planning crystallised in `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.6.md` |
| **2. Proxmox & VM Creation** (3 wks) | 2026-04-21 → 2026-05-11 | **In window, ready to start.** BLOCKER.1 Phase 1A cleared 2026-04-29 (Ksolves on Webex); BLOCKER.2 (RHEL ISO) gated by P0.0 | dev: P0.0 Ceph bootstrap, P0.1 Worker VMs, P0.2 YARN RM VM. prod: equivalents pending — `Phases_Critical_Path_Production_v0.1.md` is a draft fork |
| **3. Dev Environment Implementation** (1 wk) | 2026-05-12 → 2026-05-18 | Future | dev: P0.5 Hadoop, P0.5a Spark, P1.0 Airflow host, P1.1 History Server, P1.2 YARN RM (single-instance per v1.1 vendor change), P1.5 Ansible, P1.8 sample jobs |
| **4. Production Environment Implementation** (2 wks) | 2026-05-19 → 2026-06-01 | Future | prod: full Phase 4 plus HIPAA controls (audit logging, RBAC, encryption in transit, KMS/Vault, network isolation, bastion, OS hardening) — not yet reflected in `Phases_Critical_Path_Production_v0.1.md` |
| **5. UAT** (4 wks) | 2026-06-02 → 2026-06-29 | Future | End-to-end validation against ~2 TB datasets per source; client sign-off; aligns with dev P1.8 sample-job battery |
| **6. Handoff & KT** (1 wk) | 2026-06-30 → 2026-07-06 | Future | Configuration docs, runbooks (incl. manual YARN RM recovery runbook from v1.1), KT sessions |

---

## Where We Stand (2026-05-08 EOD)

- Today is **mid Week 4** — the **last week of the SOW Phase 2 (Proxmox & VM Creation) window** (2026-04-21 → 2026-05-11). Phase 2 has made substantial progress today.
- Phase 1 (Discovery & Setup Planning) finished 2026-04-24, on plan.
- **🎉 Major progress 2026-05-08 — six closures:** BLOCKER.1 (Ksolves remote access — Phase 1A satisfies; Phase 1B tracked under B.4), P0.0 (Ceph cluster bootstrapped — MON, MGR, 9× OSD, RGW; HEALTH_OK), P0.1 (3× Worker VMs provisioned), P0.4 pre-req (RHEL 9.4 subs verified), P0.7 (MSB-PMC01 ↔ MSB-PMC03 network connectivity confirmed). BLOCKER.2 was already closed 2026-04-30. Phase 2A's foundational layer is essentially in.
- **BLOCKER.1 Phase 1A — ACTIVE 2026-05-06; BLOCKER.1 itself CLOSED 2026-05-08.** Ksolves vendor lead drives Proxmox provisioning via Webex screen share with fqdn oversight. The original Phase 1A re-opening (Linux/Windows Webex remote-control limitation, vendor Windows-host hardware prerequisite) was **resolved 2026-05-06** — user shifted to hosting Webex from the fqdn-office Windows host. Phase 1B permanent VDI replacement is tracked under BLOCKER.4.
- **NEW BLOCKER.4 (added 2026-05-06): Phase 1B vendor-access isolation gate.** A 2026-05-06 meeting with the CIO declined Phase 1B (Horizon VDI) on the originally-proposed terms. Phase 1B is now gated on a vendor-access isolation design + Cyber endorsement + CIO sign-off. Partial progress 2026-05-07 (Ksolves Horizon pool stood up by Jason; Austin set initial pool-egress firewall posture: DNS/AD/UAG/CS allowed, rest blocked). One BLOCKER.4 sub-task complete pending validation; remaining gates open. Captured in `Phases_Critical_Path_Development_v1.6.md` § BLOCKER.4 + `security/Notes/vendor-access-isolation-plan_2026-05-06.md`.
- **BLOCKER.3 (added 2026-05-05; split 2026-05-11; partially closed 2026-05-13): HIPAA compliance gate.** Vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` § 8 introduced HIPAA encryption + Web UI ACL scope. Forked into a sub-project: `CP_HIPAA_Compliance_v1.2.md`. **BLOCKER.3a (hardware) closed 2026-05-11**; **BLOCKER.3b (software/network) reassigned to Phase 3**. Production-side ePHI processing remains gated on the full posture.
- **3-node cluster finalized (2026-05-05).** Vendor recommended +1 node for 2-concurrent-job operation; user declined on budget. Mitigations (top-12 tables first; placeholder-table size-check gate) accepted.
- **MTU mismatch resolved 2026-05-06** — fqdn networking team aligned 1400/9000 MTU between MSB-PMC01 and MSB-PMC03; closes a P0.7 follow-up.
- **Ansible topology decision (2026-05-07)** — no separate Ansible VM. Ansible + ansible-core installed on all three Proxmox dev nodes; vendor playbook tree on-cluster; `--check`-mode testing in progress with vendor engineer 1.
- **Nginx scope correction (2026-05-07)** — restored as install-in-scope on the Airflow VM; activation TBD by Ksolves. Companion file `MSB-PMC01_airflow_host_briefing_v1.1` → `_v1.2` carries this.
- **Halt Period (SOW §7.2)** — not invoked. Phase 2 is progressing through Phase 1A; the long-pole gate is BLOCKER.4 (multi-week design + Cyber + CIO chain), but vendor work continues during the gate.
- **Vendor change pending:** the 2026-04-27 verbal reversal (single YARN RM, no ZooKeeper) is still not captured in a SOW V1.1. SOW V1.1 also needs to capture (a) the 3-node finalization, (b) HIPAA scope addition (BLOCKER.3 sub-project), (c) the rollover to vendor's `Ksolves_Spark_YARN_Config_v1.0.pdf` baseline, (d) Ansible topology change, (e) Nginx scope correction, (f) BLOCKER.4 Phase 1B isolation gate, (g) **javax servlet filter DROPPED from SOW 2026-05-13 — Web UI security via Kerberos + AD logins (Spark SPNEGO filter) instead**, (h) **Ansible-driven Spark install/configuration replacing the implicit manual posture** (Ksolves granted upfront prep time 2026-05-13 due to isolation constraints; Phase 3 target start 2026-05-20). Tracked under `TODO.md § Waiting for Vendor Reply`.

## Update (2026-05-13) — Phase 3 May-20 target; javax dropped; Kevin onboarded; Ansible-for-Spark-install scope

Joint fqdn–Ksolves meeting 2026-05-13 closed several Phase 2 items and locked in Phase 3 sequencing:

- **Phase 2 — Ksolves-side obligations COMPLETE 2026-05-13** (joint confirmation). fqdn-side Phase 2 closure pending: BLOCKER.4 (vendor-isolation framework v0.3); Phase 2 closing letter responses; cluster sign-over verification checklist.
- **Phase 3 — target start 2026-05-20** (joint agreement). One-week slip from SOW indicative (2026-05-12 → 2026-05-20). Week 2026-05-13 → 2026-05-19 allocated to: (a) Ksolves' upfront Ansible-script development for Spark install/config; (b) fqdn-side Phase 2 closure work (BLOCKER.4, sign-over checklist, closing-letter responses).
- **javax servlet filter — DROPPED from SOW** (joint agreement). Vendor doc § 8.3 custom `javax servlet filter` requirement removed with fqdn concurrence. Web UI security enforced via **Kerberos + AD logins** instead (Spark's built-in SPNEGO filter against the #H4 Kerberos realm; AD groups drive ACLs via `spark.admin.acls.groups`). Closes `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md` outcome. Detailed in `CP_HIPAA_Compliance_v1.2.md` §§ #H1 (closed) + #H1-rev (new) + #H4 (scope expanded).
- **Ansible-driven Spark install scope** — Spark installation/configuration originally scoped as manual Ksolves work in SOW V1.0; with isolation constraints (Phase 1B Horizon-pool gating, framework v0.3 design surface), Ksolves has been granted **additional up-front time to develop Ansible scripts** that automate the installs. Rationale: Ksolves uses the gap proactively rather than waiting passively for the isolation design to land before manual work can begin. Net schedule effect: Phase 3 start shifts to 2026-05-20 (one-week slip). Net scope effect: SOW V1.1 line item (h) replaces implicit-manual with explicit-Ansible posture.
- **Team expansion — Kevin onboarded (fqdn-side, 2026-05-13).** Linux/Ansible/Proxmox; 3rd infrastructure reviewer alongside Rohn. Operational impact: independent review point for Phase 3 Ansible playbook walk-throughs, Kerberos/AD design (#H4 + #H1-rev), HIPAA software/network compliance.

**SOW V1.1 letter still pending** — the joint agreement of 2026-05-13 confirms the scope adjustments but the formal SOW V1.1 written instrument has not been issued. Items (a)–(h) above are the canonical list to fold in when SOW V1.1 is drafted.

## Where We Stood (2026-04-29 — historical)

- Today is **early Week 3**. Per SOW we should be ~1/3 through **Phase 2 (Proxmox & VM Creation)** — Ceph bootstrap and VM provisioning underway.
- Phase 1 (Discovery & Setup Planning) finished 2026-04-24, ~4 days past the SOW Week-1 boundary — essentially on plan given the 1-week phase budget.
- BLOCKER.1 Phase 1A cleared 2026-04-29 — Ksolves now accessing the dev cluster via Webex desktop sharing. _(Note: Phase 1A subsequently re-opened 2026-04-30 due to Linux/Windows Webex remote-control limitation; resolved again 2026-05-06 — see "Where We Stand (2026-05-08)" above.)_
- Phase 2 still not started but the gate is open. Remaining Phase 2 budget: ~1.7 weeks (then through 2026-05-11). BLOCKER.2 (RHEL ISO) was gated by P0.0 Ceph OSD setup _(BLOCKER.2 subsequently closed 2026-04-30 via node-local Directory storage — see CP v1.5 § BLOCKER.2)._
- Halt Period (SOW §7.2) could still apply if BLOCKER.2 stalled Phase 2 substantively, but with remote access live the immediate trigger has been removed.
- Vendor change pending: the 2026-04-27 verbal reversal (single YARN RM, no ZooKeeper, no nginx) is not yet captured in a SOW V1.1. _(Note: Nginx scope subsequently corrected 2026-05-07 — install-yes / activation-TBD-by-Ksolves.)_

---

## Caveats

- "Indicative" per SOW: durations are estimates, not contractual SLAs.
- SOW § 2.2 (Out of Scope) excludes "user load or performance testing" — the dev critical path's P1.8 (5 sample jobs / shuffle amplification) likely needs a Change Order or separate SOW.
- The 12-week sequence assumes continuous work; observed pattern is sequential phase gating, so Phase 5–6 cannot start before Phase 4 completes.
- Calculations use a 7-day week (no working-day adjustment).
