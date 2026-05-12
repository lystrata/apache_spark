**From:** Sean Klette (fqdn Network)
**To:** Rohn, Austin (cc as appropriate)
**Date:** 2026-05-08
**In response to:** `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`
**Subject:** Re: Ksolves Horizon Pool — alignment on next steps

---

## Verbatim reply (Sean)

> This does not change the cluster side and related VM isolation as planned.

---

## What this answers (from the 2026-05-07 alignment email)

| Question | Answered? | Resolution |
|---|---|---|
| 1. CS's = Horizon Connection Servers? | ✅ Confirmed (Austin 2026-05-08) | "CS would be the horizon connection servers in this circumstance." |
| 2. Policy enforcement layer? | ✅ Confirmed (Austin 2026-05-08) | Network firewall — pool's default gateway. Single chokepoint. |
| 3. Interaction with Sean's cluster-side design? | ✅ Confirmed (Sean 2026-05-08) | **Pool-level work does not change cluster-side / VM isolation as planned.** Layering confirmed. |

## What Sean's reply means

Sean is treating his cluster-side design as **orthogonal to Austin's pool-level firewall work**. The two layers operate independently:

- Austin's firewall bounds **what the pool can talk to** (egress, enforced at the pool's default gateway).
- Sean's cluster-side controls bound **what msb-pmc03 accepts from those allowed destinations** (ingress + intra-cluster isolation).

Pool-side decisions don't reduce or expand Sean's cluster-side scope. Sean's existing plan (VLAN-isolation proposal — make msb-pmc03 the sole tenant of VLANs 37/38/39 + add VLAN 10 as a controlled ingress/egress chokepoint, or one of the alternative paths from the `10.1.37.0/24`-overlap addendum) **proceeds as designed**.

## Layering picture — both parties' input received (final)

```
[Vendor device] → [UAG] → [Horizon pool VM]
                              │ (default gateway = firewall)
                              ▼
                       [Austin's firewall]   ← Austin's layer (egress)
                       allow: DNS, AD, UAG, CS, + Sean's-design destinations
                       deny: everything else
                              │
                              ▼
                       [allowed destinations]
                              │ (entering msb-pmc03)
                              ▼
                       [Sean's cluster-side controls]   ← Sean's layer (ingress + VM isolation)
                       (cluster-side design as planned — VLAN approach or alternative)
```

Layering confirmed by both parties. Sub-task **"Sean + Austin sync on pool ↔ cluster-side design layering"** is **closed 2026-05-08**.

## What remains open (BLOCKER.4 sub-tasks not affected by this reply)

- **Sean's cluster-side isolation design** (the actual proposal — VLAN approach or alternative; resolution of the `10.1.37.0/24` cluster overlap)
- **Pool validation testing** (Sean + Rohn) — using `ks_test` AD group before any vendor accounts are provisioned
- **Snowflake / Azure egress allowlist mechanics** (Rohn) — feeds Austin's firewall as additional allow-rules at the single chokepoint
- **Vendor user list** for VDI accounts (Michelle bridge + Ksolves)
- **Cyber endorsement** of the final design (Paul Barber)
- **CIO risk-acceptance sign-off** (Rob Ball)
- **Phase 1B exit-condition decision** (Rohn + Paul Barber)

## Cross-references

- Main CP — `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.5.md` § BLOCKER.4
- Security planning note (on-site only) — `security/Notes/vendor-access-isolation-plan_2026-05-06.md`
- 2026-05-07 outbound email — `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`
- 2026-05-08 Austin reply — `correspondence/Document/email_austin_response_horizon_pool_2026-05-08.md`
