# Vendor email — ExaBGP configuration requirements

**To:** Prashamt Tripathi, Kerthik Hegde (Ksolves)
**From:** Rohn Wood
**Subject:** ExaBGP configuration requirements — Phase 3
**Date:** 2026-05-14
**Status:** Sent 2026-05-14 — awaiting recipient response

---

Hi Prashamt, Kerthik,

As we firm up Phase 3, I have a configuration-spec request for our network team on the ExaBGP layer.

With RGW running on the Spark cluster nodes (as confirmed by the dev install on `msb-pmc03`), the original architecture has ExaBGP advertising the Ceph RGW S3 endpoint as a VIP from each RGW-bearing node toward our network fabric.

**Preliminary question — please confirm:** does your Spark and RGW client configuration support a single VIP fronted by ExaBGP failover, or does it currently hardcode per-node RGW addresses? Confirming this up front ensures the VIP pattern is actually the architecture we're building toward.

**If the single-VIP / ExaBGP pattern is what you're delivering,** our network engineer Sean owns the upstream BGP configuration on the fqdn side. To configure that side correctly, we need from you a short configuration spec covering:

- **BGP AS numbers** — the AS the RGW nodes (ExaBGP speakers) will use, and the AS expected on the upstream peer.
- **Peering model** — eBGP or iBGP; direct neighbor sessions or via a route reflector.
- **VIP details** — the prefix(es) to be advertised, the VIP IP(s), and the VLAN on which they sit.
- **Source addresses** — which interface / VLAN on each RGW node originates the BGP session (we'll map this to firewall and ACL policy on the upstream side).
- **Authentication** — MD5 / TCP-AO requirement on the BGP session, or no auth.
- **Timers** — hold timer, keepalive interval; BFD enable and timers if applicable.
- **Route policy** — any prefix-list / route-map you expect on the upstream side.
- **Load distribution** — active/active anycast across multiple RGW nodes (ECMP on the upstream) or active/standby.
- **Failover behavior** — handling of graceful shutdown vs. ungraceful node failure; whether detection is BFD-driven or BGP hold-timer expiry.

Per-cluster scope:

- **Dev cluster (`msb-pmc03`):** RGW is already running on the nodes; bring ExaBGP into the dev environment as part of Phase 3 for validation.
- **Prod cluster (`msb-pmc02`):** Once the prod cluster is brought online (gated on outstanding CPU hardware), the same pattern applies.

A paragraph per bullet above is plenty — Sean can drive the upstream configuration from that.

---

Happy to walk through any of this in our next status sync or in a dedicated working session — whichever fits your schedule.

Thanks,
Rohn
