# Email Draft — Vendor: Phase 1B Horizon VDI Security Redesign

_Drafted 2026-05-06 by Rohn_
_For Murali's review and forward to Ksolves_
_Status: **Draft** — placeholder names in `[brackets]`; replace at send time_

---

## Subject

Phase 1B Horizon VDI access — security redesign required; interim plan

---

## Body

Hi [recipient name],

I'm writing to update you on a development on our side that affects the timeline for the Horizon VDI access we'd been working toward for Phase 1B.

Following an internal review with our Cyber and Network teams, our CIO has determined that the originally proposed VDI access path needs additional security controls before he is comfortable authorizing it for an external vendor at the level of system access this engagement requires. The concern centers on the breadth of corporate-network exposure that root console access on our RHEL hosts implies, even with the VDI session itself in an isolated segment. The standard contractor VDI pattern we use elsewhere in the company doesn't quite map cleanly to a build of this depth, and the CIO has asked that we tighten the controls before granting direct access.

We are not stepping back from the engagement — we are stepping back to do the security design properly so the CIO can authorize the access cleanly. Our Network lead and I are actively redesigning the access architecture to constrain your team's reachable surface to exactly the systems you need (the Spark cluster nodes, the bastion VM, AD domain controllers, DNS, and the cloud egress endpoints), using a combination of VLAN segmentation and host-level controls. Once we have a design we believe will pass risk review, our Cyber lead will assess it, and the CIO will be asked to sign off. Given the design is non-trivial, I am not in a position to commit to a firm date yet, but my expectation is that this is measured in days, not weeks.

In the meantime, **Phase 1A continues unchanged** — Webex screen-sharing access is operational, and your team has been making real progress through that channel. I appreciate the patience that has required, particularly given the timezone difference. To minimize the disruption while we sort the access design, **I will do everything I can on this side to assist with configuration, installation, and any other setup work that you are comfortable with me performing under our SOW.** If there are specific steps where supervised execution by me — with your team walking me through the work via Webex — would meaningfully reduce the burden on your engineers during this interim, please let me know and we will coordinate. I want to be useful during this period rather than simply waiting on the new design to land.

I will keep you updated as the security redesign progresses, and I will let you know as soon as we have a target date for VDI access. Please reach out if you have questions, or if there is something specific I should pick up this week to help keep the work moving.

Thank you for your team's continued partnership and flexibility.

Best regards,
Rohn

---

## Send-time checklist

- [ ] Replace `[recipient name]` with actual recipient name(s)
- [ ] Confirm cc list (Murali, others?)
- [ ] Murali reviews and approves wording
- [ ] Forward to Ksolves
- [ ] After send, promote this file from `correspondence/Ready_For_Review/` → `correspondence/Document/` and update the TODO entry "Draft vendor-isolation email to Ksolves" to closed

---

## Notes on tone and content

- Acknowledges the change without throwing the CIO under the bus — frames it as a pragmatic posture adjustment, not a reversal.
- Honest about not having a date — avoids over-committing.
- Concrete offer to assist within SOW bounds, per Rohn's direction (the offer is the actual softening, not the apology).
- Tone is professional, warm, partner-not-adversary. Not groveling.
- Implicitly affirms the existing Webex Phase 1A path is working, which it is (NUC issue resolved 2026-05-06).
- Names of internal reviewers (Cyber lead, Network lead, CIO) are referenced by role, not by name, in the email body. The vendor doesn't need names; if specific names help on the user's review pass, edit as needed.

---

## Cross-references

- `security/Notes/vendor-access-isolation-plan_2026-05-06.md` — full meeting capture, design state, and action items behind this letter
- `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.4.md` § BLOCKER.1 — Phase 1A/1B tracking
- `TODO.md` § Vendor Access Isolation — Phase 1B VDI Security Gate — owns the action items
