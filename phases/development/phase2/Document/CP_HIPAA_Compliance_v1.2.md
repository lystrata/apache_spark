# Critical Path — HIPAA Compliance (Spark / YARN / Ceph)

_Version 1.2 · Last updated 2026-05-13_
_Source: Ksolves Spark & YARN Configuration Best Practices v1.0 (2026-05-04) § 8 — `phases/development/phase2/Document/Ksolves_Spark_YARN_Config_v1.0.pdf`_
_Status: Active — Phase 3 scope for software/network HIPAA compliance (BLOCKER.3b); Phase 2 hardware compliance (BLOCKER.3a) closed 2026-05-11; **#H1 javax filter DROPPED from SOW 2026-05-13** — replaced by Kerberos + AD logins (#H1-rev)_

> **v1.2 Update (2026-05-13) — javax servlet filter dropped from SOW; Kerberos + AD logins replaces it:**
>
> Joint fqdn–Ksolves meeting 2026-05-13 dropped the custom javax servlet filter requirement (vendor doc § 8.3) from the scope of work with fqdn concurrence. Web UI and History Server access control will be enforced via **Kerberos + AD logins** instead — both Spark service authentication (already in #H4) and Web UI user authentication share the same Kerberos/AD identity layer.
>
> **Impact on this document:**
> - **#H1 (custom javax servlet filter)** — **CLOSED 2026-05-13 (DROPPED FROM SOW)**. No fqdn-side development work required. The historic actions list is preserved below the closure note for audit trail.
> - **#H1-rev (Kerberos + AD logins on Spark Web UI / History Server)** — **NEW item replacing #H1.** Configure Spark's built-in SPNEGO/Kerberos UI filter (`org.apache.hadoop.security.authentication.server.AuthenticationFilter`) bound to the fqdn Kerberos realm; AD groups govern admin/non-admin ACLs via `spark.admin.acls.groups`. No fqdn-developed Java code.
> - **#H2 (auth integration target decision)** — **RESOLVED 2026-05-13 (KERBEROS + AD)**. Decision recorded; carried as historic context.
> - **#H4 (Kerberos realm + service principal + keytab)** — unchanged in name, but now **doubles as the Web UI auth backbone** (was just service auth in v1.1). Priority reaffirmed HIGH; scope expands to also cover the SPNEGO/Web UI flow.
> - **§ 8.3 Web UI ACL pillar framing** — replace "custom javax servlet filter" everywhere with "Kerberos + AD logins (Spark SPNEGO filter)".
>
> **Why the change is acceptable:** Spark's built-in SPNEGO filter satisfies the same § 8.3 requirement (authenticated access before ACL enforcement) without bespoke code. The Kerberos realm and AD identities required for #H4 service auth are the same identities used for Web UI auth — operationally one identity layer, not two. Removes a fqdn Development team deliverable; net schedule benefit aligns with the Phase 3 May-20 target.
>
> ---
>
> **v1.1 Update (2026-05-11) — HIPAA scope split between Phase 2 and Phase 3:** Per joint fqdn–Ksolves decision 2026-05-11, the HIPAA encryption + access-control posture splits across phase boundaries:
>
> - **Phase 2 — HIPAA Hardware Compliance (BLOCKER.3a) — CLOSED 2026-05-11.** Drive encryption / LUKS posture on NVMe scratch drives sde–sdh. <vendor-engineer> ran ansible reformat across all 3 dev cluster nodes today, removing the software LUKS layer that had been double-layered on top of the existing hardware encryption. Final posture: hardware-only encryption on scratch drives; OSD drives (sda/sdc/sdd) remain dm-crypt as expected. Confirmed via the 2026-05-11 18:42 audit log at `phases/development/phase2/Incoming/ceph_audit_msb-pmc03-01.corp.fqdn_2026-05-11_1842.log` showing sde–sdh bare-mounted at `/data/spark-scratch/drive[0-3]` with no dm-crypt mapping.
> - **Phase 3 — HIPAA Software & Network Compliance (BLOCKER.3b) — Active, scope of this document.** Transmission security (§ 8.1), Web UI ACL (§ 8.3), SSE on Ceph buckets (§ 8.2 object-storage portion), local Spark I/O encryption, Kerberos service auth. All Active Items (#H1, #H2, #H4, #H5) plus Vendor-Owned Verification Items (V1–V6) are Phase 3 scope. This document is the canonical tracker for BLOCKER.3b going forward; main CP v1.5 carries a one-line pointer here.
>
> The vendor's three-pillar § 8 framing maps to this split:
> - § 8.1 transmission security → Phase 3
> - § 8.2 data at rest → **Phase 2 (LUKS) closed**; Phase 3 portion (SSE on Ceph buckets, local Spark I/O encryption) remains active
> - § 8.3 Web UI ACL → Phase 3
>
> **v1.5 Sync notes (preserved from v1.0, 2026-05-08):** Two adjacent gates in main CP worth noting:
> - **BLOCKER.4 (NEW 2026-05-06)** — Phase 1B vendor-access isolation gate. HIPAA compliance work that requires vendor execution is sequenced behind BLOCKER.4 closure when delivered via permanent VDI. Vendor Isolation Framework v0.2 circulated 2026-05-11; awaiting Network / Cyber / CIO / AD-admin responses.
> - **P2.9 (NEW 2026-05-07)** — Centralized Audit Logging + Retention Policy (HIPAA-driven, 6-year floor per § 164.316(b)(2)). Currently in main CP; may move into this sub-project during the next HIPAA revision pass once a clear "audit / retention" pillar is added below the existing three.

---

## Document Overview

Sub-project critical path for the **HIPAA encryption and access-control posture** required for the Spark / YARN / Ceph stack to handle ePHI (electronic protected health information) data. Forked out of the main Phase 2 critical path (`Phases_Critical_Path_Development_v1.6.md`) on 2026-05-05 because the scope is large, cross-team, and partly vendor-owned, so it merits its own tracker.

**Companion to — does not duplicate:**
- `Phases_Critical_Path_Development_v1.6.md` — main Phase 2 CP. Carries a BLOCKER pointing here.
- `Ksolves_Spark_YARN_Config_v1.0.pdf` — vendor's authoritative configuration baseline (the source spec for everything below).

### Scope

The vendor's § 8 enumerates three pillars:

1. **Transmission security** (data in transit) — TLS for S3A, authenticated + encrypted internal Spark RPC, SSL on Web UIs (HIPAA Reference: 45 CFR § 164.312(e)(1))
2. **Data at rest encryption** — local Spark I/O encryption, LUKS at the OS level on NVMe drives, SSE on Ceph object buckets (HIPAA Reference: 45 CFR § 164.312(a)(2)(iv))
3. **Web UI access control** — Spark UI / History Server ACLs via custom **javax servlet filter**

The first two are mostly vendor-owned (during Spark install) plus one fqdn-owned task that's **already done** (LUKS). The third pillar requires fqdn-side development of a custom auth filter — Spark does not provide a built-in one.

### Methodology

Each item is tagged with **owner** (fqdn / Vendor / Done) and traces back to a specific § 8 sub-section and parameter table. Verification steps are listed where applicable.

---

## Active Items — fqdn-side

<a id="hipaa-1"></a>

### #H1 — Custom javax servlet auth filter for Spark Web UI / History Server — **CLOSED 2026-05-13 (DROPPED FROM SOW)**

- **Status:** **CLOSED 2026-05-13 — DROPPED FROM SOW** (joint fqdn–Ksolves meeting; fqdn concurrence). Replaced by **#H1-rev** (Kerberos + AD logins via Spark's built-in SPNEGO filter — no fqdn-developed Java code required).
- **Priority:** (historic) HIGH — gates Web UI exposure of any ePHI metadata. Now carried by #H1-rev.
- **Owner:** (historic) fqdn Development team. With the drop, no Dev-team deliverable here.
- **Closure rationale:** Spark's built-in SPNEGO/Kerberos UI filter satisfies the § 8.3 "authenticated access before ACL enforcement" requirement without bespoke code. Since #H4 (Kerberos service principal) already establishes the realm, Web UI auth shares that same identity backbone — one identity layer, not two.

**Historic context (preserved for audit trail):** Spark's Web UI and History Server display job metadata and stack traces. HIPAA requires authenticated access. Spark does not provide a built-in *application-layer* auth filter for arbitrary identity providers — `spark.acls.enable=true` only enforces ACLs *after* the user is identified. The vendor's original § 8.3 spec called for a custom `javax servlet filter` integrating with fqdn's auth IdP (LDAP / Okta / etc.). The 2026-05-13 SOW change observes that Spark **does** ship a SPNEGO/Kerberos servlet filter (`org.apache.hadoop.security.authentication.server.AuthenticationFilter`) that handles the identification step against any KRB5 realm — including the realm being set up for #H4. That covers the requirement without the bespoke filter.

**Original fqdn actions (NO LONGER REQUIRED — preserved for audit trail):**
- _[Dropped 2026-05-13]_ Decide auth integration target — resolved to **Kerberos + AD** (closes #H2).
- _[Dropped 2026-05-13]_ Develop the javax servlet filter (Java/Scala) — no longer needed.
- _[Dropped 2026-05-13]_ Package as a JAR; deploy to Spark classpath via Ansible — no longer needed.
- _[Dropped 2026-05-13]_ Configure `spark.ui.filters = <fully.qualified.ClassName>` — replaced by the Hadoop SPNEGO filter config in #H1-rev.

**Reference:** vendor doc § 8.3 (now superseded for fqdn implementation) + 2026-05-13 joint meeting decision + [https://downloads.apache.org/spark/docs/3.5.3/security.html](https://downloads.apache.org/spark/docs/3.5.3/security.html) (SPNEGO section).

---

<a id="hipaa-1-rev"></a>

### #H1-rev — Kerberos + AD logins on Spark Web UI / History Server (replaces #H1) — **NEW 2026-05-13**

- **Status:** TO DO (Phase 3 scope; activates once #H4 Kerberos realm is up)
- **Priority:** HIGH (gates Web UI exposure of any ePHI metadata)
- **Owner:** **fqdn Cybersecurity / IT + Vendor (Ksolves)** — vendor configures the filter at Spark install; fqdn supplies the realm and verifies
- **Depends on:** #H4 (Kerberos realm + service principal + keytab) — the same realm authenticates Spark services *and* Web UI users
- **Triggers / informs:** Web UI go-live; AD-group-driven ACLs replace the planned `spark.admin.acls=<user-list>` enumeration
- **Source:** Vendor doc § 8.3 (revised) + 2026-05-13 joint SOW change

The Hadoop SPNEGO/Kerberos authentication filter (`org.apache.hadoop.security.authentication.server.AuthenticationFilter`, type=`kerberos`) ships with Spark's bundled Hadoop classpath. Pointing `spark.ui.filters` at it makes Spark's Web UI and History Server require a valid Kerberos ticket; users authenticate via their AD-issued ticket (the same `kinit` flow used for Spark service auth in #H4). AD group membership feeds Spark ACLs via `spark.admin.acls.groups` / `spark.modify.acls.groups`, eliminating the per-user enumeration that the original #H1 plan implied.

**fqdn actions:**
- [ ] Confirm Spark UI Kerberos principal naming convention with vendor (typically `HTTP/<host>@<REALM>`)
- [ ] Generate Web UI principals + keytabs for each Worker VM + YARN RM + History Server VM (extends #H4 keytab work to add the HTTP service principal)
- [ ] Provide vendor: `spark.ui.filters`, `spark.<filter>.param.type=kerberos`, `spark.<filter>.param.kerberos.principal`, `spark.<filter>.param.kerberos.keytab` config snippets
- [ ] Define AD groups for `spark-admins` (full ACL) and `spark-users` (modify ACL) — coordinate with Michelle for AD provisioning
- [ ] Configure `spark.acls.enable=true`, `spark.history.ui.acls.enable=true`, `spark.admin.acls.groups=spark-admins`, `spark.modify.acls.groups=spark-users`
- [ ] Configure HSTS / XSS / no-sniff response headers per vendor § 8.3 table (vendor applies at install)
- [ ] Verification: open Spark UI / History Server with a non-`spark-admins` AD user, confirm 401 without ticket, confirm 403 on admin endpoints with valid ticket but non-admin group membership

**Why this works:** Kerberos identifies the user; AD group membership authorizes them; Spark's ACL layer enforces the role boundary. No fqdn-developed Java code; all configuration-only.

**Reference:** Hadoop `AuthenticationFilter` documentation + Spark `spark.acls.*` + 2026-05-13 joint meeting decision.

---

<a id="hipaa-2"></a>

### #H2 — Decide auth integration target for the servlet filter — **RESOLVED 2026-05-13 (Kerberos + AD)**

- **Status:** **RESOLVED 2026-05-13** — decision: **Kerberos + AD** (Spark's built-in SPNEGO filter, no custom code). Carried in #H1-rev above.
- **Priority:** (historic) HIGH — was prerequisite for #H1 design. Decision landed at the same 2026-05-13 meeting that dropped #H1.
- **Owner:** (resolved) fqdn Cybersecurity (Paul) + fqdn Development + Vendor (Ksolves)
- **Source:** 2026-05-13 joint meeting

**Historic context:** Pre-decision before the original #H1 development could begin asked whether the Spark Web UI auth filter would integrate with **Okta** (matches CP_Okta posture for Airflow/SHS), **LDAP** (corp standard), **Kerberos** (the same realm being set up for Spark service auth in #H4), or something else. Each path had development implications.

**Decision (2026-05-13):** **Kerberos + AD logins.** Rationale: Spark's bundled Hadoop SPNEGO filter satisfies the § 8.3 requirement against a Kerberos realm without custom Java code; #H4 already establishes that realm for service auth; AD groups authorize via `spark.admin.acls.groups`. One identity layer covers Spark service auth (#H4) and Web UI auth (#H1-rev).

**Implication for the broader auth landscape:** The Spark Web UI auth path diverges from the Airflow / SHS Okta-OIDC path in `CP_Okta_v1.1.md` — Airflow keeps OIDC, Spark Web UIs use SPNEGO. The History Server is also a Spark UI and falls under SPNEGO. This is acceptable per the 2026-05-13 decision; the two auth backends serve different user populations (Airflow operators vs. Spark UI viewers/admins) and the operational duplication is small.

---

<a id="hipaa-3"></a>

### #H3 — Notify Ksolves: NVMe disks already LUKS-encrypted — **CLOSED 2026-05-11**

- **Status:** **CLOSED 2026-05-11** — closed via the joint resolution of the LUKS double-encryption issue (see Closed Items below). The notification was sent (verbal 2026-05-06; written follow-up `correspondence/Document/nvme_luks_already_encrypted_followup_to_ksolves_2026-05-08.md` sent 2026-05-08), but the vendor's install applied software LUKS anyway on top of the existing hardware encryption. Final state was resolved 2026-05-11 by <vendor-engineer>'s ansible reformat removing the software LUKS layer; scratch drives now hardware-only encryption.
- **Priority:** (historic) HIGH (avoid vendor reformatting our existing encryption)
- **Owner:** Wood, Rohn (notify) + <vendor-engineer> / Ksolves (reformat)
- **Final action:** ansible reformat across all 3 dev nodes 2026-05-11; bare-mounted scratch drives at `/data/spark-scratch/drive[0-3]`. Verified via 2026-05-11 18:42 audit log.
- **Source:** Vendor doc § 8.2 + fqdn-side existing infrastructure + 2026-05-11 working-session resolution

---

<a id="hipaa-4"></a>

### #H4 — Kerberos realm + service principal + keytab for Spark — **SCOPE EXPANDED 2026-05-13**

- **Status:** TO DO (Phase 3 scope; scope expanded 2026-05-13 to also back the Web UI auth flow in #H1-rev)
- **Priority:** HIGH (transmission-security pillar **plus** Web UI auth backbone)
- **Owner:** **fqdn Cybersecurity / IT — coordinate with vendor**
- **Depends on:** Existing fqdn KDC (or new realm creation if absent)
- **Triggers / informs:** Vendor's Spark install (they consume both the service keytab and the HTTP/Web UI keytab); #H1-rev (Web UI SPNEGO filter)
- **Source:** Vendor doc § 6.2 + 2026-05-13 SOW change (HTTP principal added)

Vendor calls for a dedicated Kerberos service principal `spark-etl@<YOUR_REALM>` with a keytab at `/etc/security/keytabs/spark-etl.keytab` (owner=spark, mode=0400). Token relogin period = 1m. **As of 2026-05-13**, fqdn must also generate per-host HTTP service principals (`HTTP/<host>@<YOUR_REALM>`) for the SPNEGO Web UI filter (#H1-rev) — same realm, additional principals.

**fqdn actions:**
- [ ] Confirm `<YOUR_REALM>` (existing fqdn KDC realm or new one)
- [ ] Create `spark-etl` principal in that realm (service auth)
- [ ] Create `HTTP/<host>@<REALM>` principals for each Worker VM + YARN RM VM + History Server VM (Web UI auth — new 2026-05-13)
- [ ] Generate keytabs; deploy via Ansible to all VMs with correct ownership/perms
- [ ] Document realm name + KDC servers for the vendor's Spark install config
- [ ] Verify post-install: `klist -k /etc/security/keytabs/spark-etl.keytab` + `klist -k /etc/security/keytabs/HTTP.keytab` return the expected principals
- [ ] Coordinate AD-side: `spark-admins` / `spark-users` AD groups created for SPNEGO-driven ACLs (Michelle owns AD provisioning)

---

<a id="hipaa-5"></a>

### #H5 — Verify SSE-KMS / SSE-S3 on Ceph object buckets

- **Status:** TO DO
- **Priority:** HIGH (data-at-rest pillar for object storage)
- **Owner:** **Vendor (Ksolves) until cluster sign-over** — fqdn verifies after
- **Depends on:** Vendor's Ceph RGW configuration
- **Triggers / informs:** Production data acceptance
- **Source:** Vendor doc § 8.2

Vendor will configure server-side encryption on the `s3a://ingest/` and `s3a://output/` buckets at install time. fqdn's role is verification — confirm SSE is active before any production data lands.

**fqdn actions:**
- [ ] After vendor install, run `s3cmd info s3://ingest/` (or RGW equivalent) to confirm SSE algorithm
- [ ] Confirm key management approach (SSE-KMS preferred over SSE-S3)
- [ ] Document the configuration in this CP for audit

---

## Vendor-Owned Items (Verification Only — fqdn confirms after install)

These are configured by the vendor during Spark install. fqdn's responsibility is post-install verification.

- **V1** — `spark.hadoop.fs.s3a.connection.ssl.enabled = true` (HTTPS to Ceph RGW). _(Vendor doc § 8.1)_
- **V2** — `spark.authenticate = true` + auto-shared-secret per app (RPC authentication). _(Vendor doc § 8.1)_
- **V3** — `spark.network.crypto.enabled = true` + `authEngineVersion = 2` + `cipher = AES/GCM/NoPadding` (RPC + shuffle encryption). _(Vendor doc § 8.1)_
- **V4** — `spark.ssl.enabled = true` + `spark.ssl.rpc.enabled = true` (Web UI + History Server SSL). _(Vendor doc § 8.1)_
- **V5** — `spark.io.encryption.enabled = true` + 256-bit key + HmacSHA256 keygen (local I/O encryption — shuffle spills, cache blocks). _(Vendor doc § 8.2)_
- **V6** — `spark.redaction.regex = (?i)secret|password|token|keytab|principal|credential|key` + replacement `********` (HIPAA — credential redaction in logs and Spark UI). _(Vendor doc § 6.2)_

**fqdn verification action (post-install, single sweep):**
- [ ] `grep -E '<each parameter>' /etc/spark/conf/spark-defaults.conf` on Worker VMs; confirm all V1–V6 settings present and correct
- [ ] Run a job with intentional credential in a config; verify it's redacted in Spark UI + driver logs
- [ ] Tcpdump a sample Spark RPC connection; confirm ciphertext (no plaintext PII)

---

## Closed Items

- [x] **BLOCKER.3a HIPAA Hardware Compliance — LUKS posture on NVMe scratch drives — CLOSED 2026-05-11.** Drive-level encryption verified post-resolution: hardware-only encryption on scratch drives sde–sdh (bare-mounted at `/data/spark-scratch/drive[0-3]`); OSD drives sda/sdc/sdd remain LUKS-encrypted via dm-crypt as expected. Audit log: `phases/development/phase2/Incoming/ceph_audit_msb-pmc03-01.corp.fqdn_2026-05-11_1842.log`. This satisfies the vendor's § 8.2 LUKS recommendation under the Phase 2 hardware-compliance scope and **closes the Phase 2 portion of HIPAA scope.** Phase 3 software/network HIPAA compliance (Active Items #H1, #H2, #H4, #H5 + Vendor-Owned V1–V6) remains active scope.
- [x] **#H3 — Notify Ksolves: NVMe disks already LUKS-encrypted — CLOSED 2026-05-11** (see #H3 detail above)
- [x] **(historic)** LUKS encryption on NVMe scratch drives was already in place prior to Ksolves' arrival; the vendor's install applied software LUKS on top of the existing hardware encryption (double-encryption); resolved 2026-05-11 by removing the software layer.

---

## Critical Path Sequence

```
[ #H2: decide auth target ]  ──▶  [ #H1: develop javax filter ]  ──▶  Web UI ACL live

[ #H3: notify vendor LUKS done ]  ──▶  Vendor mounts existing LUKS volumes (not new)
                                                        │
                                                        ▼
                                              [ V5: spark.io.encryption ]
                                                        │
                                                        ▼
                                              local I/O encryption live

[ #H4: Kerberos realm + keytab ]  ──▶  Vendor's Spark install consumes keytab  ──▶  RPC auth live (V2/V3)

Vendor configures V1–V6 during install
                ▼
[ #H5: fqdn verifies SSE on Ceph buckets ]
                ▼
Production data acceptance gate — all six pillars live
```

### Halt / fork conditions

- **#H2 deadlocks** (no auth target chosen): #H1 cannot start; Web UI ACL pillar stays open indefinitely. UIs must be firewalled to admin networks only as an interim measure.
- **#H3 too late**: vendor reformats existing LUKS volumes. Recovery = re-encrypt + redeploy keys + verify; ~1 day setback.
- **#H4 blocks**: vendor cannot enable Kerberos without keytab; fall back to interim shared-secret RPC, then revisit.
- **#H5 reveals SSE off**: hold production data acceptance until vendor remediates Ceph RGW config.

---

## Notes

- **Reference to main Phase 2 CP:** `Phases_Critical_Path_Development_v1.6.md` carries a BLOCKER pointing here. Resolve all items above before lifting that BLOCKER.
- **Reference to Okta CP:** `CP_Okta_v1.0.md` covers Okta integration for Airflow + Spark History Server **end-user** access. The Kerberos work in #H4 is a **separate** layer for service-to-service auth (Spark RPC, YARN). Both are needed; they don't replace each other.
- **Cybersecurity coordination:** Paul Barber (Cybersecurity) is the natural reviewer for #H2 + #H4 + #H1's auth integration. Loop him in early.
- **Audit posture:** every item closure should be accompanied by a captured-at-closure verification artifact (config grep, packet capture excerpt, etc.) for the eventual HIPAA audit trail.

---

## Footnotes

¹ Vendor source: `phases/development/phase2/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` § 8 (HIPAA Compliance Architecture & Guidelines).

² Apache Spark security reference: [https://downloads.apache.org/spark/docs/3.5.3/security.html](https://downloads.apache.org/spark/docs/3.5.3/security.html).

³ HIPAA references: 45 CFR § 164.312(e)(1) for transmission security; 45 CFR § 164.312(a)(2)(iv) for data at rest encryption.

⁴ Parent CP doc: `Phases_Critical_Path_Development_v1.6.md` (forthcoming) — carries the BLOCKER pointing to this sub-project.
