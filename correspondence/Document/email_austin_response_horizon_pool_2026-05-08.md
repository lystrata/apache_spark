**From:** Austin (fqdn Network)
**To:** Rohn, Sean Klette (cc as appropriate)
**Date:** 2026-05-08
**In response to:** `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`
**Subject:** Re: Ksolves Horizon Pool — alignment on next steps

---

## Verbatim reply (Austin)

> That is, CS would be the horizon connection servers in this circumstance. The policies are enforced at the firewalls for this traffic. The horizon pool used the firewall as the default gateway so we can enforce traffic from that point easily.

---

## What this answers (from the 2026-05-07 alignment email)

| Question | Answered? | Resolution |
|---|---|---|
| 1. CS's = Horizon Connection Servers? | ✅ Confirmed | "CS would be the horizon connection servers in this circumstance." |
| 2. Policy enforcement layer? | ✅ Confirmed | **Network firewall.** Not NSX micro-segmentation, not host-level on the pool VMs. |
| 3. Interaction with Sean's cluster-side design? | ⏳ Not directly addressed | Sean is the right party to answer the cluster-side half. |

## New context worth capturing

- **The Horizon pool uses the firewall as its default gateway.** All egress from the pool VMs flows through the firewall by default routing — Austin gets a **single chokepoint** to enforce policy without needing per-VM or per-route configuration. Adding/removing allowed destinations is a firewall rule change at one place.
- Implication for the BLOCKER.4 design: when the **Snowflake / Azure egress allowlist** lands (Rohn's open BLOCKER.4 sub-task — currently FQDN-based vs. published CSP IP ranges vs. egress proxy), the output feeds **Austin's firewall** as additional allow-rules at this single chokepoint. Whichever mechanic is chosen, the deployment surface is one firewall, not many.

## Layering hypothesis — status after Austin

The hypothesis from the 2026-05-07 email — *Austin's pool-level controls bound egress; Sean's cluster-side controls bound ingress into msb-pmc03* — is **consistent with Austin's response.** The pool-egress chokepoint at Austin's firewall is the single policy point for what the pool can talk to. Sean's cluster-side work would still constrain what msb-pmc03 accepts from those allowed destinations.

The layering picture:

```
[Vendor device] → [UAG] → [Horizon pool VM]
                              │
                              │  (default gateway = firewall)
                              ▼
                          [Austin's firewall]   ← single egress chokepoint
                          allow: DNS, AD, UAG, CS, + Sean's-design destinations
                          deny: everything else
                              │
                              ▼
                          [allowed destinations]
                              │
                              ▼ (entering msb-pmc03)
                          [Sean's cluster-side controls]   ← TBD
                          (what msb-pmc03 accepts from allowed sources)
```

This framing should be confirmed once Sean weighs in on the cluster-side half.

## Still outstanding (BLOCKER.4 sub-tasks unaffected by this reply)

- **Sean Klette's response** on cluster-side design layering — confirms or revises the layering picture above
- **Cluster-side isolation design** (Sean Klette) — VLAN-isolation proposal vs. alternative paths; resolution of the `10.1.37.0/24` cluster overlap
- **Pool validation testing** (Sean + Rohn) — using `ks_test` AD group before any vendor accounts are provisioned
- **Snowflake / Azure egress allowlist mechanics** (Rohn) — feeds Austin's firewall once landed
- **Vendor user list** for VDI accounts (Michelle bridge + Ksolves)
- **Cyber endorsement** of the final design (Paul Barber)
- **CIO risk-acceptance sign-off** (Rob Ball)
- **Phase 1B exit-condition decision** (Rohn + Paul Barber)

## Cross-references

- Main CP — `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md` § BLOCKER.4
- Security planning note (on-site only) — `security/Notes/vendor-access-isolation-plan_2026-05-06.md`
- 2026-05-07 outbound email — `correspondence/Document/email_sean_austin_horizon_pool_alignment_2026-05-07.md`
- 2026-05-07 vendor email — `correspondence/Document/vendor_email_horizon_vdi_security_revision_2026-05-06.md`
