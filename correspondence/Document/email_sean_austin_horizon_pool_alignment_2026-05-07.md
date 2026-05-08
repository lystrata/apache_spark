**Subject:** Ksolves Horizon Pool — alignment on next steps

Hi Sean, Austin —

Quick note to make sure we're all looking at the same picture after Jason's and Austin's updates today.

**What I understand has happened:**
- The Ksolves Horizon pool is built and reachable via UAG (per Jason)
- `ks_test` AD group is on the pool, so Sean and I can validate before any actual vendor accounts come in
- Austin has policies in place: pool can reach DNS, AD, UAG, and the Connection Servers; everything else blocked until further notice

That puts us at *test-ready, pending validation by Sean and me*. Real progress — but one sub-task, not the whole picture. The broader vendor-isolation requirements from the CIO's 5/6 directive all remain open.

**A few things I want to confirm so I don't carry the wrong read:**

1. **Austin** — when you say "CS's," I'm reading that as Horizon Connection Servers (the broker tier). Confirm or correct?
2. **Austin** — what layer are these policies enforced at? Network firewall, NSX micro-seg, or host-level on the pool VMs?
3. **Sean** — given Austin's pool-level constraints, does that change how you're sizing the cluster-side isolation work (the VLAN-37/38/39 tenancy + VLAN-10 chokepoint we'd been researching)? My read is that Austin's policies constrain the pool itself while your work would constrain what the pool can reach into msb-pmc03 — so they layer rather than replace. Want to make sure that's how you see it too.

**Still open from the CIO-directive sub-task list:**
- Pool validation testing (Sean + me)
- Cluster-side isolation design (Sean's lead)
- Cyber endorsement of the final design (Paul)
- CIO risk-acceptance sign-off (Rob)
- Phase 1B exit-condition decision
- Snowflake / Azure Blob endpoint enumeration for the egress allowlist
- Ksolves user list (Michelle owns; awaiting)
- OPSWAT install confirmation on Ksolves devices (vendor-side; awaiting)

**Suggested next step:** Sean and Austin sync on how the pool-level policies interact with the cluster-side design we've been researching, then loop me in on whatever comes out of that. I'd like to fold the result into the Critical Path doc.

Thanks

Rohn
