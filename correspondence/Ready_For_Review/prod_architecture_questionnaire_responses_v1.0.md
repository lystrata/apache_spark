# Production Architecture Questionnaire — Responses (Draft)

_Version 1.0 · 2026-05-06_
_Source: vendor lead (Ksolves), 16-point production architecture questionnaire forwarded 2026-05-06_
_Status: **DRAFT for fqdn internal review** — many items require Cyber/Security and Networking input before reply_

---

## Document Overview

This document captures fqdn's draft responses to the 16-point production architecture questionnaire that Ksolves shared on 2026-05-06 as part of the dev → production transition planning. The questionnaire covers HIPAA-driven concerns Ksolves raised: SIEM / audit logging, secrets management, IAM/RBAC/PAM, network/perimeter, compliance/risk, and operational on-call/DR posture.

Where existing project decisions or documents already answer a question, the answer is given inline with citations. Where a question requires input from a fqdn stakeholder we don't yet have an answer from (Cyber/Security, Networking, Legal/Compliance), the response is marked **Needs internal confirmation** with the suggested owner.

The intent is for the user to walk through this document, edit the draft answers, and use the corrected version as the basis for the reply to Ksolves.

---

## Sources Already Available to Inform Responses

- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.4.md` — main critical path
- `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md` — HIPAA encryption + Web UI ACL sub-project (vendor-driven)
- `phases/phase2/development/Document/CP_Okta_v1.1.md` — user-facing SSO architecture
- `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` — vendor configuration baseline
- `security/Notes/okta-migration-plan.md` — earlier auth scaffolding
- `security/Notes/keycloak-implementation-plan.md` — superseded by Okta decision (kept for history)

---

## Section 1 — Audit Logging & SIEM

### Q1 — Existing centralized log management?

> HIPAA requires audit logs to be retained for a minimum of 6 years (§164.316(b)(2)). Do you have an existing centralised log management system — such as Splunk, ELK/OpenSearch, Datadog, or similar — that we can ship audit events into? If yes, which platform, and is it already HIPAA-scoped?

**Draft answer:** **Needs internal confirmation.** fqdn does not yet have a designated SIEM / log management platform identified for the Spark/Airflow/Ceph stack. Splunk has been mentioned in earlier discussions as a candidate. Whether the corporate-wide platform (if any) is HIPAA-scoped is a question for fqdn Cyber/Security.

**Suggested owner:** Rohn → fqdn Cyber/Security to confirm corporate platform + HIPAA scope.

**Existing TODO entries:** new entry under "Production Architecture Prep — Ksolves Email" (`TODO.md`).

### Q2 — Preference: managed vs self-hosted?

> If no existing SIEM, do you have a preference between a managed service (Splunk Cloud, Datadog) vs a self-hosted open-source option (Wazuh + ELK)? We can recommend either — they have different cost profiles.

**Draft answer:** **Needs internal confirmation.** fqdn does not have a stated preference yet. The decision will be driven by (a) whether corporate already owns Splunk licensing, (b) the operational appetite for hosting Wazuh + ELK on-cluster vs an additional VM footprint, and (c) the per-GB cost profile against the projected daily audit-log volume.

**Suggested owner:** Rohn → fqdn Cyber/Security + Procurement.

### Q3 — Existing log retention policy?

> Do you have an existing log retention policy defined? If not, we'll recommend a 6-year minimum with WORM (write-once read-many) protection on the audit bucket.

**Draft answer:** **Needs internal confirmation.** No retention policy has been defined for the Spark cluster context. **fqdn accepts Ksolves' recommendation: 6-year minimum with WORM protection on the audit bucket.** This aligns with HIPAA § 164.316(b)(2). Implementation likely lives on Ceph RGW (object lock + versioning) or in the SIEM platform's native retention controls, depending on the Q1 answer.

**Suggested owner:** Rohn → confirm with fqdn Compliance on whether the corporate-wide retention policy already covers HIPAA workloads.

---

## Section 2 — Secrets & Encryption Key Management

### Q4 — Existing secrets management platform?

> Do you have an existing secrets management platform — such as HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or CyberArk — in use elsewhere in your organisation? If yes, we can evaluate whether to extend it to this stack rather than deploy a new Vault instance.

**Draft answer:** **CyberArk** is in use at fqdn corporate (per the production architecture summary on the same email thread, 2026-05-06: "Production architecture planning is underway: Key topics include … secrets management (CyberArk)"). **Recommended posture:** extend existing CyberArk to the Spark/Airflow/Ceph stack rather than deploy a new Vault instance, subject to fqdn Cyber/Security agreement on scoping.

**Suggested owner:** Rohn → confirm CyberArk scope + integration model with fqdn Cyber/Security.

### Q5 — Existing PKI / internal CA?

> Do you have an existing PKI or certificate authority for issuing internal TLS certificates? Production requires TLS on all Spark RPC, Ceph RGW, and service-to-service communication.

**Draft answer:** **Needs internal confirmation.** Whether fqdn has an enterprise internal CA for issuing TLS certificates to internal services is unknown to this team. The TLS strategy for Phase 1 is captured in `CP_Okta_v1.1.md` § O0.5 — that section currently leaves the issuer open. If no internal CA exists, options include: ACME (Let's Encrypt or step-ca) for any externally-resolvable services, plus a private CA (HashiCorp Vault PKI or step-ca offline root) for internal-only services.

**Suggested owner:** Rohn → fqdn Cyber/Security + Networking for confirmation of corporate PKI.

---

## Section 3 — Identity & Access Management

### Q6 — Okta confirmed

> We've confirmed Okta is your IdP, integrated with Microsoft AD.

**Draft answer:** **Confirmed.** Okta brokers SSO; Active Directory remains authoritative for user lifecycle (joiner/mover/leaver). Detailed integration architecture for the Spark/Airflow/Ceph stack is in `CP_Okta_v1.1.md`. Okta tenant configuration, AD agent deployment, group/role mapping, reverse-proxy gateway for Hadoop UIs, RGW STS provider registration, and Snowflake federation are all scoped under tasks O0.1 through O2.4 of that document.

### Q7 — Existing RBAC / entitlement model for PHI vs de-identified data?

> Do you have an existing RBAC or entitlement model defined for who should have access to PHI data vs de-identified/aggregated data? This directly informs how we configure Apache Ranger column masking policies.

**Draft answer:** **Needs internal confirmation.** This is the question that drives the Apache Ranger column-masking policy. fqdn has not yet defined a documented PHI-vs-de-identified entitlement model for this platform. Existing TODO entry tracks this as a Rohn-owned item to coordinate with Cyber/Security. Recommended deliverable: a one-page entitlement matrix mapping AD/Okta groups to (PHI-eligible / de-identified-only / aggregated-only) data tiers — this becomes the input to Ranger policy authoring.

**Suggested owner:** Rohn → fqdn Cyber/Security + Compliance.

### Q8 — Existing PAM solution (BeyondTrust, CyberArk, etc.)?

> Is there an existing privileged access management (PAM) solution in place — such as BeyondTrust, CyberArk, or similar — for controlling and auditing administrative access to servers?

**Draft answer:** **CyberArk is in use at fqdn** (per Q4). Whether the existing CyberArk deployment also handles privileged session management for Linux server access (vs just secrets vaulting) is a question for Cyber/Security. **Recommended posture:** extend existing CyberArk for PAM if the corporate footprint already covers session brokering; otherwise pair Okta Advanced Server Access (ASA) per `CP_Okta_v1.1.md` § O1.4 for ephemeral SSH certificates.

**Suggested owner:** Rohn → fqdn Cyber/Security to confirm CyberArk PAM scope.

---

## Section 4 — Network & Perimeter

### Q9 — Existing corporate VPN or ZTNA?

> Is there an existing corporate VPN or Zero Trust Network Access (ZTNA) solution that administrators use to reach on-premise infrastructure? If yes, which one? This affects whether we need to deploy WireGuard on the remote service host or if admin access is already covered.

**Draft answer:** **VMware Horizon VDI** is the planned permanent admin-access path for Ksolves and any external administrative work (per `Phases_Critical_Path_Development_v1.4.md` § BLOCKER.1 Phase 1B). For internal fqdn engineering staff accessing the cluster, the existing corporate access path is the network team's call — **needs internal confirmation** on whether there's a separate VPN or ZTNA layer beyond AD-authenticated network presence on the corporate LAN.

**Suggested owner:** Rohn → fqdn Networking + Cyber/Security.

### Q10 — Existing Proxmox firewall / VLAN configuration?

> Are there any existing firewall policies, network segmentation rules, or VLAN configurations in place on the Proxmox hosts that we need to work within or extend?

**Draft answer:** **Yes — VLAN segmentation is in place on the dev cluster.** Per the captured `/etc/network/interfaces` from `msb-pmc03-01`: VLAN 37 (management, 10.1.37.0/24), VLAN 38 (cluster), VLAN 39 (CephFS traffic), all trunked through bond0 (LACP, 802.3ad) at MTU 9000 internally. Firewall policy details (corporate firewall rules between VLANs, ingress/egress rules to/from the Spark cluster) are owned by fqdn Networking. The MTU mismatch issue between the cluster's 9000 and the remote-path's 1400 was resolved by fqdn Networking on 2026-05-06.

**Suggested owner:** Rohn → fqdn Networking for documented firewall policy.

---

## Section 5 — Compliance & Risk

### Q11 — HIPAA Risk Assessment completed?

> Has a formal HIPAA Risk Assessment (per §164.308(a)(1)) been completed for this platform or the broader organisation? If yes, can we review it? If not, we should plan for one as part of the production readiness process.

**Draft answer:** **Needs internal confirmation.** Whether fqdn has a current HIPAA Risk Assessment that covers (or can be amended to cover) this Spark/Airflow/Ceph platform is a question for fqdn Compliance. If no current assessment exists, **fqdn accepts Ksolves' recommendation to plan one as part of the production readiness deliverables.**

**Suggested owner:** Rohn → fqdn Compliance / Legal.

### Q12 — Snowflake + cloud staging BAAs signed?

> Have Business Associate Agreements (BAAs) been signed with Snowflake and your cloud staging provider (Azure/AWS)? These are required before PHI can flow to those platforms.

**Draft answer:** **Needs internal confirmation.** BAA status with Snowflake and Azure (the confirmed cloud staging target per `Phases_Critical_Path_Development_v1.4.md` § P0.3) is a question for fqdn Legal/Compliance. **This is a hard gate: PHI cannot flow to either platform until the BAAs are signed.** Recommended action: confirm BAA status before any production cutover; if not signed, treat as a blocker on the production timeline.

**Suggested owner:** Rohn → fqdn Legal/Compliance.

### Q13 — Existing incident response / breach notification runbook?

> Do you have an existing incident response or breach notification runbook? HIPAA §164.308(a)(6) requires documented procedures. If not, we can help draft one as part of the production deliverables.

**Draft answer:** **Needs internal confirmation.** Whether fqdn has a corporate-wide IR/breach runbook that covers (or can be amended to cover) this platform is a question for fqdn Cyber/Security. If no platform-specific runbook exists, **fqdn accepts Ksolves' offer to help draft one** as a production deliverable, building on whatever corporate IR posture already exists.

**Suggested owner:** Rohn → fqdn Cyber/Security.

### Q14 — Existing vulnerability scanning / patch management?

> Is there an existing vulnerability scanning or patch management process? We'll need to incorporate regular scanning of the cluster nodes into the production security posture.

**Draft answer:** **Needs internal confirmation.** Whether fqdn corporate runs a vulnerability scanner (Tenable, Qualys, Rapid7, etc.) and a patch management cadence on Linux hosts is a question for fqdn Cyber/Security and IT Operations. The Spark cluster nodes (RHEL 9.4) should be enrolled in whichever corporate process exists.

**Suggested owner:** Rohn → fqdn Cyber/Security + IT Operations.

---

## Section 6 — Operational

### Q15 — On-call / incident response capability?

> What is your team's current on-call / incident response capability for the cluster? This affects how we design monitoring alerts and whether we recommend a managed detection layer on top of the SIEM.

**Draft answer:** **Needs internal confirmation.** fqdn's on-call posture for this platform during production is not yet defined. Inputs needed: (a) which fqdn team owns first-line response (Infrastructure, Cyber, Application Owner?), (b) PagerDuty / Opsgenie / Splunk On-Call presence, (c) whether 24×7 coverage is in scope or business-hours-plus-best-effort. Recommended: define an on-call rotation + escalation matrix as a production-readiness deliverable.

**Suggested owner:** Rohn → fqdn IT Operations + Application Owner.

### Q16 — Existing backup / DR processes?

> Are there any existing backup and disaster recovery processes for the on-premise infrastructure? Ceph provides storage HA, but application-level backup (Airflow metadata DB, Vault data, Ranger policies) also needs to be covered.

**Draft answer:** **Needs internal confirmation.** Cluster-level: Ceph provides storage redundancy at the OSD level (replication = 2 in dev per the storage reference; production may require replication = 3). Application-level: Airflow metadata Postgres DB, any Ranger policy DB, and CyberArk-vaulted secrets all need a separate backup story. Whether fqdn corporate backup tooling (Veeam, Commvault, Proxmox Backup Server, etc.) covers this on-premise footprint is a question for fqdn IT Operations. **Recommended:** dedicated Proxmox Backup Server target for VM-level backups plus application-aware backups (Postgres pg_dump, Ranger policy export) on a daily schedule.

**Suggested owner:** Rohn → fqdn IT Operations.

---

## Open Items Captured in fqdn TODO After Drafting These Responses

| Question | TODO entry | Owner |
|---|---|---|
| Q1, Q2, Q3 | "Define centralized logging approach + retention policy for production" | Rohn |
| Q1–Q3 (CP follow-up) | "CP v1.5: New task — Centralized Audit Logging + Retention Policy (HIPAA-driven)" | Development team + Cyber/Security |
| Q4, Q8 | (no new TODO; existing CyberArk extension assumed) | Rohn |
| Q5 | (existing `CP_Okta_v1.1.md` § O0.5 covers TLS) | Rohn |
| Q7 | "Confirm IAM/RBAC model — specifically PHI vs de-identified entitlement boundaries" | Rohn |
| Q9, Q10 | "Send network-related questions and requirements to fqdn infrastructure/network team" | Rohn |
| Q11, Q12, Q13 | (no separate TODOs yet — one consolidated "Compliance prep" item could capture all three) | Rohn |
| Q14 | (no separate TODO — likely subsumed under Cyber/Security coordination) | Rohn |
| Q15, Q16 | (no separate TODO — defer until production planning sub-project is cut) | Rohn |

---

## Recommended Next Steps

1. **User reviews this draft and edits where corporate posture is known but not yet captured here.**
2. After edits, promote `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` → `correspondence/Document/prod_architecture_questionnaire_responses_v1.0.md`.
3. Reply to vendor lead's email with the relevant subset of confirmed answers; mark unresolved items with target dates for follow-up.
4. As confirmations come in from Cyber/Security, Networking, Legal, and IT Operations, bump this doc to v1.1 and update the answers in place; track Q-by-Q closure in the TODO.

---

_End of draft._
