**Status:** Sent 2026-05-08 — awaiting vendor response
**From:** Rohn (fqdn)
**To:** vendor lead (Ksolves)
**CC:** Murali (per existing vendor-correspondence convention)
**Date:** 2026-05-08
**Subject:** HIPAA § 8.3 — Web UI Access Control: confirming responsibility split for the custom javax servlet filter

---

Hi [vendor lead],

Quick clarification on the HIPAA Web UI ACL scope from the configuration document § 8.3.

## Background

The vendor configuration document (`Ksolves_Spark_YARN_Config_v1.0.pdf` § 8.3) calls for a **custom javax servlet filter** for Spark Web UI / History Server access control, since Apache Spark provides no built-in ACL mechanism for those interfaces. In our internal critical-path tracking, we've **assumed this is a fqdn development task** — i.e., we'd build the filter ourselves with our development team, integrating with our chosen auth target (Okta / LDAP / Kerberos).

We've flagged it as **#H1 — High Priority** in our internal HIPAA action items because if it's fqdn-side, we need to start the dev team conversation now to keep BLOCKER.3b (HIPAA software & network compliance) on track for production go-live.

## Three questions

1. **Ownership:** Is the custom javax servlet filter on the **fqdn side** (we build it with our dev team), or is Ksolves planning to deliver it as part of the Spark / YARN install?

2. **Reference implementations:** If fqdn-side, do you have any **reference filter implementations or recommended patterns** from prior deployments we can use as a starting point? Even a "look at how we did it for [other client]" pointer would help kick off the work efficiently.

3. **Auth integration target:** What auth integration target do you recommend for the filter? Options we're considering:
   - Direct Okta OIDC (our chosen IdP — see `CP_Okta_v1.1.md`)
   - Our LDAP service
   - Kerberos (vendor doc § 8.1 mentions Kerberos for Spark service auth)
   - Other?

   We have `CP_Okta_v1.1.md` tracking the broader Okta integration; coordination with that document would be useful when we land on the auth path.

## Apache Spark reference

For context on what Spark provides natively (and doesn't):
https://spark.apache.org/docs/3.5.3/security.html

Spark's documentation confirms that **Web UI ACLs are not built in** — operators must layer either a reverse proxy (e.g., Nginx + oauth2-proxy) or a custom servlet filter, which aligns with the vendor doc § 8.3 framing.

## Why this is urgent

If it's **fqdn-side**, we need to:

- Engage our development team for the implementation
- Decide auth integration target (likely Okta — needs coordination with Paul Barber on the Cyber side)
- Build, test, integrate with the Spark History Server (P1.1) and YARN UI

That's a multi-week effort, and it gates BLOCKER.3b closure → which gates production ePHI processing. Confirming ownership now lets us start the right work in parallel with Phase 3.

If it's **Ksolves-side**, we'd love to know your delivery timeline so we can sequence the auth integration tasks (CP_Okta_v1.1) appropriately.

Thanks,

Rohn

---

## Internal tracking notes (not part of the email body)

- **Subject of letter:** H1 javax filter verification — item 13 from the 2026-05-08 review punch-list
- **Why a separate letter from the Phase 2 closing letter:** the Phase 2 closing letter is about Phase 2 sign-off + HIPAA framing + LUKS software question. This one is a focused single-topic question on § 8.3 fqdn-vs-vendor ownership. Keeping them separate prevents the response on H1 from getting buried in a multi-question Phase 2 reply.
- **Cross-references:**
  - Main CP — `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md` § BLOCKER.3b (HIPAA Software & Network Compliance)
  - HIPAA sub-project — `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md`
  - Vendor configuration document — `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` § 8.3
  - CP_Okta — `phases/phase2/development/Document/CP_Okta_v1.1.md`
- **Pairs with:** `correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md` (broader Phase 2 closure verification)
