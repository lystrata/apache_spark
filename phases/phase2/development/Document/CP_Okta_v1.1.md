# Critical Path — Okta + Active Directory Integration for Spark Phase 1

_Version 1.1 · Last updated 2026-05-05 · v1.5-sync notes added 2026-05-08_  
_Companion document to `Phases_Critical_Path_Development_v1.5.md` and `CP_HIPAA_Compliance_v1.0.md` · Audit + critical-path additions for enterprise Okta SSO with AD as authoritative directory_

> **v1.5 Sync (2026-05-08):** No changes to Okta scope or task list. Cross-references bumped to `Phases_Critical_Path_Development_v1.5.md`. Three points worth noting:
> - **AD DC enumeration closed 2026-05-06** — 7 DCs across 4 sites (Windsor ×2, Garfield ×1, South ×2, MSB RW + RO). Captured in `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § AD domain controllers. Relevant to § O0.4 (network egress requirements) here. **Open follow-up:** confirm with fqdn AD admins whether vendor traffic should be DC-pool-wide or steered to specific DCs (e.g., MSB-RO for query, MSB-RW for writeback).
> - **BLOCKER.4 (NEW 2026-05-06)** in main CP — Phase 1B vendor-access isolation gate. The vendor-egress allowlist that gates Phase 1B must include the AD DC pool documented above plus Okta endpoints. During Phase 1A (Webex), Okta integration work can begin behind the screen-share without exposing the AD/Okta endpoints to vendor-side network reach.
> - **Nginx scope correction 2026-05-07** — restored as install-in-scope on the Airflow VM (companion: `MSB-PMC01_airflow_host_briefing_v1.3.md`; v1.3 carries 2026-05-11 supersession notice — msb-pmc01 retiring; Airflow host migrating to msb-pmc04). One of Nginx's candidate roles is **Okta SSO front-door routing**; if Ksolves activates that role post-install, it intersects with Okta integration tasks here. Coordinate when Ksolves makes the activation decision.
>
> **Update 2026-05-08 — flag follow-up with Paul Barber:** From the 2026-05-08 review punch-list, the user wants Okta + AD integration explicitly flagged as a follow-up topic with Paul Barber (Cyber). Likely topics: (a) Okta tenant configuration approval (groups, claim mappings, redirect URIs), (b) the gateway-vs-per-app topology choice (Step 3 in this document), (c) whether the gateway sits on the Airflow VM (P1.0) or migrates to the proposed msb-pmc04 third cluster (see CP v1.5 § BLOCKER.4 msb-pmc04 note), (d) Okta Advanced Server Access (ASA) for ephemeral SSH certs (Step 7) — Paul's call on whether ASA is in scope or fqdn uses an alternative SSH-CA solution.

---

<a id="document-overview"></a>

## Document Overview

This document inventories every authentication touchpoint in the Phase 1 Spark cluster build, maps each to a concrete Okta integration pattern, and produces a critical-path task list (`O0.x`, `O1.x`, `O2.x`) that can be merged into `Phases_Critical_Path_Development_v1.5.md` once Cyber Security has approved the architecture.

The current Phase 1 plan mentions Okta in three places (P1.0 step 4 — "Install Okta SSO integration"; P1.0 step 8 — "Provide Okta OIDC credentials for Airflow SSO configuration"; P2.2 step 7 — "Set up Airflow web UI ... with basic auth or Okta integration") but does **not** specify the actual implementation work that those one-line items represent: tenant configuration, AD agent deployment, group/role mapping, reverse-proxy gateway for the Hadoop UIs that have no native OIDC, RGW STS provider registration, federated SSH access, or Snowflake federation. This document fills those gaps.

<a id="methodology"></a>

### Methodology

Each integration claim is supported by at least two independent authoritative sources (vendor official docs, peer-reviewed implementation guides, or recognized industry references), per the security-context citation rule in `CLAUDE.md`. Citations appear inline as superscript footnotes; full Turabian-style entries appear in the Bibliography.

Tasks are numbered `O<phase>.<step>`:

- **O0.x** — Foundation (Okta tenant, AD agent, group structure, network egress) — must complete before any service integration begins.
- **O1.x** — Per-service integrations (Airflow, History UI, YARN UI, RGW, SSH, Snowflake), executable in parallel after O0 is done.
- **O2.x** — Validation, cutover, audit, and documentation.

Each task includes status, owner, dependencies, action steps as GFM checkboxes, verification criteria, and effort estimate — matching the style of `Phases_Critical_Path_Development_v1.5.md`.

---

<a id="table-of-contents"></a>

## Table of Contents

- [Scope](#scope)
- [Inventory: Auth Surfaces in Phase 1](#auth-surfaces-inventory)
- [Architecture Decisions](#architecture-decisions)
- [Critical Path — O0: Foundation](#cp-o0-foundation)
  - [O0.1 — Okta Tenant App Registrations](#o0-1-tenant-apps)
  - [O0.2 — Okta AD Agent Deployment & AD ↔ Okta Sync](#o0-2-ad-agent)
  - [O0.3 — Okta Group Architecture](#o0-3-group-architecture)
  - [O0.4 — Network Egress & Firewall Rules](#o0-4-network)
  - [O0.5 — TLS Certificate Strategy](#o0-5-tls)
- [Critical Path — O1: Per-Service Integrations](#cp-o1-services)
  - [O1.1 — Airflow OIDC via FAB Auth Manager](#o1-1-airflow)
  - [O1.2 — Reverse-Proxy Gateway for Hadoop UIs (Spark History, YARN RM, Spark App)](#o1-2-gateway)
  - [O1.3 — Ceph RGW OIDC Provider + STS Trust Policies](#o1-3-rgw)
  - [O1.4 — SSH/Bastion Access via Okta Advanced Server Access (ASA)](#o1-4-asa)
  - [O1.5 — Snowflake SAML Federation with Okta](#o1-5-snowflake)
- [Critical Path — O2: Validation & Cutover](#cp-o2-validation)
  - [O2.1 — End-to-End SSO Smoke Test](#o2-1-smoke-test)
  - [O2.2 — Group / Role Mapping Audit](#o2-2-mapping-audit)
  - [O2.3 — Offboarding & Revocation Drill](#o2-3-offboarding)
  - [O2.4 — As-Built Documentation & Compliance Citations](#o2-4-asbuilt)
- [Group / Role Mapping Matrix](#group-role-matrix)
- [Network Egress Requirements](#network-egress)
- [Open Questions for fqdn Cyber Security](#open-questions)
- [Cross-References to Phase 1 TODO](#cross-references)
- [Assumptions & Dependencies](#assumptions)
- [Reference Documents](#reference-documents)
- [Footnotes](#footnotes)
- [Bibliography](#bibliography)

---

<a id="scope"></a>

## Scope

**In scope (this document):**

- Authentication and authorization for every interactive endpoint surfaced by the Phase 1 Spark cluster: Airflow webserver, Spark History Server UI (port 18080), YARN ResourceManager UI (port 8088), per-application Spark UI (port 4040), Ceph RGW S3 endpoint, RGW admin operations, and SSH/console access to all Worker, RM, and Remote Airflow VMs.
- Federated identity flow from fqdn Active Directory → Okta → cluster services.
- Snowflake federation (the Snowflake account itself remains fqdn-managed per `Phases_Critical_Path_Development_v1.5.md` § P2.3 Snowflake Scope Note, but the SSO integration is in scope here).

**Out of scope (this document):**

- Snowflake-internal RBAC, warehouse provisioning, COPY INTO authorship — fqdn responsibility per Phase 1 plan.
- Spark application-level data authorization (Ranger / row-level filtering / column masking) — deferred to a future phase.
- Replacing Spark's native Kerberos/delegation-token machinery for inter-daemon traffic — Phase 1 retains Hadoop's standard delegation token model for executor-to-NM-to-RM communication.¹ Okta sits at the **user-facing** edge only. **Cross-reference:** the HIPAA-driven inter-daemon work — Kerberos realm + keytab provisioning, RPC AES-GCM encryption, SSL/TLS on shuffle and IO encryption, Web UI ACL via custom javax servlet filter, and SSE on Ceph buckets — is tracked in `CP_HIPAA_Compliance_v1.0.md`. That sub-project owns the on-cluster identity protocol; this Okta document owns user-facing SSO only. Where the two intersect (Web UI ACL, SSH/ASA), the connection is called out explicitly in the relevant `O1.x` task.

---

<a id="auth-surfaces-inventory"></a>

## Inventory: Auth Surfaces in Phase 1

The Phase 1 cluster exposes the following endpoints that require authentication. Each is mapped to its native auth capability and the Okta-integration approach selected below.

| # | Service | Native Auth Options | Selected Okta Approach | Notes |
|---|---|---|---|---|
| 1 | Airflow webserver (port 8080) | Flask-AppBuilder (DB, LDAP, OAuth/OIDC, SAML) | **Direct OIDC via FAB**² | `okta` is a first-class provider in FAB |
| 2 | Spark History Server UI (port 18080) | Servlet auth filter (Kerberos/SPNEGO or none) | **Reverse-proxy SSO gateway** | No native OIDC; gateway terminates Okta and forwards |
| 3 | YARN ResourceManager UI (port 8088) | SPNEGO/Kerberos via RM Proxy¹ | **Reverse-proxy SSO gateway** | RM Proxy is Kerberos-only; gateway sits in front |
| 4 | Per-app Spark UI (port 4040) | Same as YARN RM (proxied through RM Proxy) | Inherits gateway from #3 | App UI is proxied via RM by default |
| 5 | Ceph RGW S3 API | AWS SigV4 + access/secret keys | **STS AssumeRoleWithWebIdentity** + OIDC provider³ | Static keys retired except for service principals |
| 6 | Ceph RGW admin ops | `radosgw-admin` CLI on hosts | SSH-gated (#7); no Okta needed at API layer | |
| 7 | SSH to all VMs | Static SSH keys / passwords | **Okta Advanced Server Access (ASA)**⁴ | Replaces static keys with ephemeral certs |
| 8 | Proxmox web UI | Proxmox PAM/PVE/AD realm | **AD realm via Okta-synced AD** | Inherits Okta MFA via AD password sync; covered in `BLOCKER.1` for Ksolves |
| 9 | Snowflake account | Snowflake-native or SAML federation | **SAML 2.0 federation with Okta**⁵ | Pre-built Snowflake↔Okta integration |
| 10 | Grafana / Prometheus (out of Phase 1 scope) | — | Deferred | Listed for completeness |

References to native auth options for #2 and #3 are supported by Apache Hadoop's YARN security documentation, which states that "YARN provides a straightforward way of giving every YARN application SPNEGO authenticated web pages: it implements SPNEGO authentication in the Resource Manager Proxy"¹ — meaning the Hadoop UIs assume Kerberos as the on-cluster identity protocol, which is incompatible with Okta-issued OIDC/SAML tokens without a translating gateway.

---

<a id="architecture-decisions"></a>

## Architecture Decisions

### AD-1 — Active Directory remains the authoritative directory; Okta brokers SSO

**Decision:** fqdn AD continues to own user lifecycle (joiner-mover-leaver). Okta integrates with AD via the **Okta AD Agent**, configured in **delegated authentication** mode so that AD performs every credential check and Okta never persistently stores user passwords.⁶

**Rationale:** Per Okta's published architecture, "When Okta is integrated with an Active Directory (AD) instance, delegated authentication is enabled by default. ... the AD domain controller validates the username and password. ... With this authentication mechanism, the user's password is never stored in the Okta service and your directory is maintained as the immediate and ultimate source for credential validation."⁶ This satisfies enterprise AD-as-source-of-truth constraints and avoids creating a parallel password store in Okta.

**Cross-source confirmation:** Okta's Directory Integration architecture whitepaper⁷ describes the same model — agent-mediated delegated auth — and notes the agent supports redundant deployment ("multiple Okta AD and/or LDAP Agents running in your environment to provide redundancy").⁶

### AD-2 — Federation protocol per service

**Decision:**

- **OIDC** for every service that supports it natively (Airflow,² Snowflake when used with External OAuth, future Grafana).
- **SAML 2.0** only where required (Snowflake federated SSO uses SAML 2.0 in its native Okta integration⁵).
- **Reverse-proxy SSO** (oauth2-proxy or Apache Knox 2.1.0) for the Hadoop-ecosystem UIs that have neither native OIDC nor a clean SAML path: Spark History, YARN RM, Spark App UIs.⁸,⁹

**Rationale:** OIDC is preferred where available because token introspection and refresh are well-defined. The Hadoop UIs were designed for Kerberos-era environments; the canonical path to put modern SSO in front of them is a reverse-proxy gateway that terminates the IdP token and forwards an authenticated identity header to the upstream UI.⁸ Apache Knox 2.1.0 is the Apache-blessed gateway for this purpose and supports YARN ResourceManager UI explicitly⁹; oauth2-proxy is a lighter-weight alternative when Knox's full Hadoop service catalog is not needed.⁸

### AD-3 — Single SSO gateway, not per-app gateways

**Decision:** Deploy **one** reverse-proxy gateway VM that fronts Spark History, YARN RM, and Spark App UIs. Airflow integrates OIDC directly (no gateway hop). Snowflake federates directly (no gateway).

**Rationale:** A single gateway means one Okta app registration for the cluster UIs, one TLS endpoint to manage, one place to audit access logs. Per Apache Knox documentation, KnoxSSO "abstracts the actual identity provider integration away from participating applications so that they only need to be aware of the KnoxSSO cookie."⁹ This pattern works equally with oauth2-proxy.⁸

### AD-4 — Static S3 keys retained only for service-to-service flows

**Decision:** Human users authenticate to RGW via STS `AssumeRoleWithWebIdentity` using their Okta JWT.³,¹⁰ Service principals (Spark drivers, Airflow workers, History Server) continue to use long-lived access/secret keys stored in HashiCorp Vault or equivalent — these are non-interactive and do not benefit from federation.

**Rationale:** Per Ceph official documentation, RGW supports `AssumeRoleWithWebIdentity` such that "applications authenticate via your existing SSO system to obtain a JWT, which they then use to request a temporary credential directly from the STS API"³ — eliminating static credentials for human users while preserving the simpler keyed model for daemons. Ceph.io's 2025 blog post on STS modernization¹⁰ explicitly recommends this hybrid: STS for federated humans, static keys for service identities.

---

<a id="cp-o0-foundation"></a>

## Critical Path — O0: Foundation

These tasks must complete before any per-service integration (O1.x) begins. They are prerequisites for the Phase 1 plan's existing P1.0 step 4 ("Install Okta SSO integration") and P2.2 step 7 ("Set up Airflow web UI ... with Okta integration").

<a id="o0-1-tenant-apps"></a>

### 🟣 O0.1 — Okta Tenant App Registrations

- **Status:** OPEN — fqdn IT/Cyber Security
- **Priority:** CRITICAL — Gate for every O1.x service integration
- **Context:** Each Okta-protected endpoint requires its own application registration in the Okta tenant. App registrations carry the client ID, client secret (or signing key), redirect URIs, and group/claim policy.
- **Prerequisites:**
  - [ ] fqdn Okta tenant accessible to the engineer performing setup
  - [ ] Final hostnames (or DNS plan) for Airflow webserver, gateway, RGW endpoint
- **Actions:**
  - [ ] Create OIDC Web app in Okta for Airflow (`spark-airflow`) — redirect URI `https://<airflow-host>/oauth-authorized/okta`²
  - [ ] Create OIDC Web app in Okta for the SSO gateway (`spark-ui-gateway`) — redirect URI `https://<gateway-host>/oauth2/callback` (oauth2-proxy convention⁸) or `/knoxsso/api/v1/websso` (Knox convention⁹)
  - [ ] Create OIDC Web app in Okta for Ceph RGW STS (`spark-rgw-sts`) — used by browser/CLI clients calling `AssumeRoleWithWebIdentity`
  - [ ] Create SAML 2.0 SP app in Okta for Snowflake (`spark-snowflake`) using Okta's pre-built Snowflake integration⁵
  - [ ] Define authorization server claims for each app: `groups`, `email`, `preferred_username`, `sub`
  - [ ] Capture client IDs, client secrets, signing keys/JWKS endpoints — store in fqdn secrets vault, share securely with Ksolves where required (e.g., Airflow needs the Airflow app's client_id/secret)
  - [ ] Document token lifetimes (access token, ID token, refresh token) consistent with corp policy
- **Verification:** All four apps appear in Okta admin console with correct redirect URIs and claim configs; one test user can complete the OIDC flow against each app's authorization endpoint.
- **Owner:** fqdn IT/Cyber Security
- **Estimated Effort:** 4–6 hours (4 app registrations + claims + secret distribution)

<a id="o0-2-ad-agent"></a>

### 🟣 O0.2 — Okta AD Agent Deployment & AD ↔ Okta Sync

- **Status:** PENDING — likely already in place if fqdn uses Okta enterprise-wide; verify
- **Priority:** CRITICAL — Without AD ↔ Okta sync, no fqdn user can authenticate via Okta
- **Context:** The Okta AD Agent installs on a domain-joined Windows server and performs (a) directory import of users/groups from AD into Okta and (b) delegated authentication of credential checks back to AD domain controllers.⁶,⁷
- **Prerequisites:**
  - [ ] AD service account with the rights documented in Okta's AD agent installation guide⁶ (read for users/groups, password sync if directional sync is enabled)
  - [ ] Windows server (or Windows VM) joined to the AD domain, network egress to Okta tenant on TCP 443
  - [ ] Okta tenant admin able to register a new AD domain
- **Actions:**
  - [ ] Install Okta AD Agent on at least two domain-joined hosts for redundancy⁶ (Okta documentation states the architecture "supports multiple Okta AD and/or LDAP Agents running in your environment to provide redundancy")
  - [ ] Configure delegated authentication mode⁶ — confirm "Activate Delegated Authentication" is enabled in Okta admin console
  - [ ] Define AD OUs to import (limit to engineering/data OUs that include Spark cluster users)
  - [ ] Define AD groups to import (see O0.3 for required group set)
  - [ ] Schedule periodic sync (Okta default 1 hour) and run an initial full sync
  - [ ] Verify imported users appear in Okta with `Active` status and AD-linked source
  - [ ] Test delegated auth: log in to Okta with an AD credential and confirm AD DC sees the lookup in its security log
- **Verification:** Okta admin console shows AD agent status `Active` on both hosts; AD groups appear in Okta; a test user can log in to Okta with AD credentials and the AD password is **not** stored in Okta (confirmed by Okta admin → People → user profile → no password attribute).⁶
- **Owner:** fqdn IT (AD) + fqdn IT (Okta admin)
- **Estimated Effort:** 4–8 hours (agent install on two hosts + sync config + test)
- **Critical Note:** Okta documents that "directory passwords aren't synchronized to Okta because delegated authentication performs the authentication and there's no Okta password"⁶ — this is the desired behavior. If the team has previously enabled "Synchronize passwords from Active Directory to Okta," disable it before delegated auth is finalized to avoid storing AD password hashes in Okta.

<a id="o0-3-group-architecture"></a>

### 🟣 O0.3 — Okta Group Architecture

- **Status:** OPEN — fqdn IT/Cyber Security
- **Priority:** HIGH — Drives every per-service authorization decision in O1.x
- **Context:** Authorization in each Okta-protected service is driven by group claims. Defining the group taxonomy up front avoids the situation where every service invents its own groups and the resulting access matrix becomes unauditable.
- **Prerequisites:**
  - [ ] O0.2 (AD ↔ Okta sync) operational so that AD groups can be referenced
- **Actions:**
  - [ ] Decide whether cluster groups live in AD (synced via O0.2) or are Okta-native. **Recommended:** AD-native, so joiner/leaver lifecycle remains in AD.
  - [ ] Create the following groups in AD (and confirm sync to Okta):
    - [ ] `fqdn-spark-admin` — full cluster admin (Airflow admin, YARN admin, RGW admin S3 ops)
    - [ ] `fqdn-spark-developer` — submit jobs, view all UIs, read/write own RGW prefix
    - [ ] `fqdn-spark-analyst` — read-only Airflow viewer, History UI, RGW read on output prefix
    - [ ] `fqdn-spark-oncall` — on-call SSH access via ASA + read-only YARN RM
    - [ ] `fqdn-snowflake-loader` — Snowflake-side group used by federated logins for ETL operators
  - [ ] For each group, document: (a) which services it grants, (b) which Okta apps assign it, (c) AD OU/membership rules
  - [ ] Assign all four Okta apps from O0.1 to the appropriate groups (every app should at least have `fqdn-spark-admin` for break-glass access)
- **Verification:** Each group exists in AD, syncs to Okta, and is assigned to every app it should grant; a test member of `fqdn-spark-developer` can complete OIDC against the Airflow app and Okta returns the group claim.
- **Owner:** fqdn IT (AD) + fqdn IT (Okta) + fqdn data-platform lead (group definitions)
- **Estimated Effort:** 3–4 hours (group creation + assignment + verification)

<a id="o0-4-network"></a>

### 🟣 O0.4 — Network Egress & Firewall Rules

- **Status:** OPEN — fqdn Network Team
- **Priority:** CRITICAL — Without egress to Okta, no token can be validated
- **Context:** Every Okta-protected service must reach the Okta tenant for OIDC discovery, authorization redirects, JWKS fetches, and (for ASA) certificate signing requests. The Phase 1 plan's `P0.7` (MSB-PMC01 ↔ MSB-PMC03 connectivity) addresses on-cluster networking; Okta integration adds an outbound dependency.
- **Prerequisites:**
  - [ ] Phase 1 `P0.7` complete (cluster ↔ Remote Airflow Server connectivity verified)
- **Actions:**
  - [ ] Open outbound TCP 443 from each of the following hosts to `<fqdn-tenant>.okta.com` and `<fqdn-tenant>.oktapreview.com` (test tenant if used):
    - [ ] Remote Airflow Server (MSB-PMC01) — Airflow OIDC redirect + JWKS
    - [ ] SSO gateway VM (MSB-PMC01 or MSB-PMC03 — see O1.2) — OIDC for Hadoop UIs
    - [ ] All three Worker VMs and both YARN RM VMs (MSB-PMC03) — ASA certificate refresh⁴
    - [ ] Spark History Server VM — ASA + JWKS (if it validates tokens locally)
    - [ ] All RGW hosts — JWKS fetch for STS WebIdentity verification³
  - [ ] Open outbound TCP 443 from each cluster VM to `gateway.<region>.sft.okta.com` (Okta ASA gateway) and `<fqdn-team>.scaleft.com` if ASA team uses ScaleFT-legacy hostnames⁴
  - [ ] Open outbound TCP 443 to `*.snowflakecomputing.com` from any host that initiates Snowflake connections (already required by Phase 1 P0.3 — verify scope includes federated login redirects)
  - [ ] Confirm no SSL inspection middlebox breaks Okta JWT signature validation; Okta's signing keys must be retrievable directly from `<fqdn-tenant>.okta.com/oauth2/v1/keys`
- **Verification:** From each host, `curl -v https://<fqdn-tenant>.okta.com/.well-known/openid-configuration` returns 200 with valid JSON; ASA client `sft enroll` succeeds without proxy/TLS errors.
- **Owner:** fqdn Network Team
- **Estimated Effort:** 2–4 hours (firewall change requests + testing)

<a id="o0-5-tls"></a>

### 🟣 O0.5 — TLS Certificate Strategy

- **Status:** OPEN
- **Priority:** HIGH — Browser-trusted certs are required for every redirect URI registered with Okta
- **Context:** Okta will redirect browsers to each app's redirect URI; modern browsers refuse OIDC redirects to untrusted-cert hosts. Plan certificate issuance before app registrations are finalized.
- **Prerequisites:** Okta app registrations from O0.1 (or vice versa — work them in parallel)
- **Actions:**
  - [ ] Decide cert source: corporate ACME / internal CA / public CA per host
  - [ ] Issue certs for: Airflow webserver hostname, SSO gateway hostname, RGW S3 endpoint hostname (if browser STS is exposed)
  - [ ] Document cert renewal schedule and ownership
  - [ ] Install certs on respective hosts before O1.x integration begins
- **Verification:** Each Okta-redirected hostname returns a browser-trusted cert (no warnings); cert chain verified with `openssl s_client -connect <host>:443 -showcerts`
- **Owner:** fqdn Network Team / fqdn IT
- **Estimated Effort:** 2–3 hours

---

<a id="cp-o1-services"></a>

## Critical Path — O1: Per-Service Integrations

These tasks become unblocked once O0.1–O0.5 are complete. They can run in parallel except where Phase 1 dependencies (e.g., the Remote Airflow Host must exist before O1.1 can run) sequence them.

<a id="o1-1-airflow"></a>

### 🟣 O1.1 — Airflow OIDC via FAB Auth Manager

- **Status:** PENDING O0.1, O0.2, O0.3, P1.0 (Remote Airflow Host), P2.2 (Airflow installed)
- **Priority:** HIGH
- **Context:** Apache Airflow's webserver authenticates via Flask-AppBuilder (FAB). Per the FAB providers documentation, Airflow's "currently supported providers" include `okta` as a first-class entry, so no custom security manager is required for the basic flow.² Configuration is via `webserver_config.py` — set `AUTH_TYPE = AUTH_OAUTH` and populate `OAUTH_PROVIDERS`. Without `AUTH_TYPE = AUTH_OAUTH`, "the OAuth providers will not be activated even if OAUTH_PROVIDERS is configured."²
- **Prerequisites:**
  - [ ] Airflow 2.10.4 installed (Phase 1 `P2.2`)
  - [ ] Okta `spark-airflow` app from O0.1 with client ID/secret available
  - [ ] `fqdn-spark-admin`, `fqdn-spark-developer`, `fqdn-spark-analyst` groups assigned to that app (O0.3)
  - [ ] Python `authlib` package installed in the Airflow venv²
- **Actions:**
  - [ ] `pip install authlib` in the Airflow venv
  - [ ] Edit `$AIRFLOW_HOME/webserver_config.py`:
    - [ ] Set `AUTH_TYPE = AUTH_OAUTH`
    - [ ] Populate `OAUTH_PROVIDERS = [{"name": "okta", "icon": "fa-circle-o", "token_key": "access_token", "remote_app": {...}}]` with Okta endpoints (`api_base_url=https://<tenant>.okta.com/oauth2/v1/`, `access_token_url=.../token`, `authorize_url=.../authorize`, client ID/secret from O0.1)²
    - [ ] Set `AUTH_USER_REGISTRATION = True` and `AUTH_USER_REGISTRATION_ROLE = "Public"` so first-time logins land in a low-privilege role
    - [ ] Define `AUTH_ROLES_MAPPING = {"fqdn-spark-admin": ["Admin"], "fqdn-spark-developer": ["User"], "fqdn-spark-analyst": ["Viewer"]}` — maps Okta groups to FAB roles²
    - [ ] Set `AUTH_ROLES_SYNC_AT_LOGIN = True` so role changes in Okta propagate at next login
  - [ ] Restart Airflow webserver
  - [ ] Test login: each test user from each group lands in the correct FAB role
- **Verification:** A user in `fqdn-spark-admin` lands as `Admin` and sees all DAGs; a `fqdn-spark-analyst` user lands as `Viewer` and cannot trigger DAGs; logout redirects through Okta.
- **Owner:** Ksolves (config) + fqdn (Okta credentials)
- **Estimated Effort:** 2–4 hours (config + role mapping verification)
- **Citation Note:** This configuration pattern is corroborated by Apache Airflow's FAB SSO documentation² and by independent walk-throughs at Riskified Tech¹¹ and Scribd Tech,¹² both of which describe the same `webserver_config.py` + `authlib` pattern with Okta groups → FAB roles mapping.

<a id="o1-2-gateway"></a>

### 🟣 O1.2 — Reverse-Proxy SSO Gateway for Hadoop UIs (Spark History, YARN RM, Spark App)

- **Status:** PENDING O0.1, O0.4, O0.5, P0.0 (Ceph), P1.1 (Spark History Server), P1.2 (YARN RM HA)
- **Priority:** HIGH — Without this, Spark History and YARN RM UIs are either unauthenticated or accessible only via SSH tunnel
- **Context:** Spark History Server, YARN ResourceManager UI, and per-application Spark UIs were designed for Kerberos/SPNEGO. The YARN RM Proxy implements SPNEGO and routes app UIs through it,¹ but SPNEGO is incompatible with Okta-issued OIDC tokens. The standard solution is a reverse-proxy gateway that terminates Okta and forwards an authenticated identity header (or sets a cookie) that the upstream UI accepts. Two viable gateways:
  - **Option A — Apache Knox 2.1.0:** Apache-blessed Hadoop SSO gateway. Supported services in 2.1.0 include YARN ResourceManager, Apache Livy (Spark REST), and a generic UI proxy. Configures via `pac4j` provider for OIDC.⁹
  - **Option B — oauth2-proxy + Nginx:** Lightweight reverse proxy that supports Okta as a first-class provider and forwards `X-Forwarded-User`/`X-Forwarded-Email` headers to upstreams.⁸
- **Recommendation:** **Option B (oauth2-proxy + Nginx)** for Phase 1. Knox brings a large surface area (full Hadoop service catalog including services Phase 1 does not use); oauth2-proxy is purpose-built for "stick OIDC in front of N web apps," which is exactly the Phase 1 need. Knox remains a viable migration path if Phase 2 adds HBase/Hive/Solr.
- **Prerequisites:**
  - [ ] Phase 1 `P1.4` (Nginx on Remote Airflow Host) — gateway can co-locate with this Nginx, **or** stand up dedicated gateway VM
  - [ ] Okta `spark-ui-gateway` app from O0.1
  - [ ] TLS cert from O0.5
- **Actions:**
  - [ ] Decide co-location vs. dedicated VM. **Recommended:** co-locate with the existing P1.4 Nginx since it already terminates TLS for the YARN RM HA upstream — adds one more upstream block per protected UI.
  - [ ] Install `oauth2-proxy` (binary release from upstream)⁸
  - [ ] Configure oauth2-proxy with Okta provider:
    - [ ] `--provider=oidc`
    - [ ] `--oidc-issuer-url=https://<fqdn-tenant>.okta.com`
    - [ ] `--client-id`, `--client-secret` from O0.1 `spark-ui-gateway` app
    - [ ] `--redirect-url=https://<gateway-host>/oauth2/callback` (matches O0.1 redirect URI)
    - [ ] `--email-domain=*` and `--allowed-groups=fqdn-spark-admin,fqdn-spark-developer,fqdn-spark-analyst,fqdn-spark-oncall`
    - [ ] `--reverse-proxy=true` and `--trusted-proxy-ip=<nginx-front-ip>`⁸
    - [ ] `--pass-access-token=true`, `--set-xauthrequest=true` so upstream can read identity headers
  - [ ] Configure Nginx upstream blocks for:
    - [ ] Spark History Server: `https://<gateway>/history/` → `http://<node02>:18080/`
    - [ ] YARN RM (active/standby via existing P1.4 upstream): `https://<gateway>/yarn/` → `http://<yarn-rm-active>:8088/`
    - [ ] Per-app Spark UI proxied via YARN RM (RM auto-proxies app UIs at `/proxy/<application_id>/`)¹
  - [ ] Use oauth2-proxy's `auth_request` Nginx pattern⁸ so each upstream request validates the Okta cookie before being forwarded
  - [ ] Disable Hadoop SPNEGO on Spark History and YARN RM (set `hadoop.http.authentication.type=simple` on the gateway-fronted hostnames) — gateway is now the auth boundary; do **not** expose the upstream ports outside the cluster network
  - [ ] Add firewall rule: only the gateway VM IP may reach Spark History 18080 and YARN RM 8088 directly
- **Verification:**
  - [ ] Hitting `https://<gateway>/history/` while not signed in to Okta redirects through Okta and returns the History UI
  - [ ] Hitting `https://<gateway>/yarn/` works the same way
  - [ ] A user in only `fqdn-spark-analyst` is denied if Nginx route requires `fqdn-spark-admin`; user in admin group is allowed
  - [ ] Spark UI 4040 link from RM is reachable (via `/proxy/<app_id>/`) and inherits gateway auth
  - [ ] Direct unauthenticated request to `<node02>:18080` from outside the gateway IP is denied at the firewall
- **Owner:** Ksolves (gateway install + Nginx config) + fqdn (Okta credentials, firewall)
- **Estimated Effort:** 6–10 hours (install + multi-upstream config + firewall coordination + testing)
- **Citation Note:** The reverse-proxy pattern with header-injection is documented at oauth2-proxy's official site⁸ ("Some multi-user services support receiving the authenticated username/email from the reverse proxy passed in an HTTP header") and corroborated by Apache Knox's `KnoxSSO` description⁹ ("a normalized SSO token for representing the authenticated user ... applications participating in the KnoxSSO integration are able to cryptographically validate the presented token and remain agnostic to the underlying SSO integration").

<a id="o1-3-rgw"></a>

### 🟣 O1.3 — Ceph RGW OIDC Provider Registration + STS Trust Policies

- **Status:** PENDING O0.1, O0.4, P0.0 (Ceph cluster bootstrap)
- **Priority:** MEDIUM — Phase 1 critical path can run with static RGW keys initially; STS federation is a hardening step
- **Context:** Ceph Reef RGW supports the AWS-compatible STS API including `AssumeRoleWithWebIdentity`, allowing federated users to exchange an Okta-issued JWT for a short-lived AWS-style credential.³,¹⁰ Per Ceph official docs, "AssumeRoleWithWebIdentity returns a set of temporary credentials for an app/user that has been authenticated via an external IDP using OIDC."³ Setup requires: enable STS in `ceph.conf`, create the OIDC provider entity in RGW with Okta's URL and certificate thumbprints,¹³ create role(s) with trust policy referencing the provider, and grant role permissions over RGW buckets.
- **Prerequisites:**
  - [ ] P0.0 complete (Ceph cluster healthy, RGW endpoint live)
  - [ ] Okta `spark-rgw-sts` app from O0.1 with discovered Audience (`aud`) value
  - [ ] Admin user in RGW with `oidc-provider=*` capability¹³
- **Actions:**
  - [ ] Edit `ceph.conf` on all RGW hosts:
    - [ ] Set `rgw_sts_key = <16-hex-char>` — generate with `openssl rand -hex 16`; per Ceph docs all RGW instances in a zone must use **identical** keys, and "this setting is not runtime updatable"¹⁴
    - [ ] Set `rgw_s3_auth_use_sts = true` (runtime-updatable; defaults to `false`)¹⁴
  - [ ] Restart RGW daemons cluster-wide
  - [ ] Create RGW admin user with OIDC provider capability:
    ```
    radosgw-admin user create --uid=oidc-admin --display-name="OIDC Admin" --access-key=ADMIN_KEY --secret=ADMIN_SECRET
    radosgw-admin caps add --uid=oidc-admin --caps="oidc-provider=*"
    ```
    (Pattern from Ceph official OIDC docs.¹³)
  - [ ] Generate Okta IdP server certificate thumbprint (SHA-1 fingerprint of the leaf cert at `<fqdn-tenant>.okta.com:443`); store as `<thumbprint>`
  - [ ] Register Okta as OIDC provider via the IAM API (using awscli configured against the RGW endpoint with `oidc-admin` keys):
    ```
    aws iam create-open-id-connect-provider \
        --url https://<fqdn-tenant>.okta.com \
        --thumbprint-list <thumbprint> \
        --client-id-list <okta-rgw-client-id> \
        --endpoint-url <rgw-endpoint>
    ```
    Per Ceph docs the API accepts up to 5 thumbprints and N client IDs.¹³
  - [ ] Create one or more IAM roles with trust policy referencing the provider, e.g., a role allowing `fqdn-spark-developer` group members to read/write the `output/parquet` prefix
  - [ ] Document the AssumeRoleWithWebIdentity flow for end-user clients (CLI: `aws sts assume-role-with-web-identity` with the Okta ID token, then use returned temp creds for S3 ops)
- **Verification:**
  - [ ] `radosgw-admin user list` shows `oidc-admin` and the provider entity is queryable via `aws iam list-open-id-connect-providers --endpoint-url <rgw-endpoint>`
  - [ ] A test user from `fqdn-spark-developer` can complete the AssumeRoleWithWebIdentity flow and list objects in the `output/parquet` bucket using returned temp creds
  - [ ] A test user **not** in any granted group is denied with `AccessDenied`
- **Owner:** Ksolves (ceph.conf + IAM API calls) + fqdn (Okta app credentials, group assignments)
- **Estimated Effort:** 4–6 hours
- **Citation Note:** The configuration parameters (`rgw_sts_key`, `rgw_s3_auth_use_sts`) and the AssumeRoleWithWebIdentity prerequisites are stated in Ceph's official STS documentation.¹⁴ The OIDC provider registration flow is documented in Ceph's official OIDC docs¹³ and corroborated by Ceph.io's 2025 blog on STS modernization,¹⁰ which gives the same end-to-end flow with a worked Keycloak example (the model is IdP-agnostic per the docs).

<a id="o1-4-asa"></a>

### 🟣 O1.4 — SSH/Bastion Access via Okta Advanced Server Access (ASA)

- **Status:** PENDING O0.4, P0.1 (Worker VMs), P0.2 (YARN RM VMs), P1.0 (Remote Airflow Host)
- **Priority:** MEDIUM — Static SSH keys remain functional in the interim; ASA hardens the human-SSH path
- **Context:** Per Okta's official architecture, ASA "secures administrator access for Linux and Windows servers ... with multifactor authentication (MFA), ephemeral certificates, and seamless client tool integration."⁴ ASA replaces static SSH keys with a Programmable CA that mints "single use, ephemeral credentials for every login ... each certificate linked to a user and a device logging into a server and expiring within three minutes."¹⁵ The cluster-side requirement is small: the ASA `sftd` daemon installed on each target host with the right enrollment token.
- **Prerequisites:**
  - [ ] All target VMs provisioned (P0.1, P0.2, P1.0, P1.1, Spark History Server)
  - [ ] ASA project provisioned in Okta tenant (one project per environment, e.g., `spark-dev`)
  - [ ] AD groups synced to Okta (O0.2) so ASA group memberships map to AD
- **Actions:**
  - [ ] In Okta admin → Advanced Server Access, create project `spark-dev` (or per-env naming)
  - [ ] Define ASA groups within the project — typically `spark-dev-admin`, `spark-dev-oncall`, mapped to the corresponding fqdn AD/Okta groups from O0.3
  - [ ] On each cluster VM, install `sftd` (Okta-provided package; supports RHEL 9):
    ```
    curl -fsSL https://dist.scaleft.com/repos/rpm/stable/scaleft-yum-stable.rpm -o /tmp/scaleft-yum-stable.rpm
    rpm -i /tmp/scaleft-yum-stable.rpm
    yum install scaleft-server-tools
    sftd enroll --token <project-enrollment-token>
    systemctl enable --now sftd
    ```
  - [ ] Configure sshd to trust the ASA CA: append `TrustedUserCAKeys /var/lib/sftd/trusted_ca` to `/etc/ssh/sshd_config` and `systemctl reload sshd` (matches the model described in Okta's "Best Practices: Enforcing Least Privilege Access for Linux Servers"¹⁶)
  - [ ] Distribute `sft` client to fqdn engineering laptops; engineers run `sft enroll` once
  - [ ] Define server access policies in ASA: which groups have which sudo access on which host pools
  - [ ] Decide static-key retirement plan: keep one break-glass static key in vault per host for ASA-outage scenarios; remove all other authorized_keys entries after a stability window
- **Verification:**
  - [ ] `sft ssh <hostname>` from an enrolled client connects successfully with `auth: certificate` in the sshd log
  - [ ] Static-key login is denied for non-break-glass users
  - [ ] An ASA audit log entry appears in Okta for every session (Okta documents that "every connection ... is end-to-end encrypted, mutually authenticated, and authorized with ephemeral client certificates"¹⁵)
- **Owner:** fqdn IT (ASA project) + Ksolves (sftd install per VM) + fqdn engineers (client enrollment)
- **Estimated Effort:** 6–8 hours (project setup + ~6 VM installs + client distribution)
- **Citation Note:** ASA's ephemeral-cert model is documented by Okta in two distinct sources: the ASA Help Center setup guide⁴ ("Set Up SSH with Advanced Server Access") and the Okta whitepaper "Best Practices: Enforcing Least Privilege Access for Linux Servers."¹⁶ Both describe the same TrustedUserCAKeys + sftd architecture.

<a id="o1-5-snowflake"></a>

### 🟣 O1.5 — Snowflake SAML Federation with Okta

- **Status:** PENDING O0.1, P0.3 (cloud staging decision)
- **Priority:** MEDIUM — Federation hardens the Snowflake login path; Phase 1 P2.3 can validate end-to-end pipeline with non-federated keypair auth in the interim
- **Context:** Snowflake supports SAML 2.0 federation as a first-class feature, and Okta ships a pre-built Snowflake SAML app integration.⁵,¹⁷ The Snowflake-side config lives in a `SECURITY INTEGRATION` of type SAML2; the Okta-side config is the pre-built Snowflake app with the Snowflake account URL filled in.
- **Prerequisites:**
  - [ ] Snowflake account exists (fqdn responsibility per Phase 1 P2.3 Snowflake Scope Note)
  - [ ] Okta `spark-snowflake` SAML SP app from O0.1
  - [ ] `fqdn-snowflake-loader` group from O0.3 assigned to the app
  - [ ] Snowflake admin (ACCOUNTADMIN) able to run `CREATE SECURITY INTEGRATION`
- **Actions:**
  - [ ] In Okta → Applications → Snowflake (pre-built), set the Snowflake account URL (e.g., `https://<account>.snowflakecomputing.com`) and the Snowflake username attribute (typically `email` mapping to Snowflake `LOGIN_NAME`)⁵
  - [ ] Capture Okta IdP metadata (sign-on URL, X.509 cert)
  - [ ] In Snowflake, run:
    ```sql
    CREATE SECURITY INTEGRATION OKTA_SSO
      TYPE = SAML2
      ENABLED = TRUE
      SAML2_ISSUER = '<okta-issuer>'
      SAML2_SSO_URL = '<okta-sso-url>'
      SAML2_PROVIDER = 'OKTA'
      SAML2_X509_CERT = '<base64-cert>'
      SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = 'Okta'
      SAML2_ENABLE_SP_INITIATED = TRUE
      SAML2_FORCE_AUTHN = FALSE;
    ```
    (Pattern from Snowflake's `CREATE SECURITY INTEGRATION (SAML2)` reference¹⁸)
  - [ ] Test SP-initiated login: visit Snowflake URL, click "Sign in with Okta," confirm AD-credentials → Okta → Snowflake works
  - [ ] Test IdP-initiated login: from Okta dashboard, click Snowflake tile, confirm landing in Snowflake without re-prompt
  - [ ] Decide whether to enforce SSO-only (set `LOGIN_TYPE = NULL` or restrict native logins) once verified; recommend keeping one break-glass ACCOUNTADMIN with keypair auth
- **Verification:** `fqdn-snowflake-loader` member can authenticate to Snowflake via Okta; non-member is denied at Okta; SAML response in Okta log contains correct `NameID` and group claims.
- **Owner:** fqdn (Snowflake admin) + fqdn IT (Okta admin); not a Ksolves task
- **Estimated Effort:** 2–4 hours
- **Citation Note:** The SAML2 security integration syntax is documented in Snowflake's official SQL reference¹⁸ and the end-to-end Okta-as-IdP flow is documented in both Snowflake's federated-auth user guide¹⁷ and Okta's pre-built Snowflake SAML configuration guide.⁵

---

<a id="cp-o2-validation"></a>

## Critical Path — O2: Validation & Cutover

<a id="o2-1-smoke-test"></a>

### 🟣 O2.1 — End-to-End SSO Smoke Test

- **Status:** PENDING O1.1–O1.5
- **Priority:** HIGH — Required gate before declaring Okta integration production-ready
- **Actions:**
  - [ ] One test user per group (`fqdn-spark-admin`, `fqdn-spark-developer`, `fqdn-spark-analyst`, `fqdn-spark-oncall`, `fqdn-snowflake-loader`)
  - [ ] For each user: log in to Airflow, Spark History via gateway, YARN RM via gateway, run `aws sts assume-role-with-web-identity`, SSH via `sft`, log in to Snowflake — confirm allowed/denied per group
  - [ ] Document any deviation between expected and actual access; reconcile against group mapping matrix
- **Verification:** Access matrix matches design exactly for all five test users
- **Owner:** fqdn data-platform lead + Ksolves (cluster-side support)
- **Estimated Effort:** 2–3 hours

<a id="o2-2-mapping-audit"></a>

### 🟣 O2.2 — Group / Role Mapping Audit

- **Status:** PENDING O2.1
- **Priority:** HIGH
- **Actions:**
  - [ ] Generate the access matrix (groups × services × permissions) from live Okta + service configs
  - [ ] Compare against the matrix defined in O0.3 / O1.x
  - [ ] Resolve drift; document final matrix in security context as the canonical reference
- **Verification:** Reviewed and signed off by fqdn Cyber Security
- **Owner:** fqdn data-platform lead + fqdn Cyber Security
- **Estimated Effort:** 1–2 hours

<a id="o2-3-offboarding"></a>

### 🟣 O2.3 — Offboarding & Revocation Drill

- **Status:** PENDING O2.1
- **Priority:** HIGH
- **Context:** A failed revocation is a compliance finding. Test the offboarding path before production use.
- **Actions:**
  - [ ] Pick a test user; remove from AD group `fqdn-spark-developer`
  - [ ] Within sync window (Okta default 1h, force a sync to verify), confirm the user can no longer:
    - [ ] Log in to Airflow (FAB role downgraded or session terminated at next request)
    - [ ] Authenticate to gateway (Okta denies token issuance)
    - [ ] Assume RGW STS role (token issuance denied or trust policy fails)
    - [ ] SSH via ASA (server access policy revoked)
    - [ ] Log in to Snowflake (Okta SAML denies)
  - [ ] Document any service where revocation lags > 1 hour and decide if that's acceptable
- **Verification:** Access matrix transitions correctly within agreed sync window
- **Owner:** fqdn Cyber Security + fqdn data-platform lead
- **Estimated Effort:** 2 hours

<a id="o2-4-asbuilt"></a>

### 🟣 O2.4 — As-Built Documentation & Compliance Citations

- **Status:** PENDING O2.1, O2.2, O2.3
- **Priority:** MEDIUM
- **Actions:**
  - [ ] Update `security/Document/` with: auth architecture diagram, service-by-service runbook, group→role matrix, revocation procedure
  - [ ] Update Phase 1 as-built (`P3.2`) to reflect Okta integration
  - [ ] Replace any Keycloak references in security documents with Okta + the citations from this document's bibliography
- **Verification:** All target documents updated and reviewed; promoted from `Ready_For_Review/` to `Document/` per project convention
- **Owner:** fqdn data-platform lead
- **Estimated Effort:** 3–5 hours

---

<a id="group-role-matrix"></a>

## Group / Role Mapping Matrix

| AD/Okta group | Airflow FAB role | Gateway access | RGW STS role | ASA server access | Snowflake role |
|---|---|---|---|---|---|
| `fqdn-spark-admin` | `Admin` | All UIs (admin) | `spark-admin` (full S3) | All hosts, sudo | `SYSADMIN` |
| `fqdn-spark-developer` | `User` | All UIs (read+submit) | `spark-developer` (RW own prefix) | Worker VMs, no sudo | `DEVELOPER` (custom) |
| `fqdn-spark-analyst` | `Viewer` | History, YARN RM (read) | `spark-analyst` (RO output) | None | `ANALYST` (custom) |
| `fqdn-spark-oncall` | `Viewer` | YARN RM (read) | None | All hosts, sudo (MFA-required) | None |
| `fqdn-snowflake-loader` | None | None | None | None | `ETL_LOADER` (custom) |

This matrix is a starting point; finalize in O2.2 audit.

---

<a id="network-egress"></a>

## Network Egress Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Remote Airflow Host (MSB-PMC01) | `<tenant>.okta.com` | 443 | Airflow OIDC redirect, JWKS |
| SSO Gateway VM | `<tenant>.okta.com` | 443 | Gateway OIDC + JWKS |
| All cluster VMs (MSB-PMC03) | `gateway.<region>.sft.okta.com` | 443 | ASA control plane⁴ |
| All cluster VMs | `<tenant>.okta.com` | 443 | OIDC discovery, JWKS for cert validation |
| All RGW hosts | `<tenant>.okta.com` | 443 | JWKS for STS WebIdentity verification |
| Snowflake-connected hosts | `*.snowflakecomputing.com` | 443 | Snowflake federated login redirect |
| Browser clients | `<tenant>.okta.com` | 443 | All redirect-based flows |
| Browser clients | Each protected service hostname | 443 | Service access |

---

<a id="open-questions"></a>

## Open Questions for fqdn Cyber Security

These must be resolved before O0/O1 work can be sequenced into the Phase 1 plan.

- [ ] Is Okta ASA approved for cluster SSH, or must SSH continue with static keys + AD/SSSD?
- [ ] Is delegated authentication to AD acceptable, or does corp policy require Okta-native passwords (would change O0.2 scope)?
- [ ] Is there an existing fqdn Okta gateway/proxy pattern to follow, or is the Phase 1 cluster the first Hadoop-style workload to integrate?
- [ ] What is the corp standard for OIDC redirect URI domain (do all redirect URIs need to be on a fqdn-owned domain)?
- [ ] What is the corp policy on token lifetimes (access/ID/refresh), MFA-on-step-up, and idle-session timeout?
- [ ] Should ASA enrollment require device posture checks (managed device only)?
- [ ] Does fqdn already have a Snowflake↔Okta SAML integration in another business unit that should be reused?
- [ ] Is Apache Knox a corp-blessed gateway, or does Cyber Security prefer oauth2-proxy or another solution?

---

<a id="cross-references"></a>

## Cross-References to Phase 1 TODO

The following items in `Phases_Critical_Path_Development_v1.5.md` need updates once this document is approved:

- **P1.0 Step 4** ("Install Okta SSO integration") — replace with reference to `O1.1` for concrete implementation steps
- **P1.0 Step 8** ("Provide Okta OIDC credentials for Airflow SSO configuration") — replace with reference to `O0.1` (app registration as the source of those credentials) and `O1.1` (where they are consumed)
- **P2.2 Step 7** ("Set up Airflow web UI ... with basic auth or Okta integration") — replace ambiguity with explicit reference to `O1.1`
- **Add new tasks** at appropriate points in Phase 1: `O0.1`–`O0.5` belong in Phase 2A (foundation, before P1.0); `O1.1`–`O1.5` belong in Phase 2B/2C alongside their service dependencies; `O2.1`–`O2.4` belong in Phase 2C as a parallel validation track
- **Update group/role mapping matrix** in `Phases_Critical_Path_Development_v1.5.md` § Assumptions if/when this document's matrix is approved
- **Update Bibliography** in `Phases_Critical_Path_Development_v1.5.md` to incorporate the citations below if Okta integration is folded into the main document

---

<a id="assumptions"></a>

## Assumptions & Dependencies

**Assumptions:**

- fqdn Okta tenant is the existing enterprise tenant (not a new Phase 1-specific tenant)
- AD remains the authoritative source for user lifecycle (joiner/mover/leaver) — Okta does not replace AD
- Engineers performing setup have admin rights in Okta and AD
- Phase 1 cluster has outbound HTTPS connectivity to Okta endpoints (verified in O0.4)
- Reverse-proxy gateway can co-locate with the existing P1.4 Nginx VM, or stand alone — both are viable

**Dependencies on Phase 1 plan:**

- O0.4 depends on Phase 1 P0.7 (cluster network connectivity verified) — same network team owns both
- O1.1 depends on P1.0 (Remote Airflow Host) and P2.2 (Airflow installed)
- O1.2 depends on P0.0 (Ceph), P1.1 (Spark History Server), P1.2 (YARN RM HA), P1.4 (Nginx)
- O1.3 depends on P0.0 (Ceph cluster bootstrap)
- O1.4 depends on P0.1, P0.2, P1.0, P1.1 (all VMs that need ASA)
- O1.5 has no Ksolves dependency — fqdn-only

---

<a id="reference-documents"></a>

## Reference Documents

- `Phases_Critical_Path_Development_v1.5.md` — Phase 1 critical path that this document augments
- `CP_HIPAA_Compliance_v1.0.md` — HIPAA encryption + Web UI ACL sub-project (companion to this document; owns inter-daemon Kerberos + RPC encryption, while this document owns user-facing Okta SSO)
- `Ksolves_Spark_YARN_Config_v1.0.pdf` — vendor configuration baseline; § 8 is the source for the HIPAA workstream that the cross-reference above points to
- `security/Notes/okta-migration-plan.md` — earlier scaffold from which this document expands
- `security/Notes/keycloak-implementation-plan.md` — superseded by Okta decision (kept for historical reference)
- `security/Notes/questions_for_vendors.txt` — vendor-side open questions on auth

---

<a id="footnotes"></a>

## Footnotes

¹ Apache Software Foundation, "YARN Application Security," in *Apache Hadoop 3.4.1 Documentation*, accessed April 26, 2026, https://hadoop.apache.org/docs/r3.4.1/hadoop-yarn/hadoop-yarn-site/YarnApplicationSecurity.html.

² Apache Software Foundation, "FAB Auth Manager: Webserver Authentication," in *Apache Airflow Providers FAB Documentation*, accessed April 26, 2026, https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/webserver-authentication.html.

³ Ceph Project, "STS in Ceph," in *Ceph Documentation*, accessed April 26, 2026, https://docs.ceph.com/en/latest/radosgw/STS/.

⁴ Okta, "Set Up SSH with Advanced Server Access," in *Okta Advanced Server Access Help Center*, accessed April 26, 2026, https://help.okta.com/asa/en-us/content/topics/adv_server_access/docs/setup/ssh.

⁵ Okta, "Configuring SAML for Snowflake with Okta — Setup SSO," in *Okta SAML Documentation*, accessed April 26, 2026, https://saml-doc.okta.com/SAML_Docs/How-to-Configure-SAML-2.0-for-Snowflake.html.

⁶ Okta, "Active Directory Password Sync and Delegated Authentication," in *Okta Help Center*, accessed April 26, 2026, https://support.okta.com/help/s/article/Active-Directory-Password-Sync-and-Delegated-Authentication.

⁷ Okta, "Okta Directory Integration — An Architecture Overview," whitepaper, accessed April 26, 2026, https://www.okta.com/resources/whitepaper/ad-architecture/.

⁸ OAuth2 Proxy Project, "OAuth2 Proxy Documentation," accessed April 26, 2026, https://oauth2-proxy.github.io/oauth2-proxy/.

⁹ Apache Software Foundation, "Apache Knox 2.1.0 User's Guide," accessed April 26, 2026, https://knox.apache.org/books/knox-2-1-0/user-guide.html.

¹⁰ Ceph Project, "Breaking the Static Key Habit: Modernizing Ceph RGW S3 Security with STS," *Ceph Blog*, 2025, accessed April 26, 2026, https://ceph.io/en/news/blog/2025/rgw-modernizing-sts/.

¹¹ Or Sagiv, "Airflow with Okta: A Step-by-Step Integration," *Riskified Tech (Medium)*, accessed April 26, 2026, https://medium.com/riskified-technology/airflow-with-okta-a-step-by-step-integration-3a3d87081445.

¹² Scribd Engineering, "Integrating Airflow with Okta," *Scribd Tech Blog*, 2021, accessed April 26, 2026, https://tech.scribd.com/blog/2021/integrating-airflow-and-okta.html.

¹³ Ceph Project, "OpenID Connect Provider in RGW," in *Ceph Documentation*, accessed April 26, 2026, https://docs.ceph.com/en/latest/radosgw/oidc/.

¹⁴ Ceph Project, "STS — Configuration Parameters," in *Ceph Documentation*, accessed April 26, 2026, https://docs.ceph.com/en/latest/radosgw/STS/#parameters.

¹⁵ Okta, "SSH is Dead. Long Live SSH: One Million SSH Logins with Okta. Zero SSH Keys.," *Okta Blog*, 2020, accessed April 26, 2026, https://www.okta.com/blog/2020/07/ssh-is-dead-long-live-ssh-one-million-ssh-logins-with-okta-zero-ssh-keys/.

¹⁶ Okta, "Best Practices: Enforcing Least Privilege Access for Linux Servers With Okta," whitepaper, accessed April 26, 2026, https://www.okta.com/resources/whitepaper/best-practices-enforcing-least-privilege-access-for-linux-servers-with-okta/.

¹⁷ Snowflake Inc., "Overview of Federated Authentication and SSO," in *Snowflake Documentation*, accessed April 26, 2026, https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview.

¹⁸ Snowflake Inc., "CREATE SECURITY INTEGRATION (SAML2)," in *Snowflake SQL Reference*, accessed April 26, 2026, https://docs.snowflake.com/en/sql-reference/sql/create-security-integration-saml2.

---

<a id="bibliography"></a>

## Bibliography

Apache Software Foundation. "Apache Knox 2.1.0 User's Guide." Accessed April 26, 2026. https://knox.apache.org/books/knox-2-1-0/user-guide.html.

Apache Software Foundation. "FAB Auth Manager: Webserver Authentication." In *Apache Airflow Providers FAB Documentation*. Accessed April 26, 2026. https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/webserver-authentication.html.

Apache Software Foundation. "Single Sign-On (SSO) Integration." In *Apache Airflow Providers FAB Documentation*. Accessed April 26, 2026. https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/sso.html.

Apache Software Foundation. "YARN Application Security." In *Apache Hadoop 3.4.1 Documentation*. Accessed April 26, 2026. https://hadoop.apache.org/docs/r3.4.1/hadoop-yarn/hadoop-yarn-site/YarnApplicationSecurity.html.

Ceph Project. "Breaking the Static Key Habit: Modernizing Ceph RGW S3 Security with STS." *Ceph Blog*, 2025. Accessed April 26, 2026. https://ceph.io/en/news/blog/2025/rgw-modernizing-sts/.

Ceph Project. "OpenID Connect Provider in RGW." In *Ceph Documentation*. Accessed April 26, 2026. https://docs.ceph.com/en/latest/radosgw/oidc/.

Ceph Project. "STS in Ceph." In *Ceph Documentation*. Accessed April 26, 2026. https://docs.ceph.com/en/latest/radosgw/STS/.

OAuth2 Proxy Project. "OAuth2 Proxy Documentation." Accessed April 26, 2026. https://oauth2-proxy.github.io/oauth2-proxy/.

Okta. "Active Directory Password Sync and Delegated Authentication." In *Okta Help Center*. Accessed April 26, 2026. https://support.okta.com/help/s/article/Active-Directory-Password-Sync-and-Delegated-Authentication.

Okta. "Best Practices: Enforcing Least Privilege Access for Linux Servers With Okta." Whitepaper. Accessed April 26, 2026. https://www.okta.com/resources/whitepaper/best-practices-enforcing-least-privilege-access-for-linux-servers-with-okta/.

Okta. "Configuring SAML for Snowflake with Okta — Setup SSO." In *Okta SAML Documentation*. Accessed April 26, 2026. https://saml-doc.okta.com/SAML_Docs/How-to-Configure-SAML-2.0-for-Snowflake.html.

Okta. "Okta Directory Integration — An Architecture Overview." Whitepaper. Accessed April 26, 2026. https://www.okta.com/resources/whitepaper/ad-architecture/.

Okta. "Set Up SSH with Advanced Server Access." In *Okta Advanced Server Access Help Center*. Accessed April 26, 2026. https://help.okta.com/asa/en-us/content/topics/adv_server_access/docs/setup/ssh.

Okta. "SSH is Dead. Long Live SSH: One Million SSH Logins with Okta. Zero SSH Keys." *Okta Blog*, 2020. Accessed April 26, 2026. https://www.okta.com/blog/2020/07/ssh-is-dead-long-live-ssh-one-million-ssh-logins-with-okta-zero-ssh-keys/.

Sagiv, Or. "Airflow with Okta: A Step-by-Step Integration." *Riskified Tech (Medium)*. Accessed April 26, 2026. https://medium.com/riskified-technology/airflow-with-okta-a-step-by-step-integration-3a3d87081445.

Scribd Engineering. "Integrating Airflow with Okta." *Scribd Tech Blog*, 2021. Accessed April 26, 2026. https://tech.scribd.com/blog/2021/integrating-airflow-and-okta.html.

Snowflake Inc. "CREATE SECURITY INTEGRATION (SAML2)." In *Snowflake SQL Reference*. Accessed April 26, 2026. https://docs.snowflake.com/en/sql-reference/sql/create-security-integration-saml2.

Snowflake Inc. "Overview of Federated Authentication and SSO." In *Snowflake Documentation*. Accessed April 26, 2026. https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-overview.

---

_End of CP_Okta_v1.0.md_
