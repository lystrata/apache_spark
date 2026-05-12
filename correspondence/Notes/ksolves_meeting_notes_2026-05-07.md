# Ksolves Daily Stand-up — Meeting Notes Capture

_Captured 2026-05-07 from Ksolves' formal meeting note (PDF in Incoming/, Webex meet held 2026-05-07 IST / late 2026-05-06 CST)_
_Sanitized: vendor first names → role descriptors; fqdn corp identifier abstracted_
_Source PDF: `phases/development/phase2/Incoming/Meeting_Notes_07_May_2026.pdf` (gitignored)_

---

## Attendees

| Role | Organization |
|---|---|
| Vendor lead | Ksolves |
| Vendor engineer 1 | Ksolves |
| Vendor engineer 2 (new on roster — first appearance 2026-05-07) | Ksolves |
| Murali | fqdn |
| Rohn | fqdn |
| Sean | fqdn |
| Rama (Ramakrishna) | fqdn |

Note: vendor engineer 2 (Devansh Singh) is new to the meeting roster as of this date. Worth tracking when the vendor user list lands for VDI account provisioning — see TODO § Vendor Access Isolation.

---

## Discussion Points

### Proxmox Setup & VM Creation

Vendor engineer 1 had a prior call with Rohn to analyze Proxmox setup and VM creation requirements. Ksolves has prepared Ansible scripts for VM creation (locally tested on their side). Rohn shared environment-specific details (node logs, drive layout, RAM). **Vendor engineer 1 will update the environment-specific variables in the scripts and share them with Rohn for execution.**

This is operationally significant: it implies a continuation of the "fqdn performs portions of the installation" path captured in Harper's 2026-05-06 summary item #10. Rohn is being asked to execute Ksolves' scripts on the Proxmox cluster directly. That has contract / certification implications already flagged in TODO and in `security/Notes/vendor-access-isolation-plan_2026-05-06.md` § Approaches Considered and Ruled Out.

### Remote Session / VDI Access

VDI permissions from the fqdn side remain pending (matches our Phase 1B gate state). For Phase 3 execution, Ksolves states a live remote / screen-share session is required to handle real-time changes during script execution; without it, "any issue would require local changes, re-sharing, and re-running — which is inefficient." This corroborates the team's position and reinforces the urgency of landing Sean's design.

### Extended Working Hours

Vendor engineer 1 will extend his working hours to align with Rohn's timezone — narrows the IST/CST overlap from ~2–3 hours/day to a more useful window. Rohn confirmed full availability during normal workday and offered nighttime availability if needed.

### Production Calculator & RAM Update

Rohn shared the production sizing calculator. Dev-cluster RAM **finalized at 320 GB/node** (formally confirmed in this meeting). Production sizing remains pending the data questionnaire response from Rama's team.

### Data Questionnaire (Production Sizing)

**Important context for the staged questionnaire response doc** (`correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md`):

Rama confirmed the questionnaire has been filled out and shared internally with his team for second-opinion / deeper-analysis review. Once finalized, it will be sent to Ksolves. This is a prerequisite for production resource mapping (data size, SLAs, codec considerations, storage estimates).

**Note for Rohn:** The Ready_For_Review draft was authored as the user's own pass at the answers. The meeting indicates Rama's team is leading the formal response. Reconciliation needed: is the user's draft input to Rama's team, or are these parallel response paths? Worth a quick sync with Rama before the staged doc gets promoted.

### DNS & Firewall Questions

The DNS / firewall question list previously shared by Rohn (`correspondence/Document/Ksolves Network Firewall DNS Query.md`, sent 2026-04-30) was not discussed in the previous session — vendor lead was absent. **Vendor engineer 1 will share the question sheet (with vendor responses) via Google Drive today** for Rohn's review. Walkthrough scheduled for the next session.

This closes part of the "Awaiting Ksolves reply on network/firewall/DNS access matrix" item that's been in TODO under Waiting for Vendor Reply since 2026-04-30.

### Script / Code Sharing Channel

Google Drive (previously shared by vendor lead) was tested. Rohn confirmed he can download files. **Agreed: Google Drive is the primary channel for sharing scripts and documents** until a better option (read: VDI) is available.

This is a working-channel decision worth knowing — script/config artifacts moving between fqdn and vendor pass through Google Drive in the interim. When VDI lands, this channel can sunset.

### Vendor Lead Availability

Vendor lead on leave 2026-05-07 (Ksolves day). Vendor engineers 1 and 2 will cover the call.

---

## Action Items (verbatim from Ksolves' formal note)

| Owner | Action Item | Notes |
|---|---|---|
| Vendor engineer 1 | Update environment-specific variables in Ansible scripts; share via Google Drive | Based on logs Rohn shared |
| Vendor engineer 1 | Extend working hours aligned with Rohn's timezone | Phase 3 execution coverage |
| Vendor lead | Reshare Google Drive link with Rohn | Primary script / document channel |
| **Rohn** | **Review DNS & Firewall questions shared by Vendor engineer 1** | Walkthrough next session — NEW TODO entry |
| Rama's team | Finalize and share data questionnaire responses with Ksolves | Production resource-mapping prerequisite |

---

## Items For Rohn To Reconcile

1. **Production questionnaire path** — `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` (drafted earlier by Rohn) vs Rama's team's response (in flight). Sync with Rama before promoting the Ready_For_Review draft.
2. **Vendor engineer 2 (Devansh Singh)** — first appearance on the roster. Confirm whether he's permanent on the engagement and ensure he's included in Ksolves' user list for VDI account provisioning when that arrives (TODO § Waiting for Vendor Reply).
3. **Script-execution-by-Rohn pattern** — already happening (Vendor engineer 1 sharing finalized Ansible scripts for Rohn to run). This implicitly executes Harper's item #10 ("fqdn performs portions of installation"); legal / contract / certification review still queued in TODO. May want to pull that forward given the pattern is already in motion.

---

## Cross-references

- `phases/development/phase2/Incoming/Meeting_Notes_07_May_2026.pdf` — original PDF (gitignored)
- `security/Notes/harper_meeting_summary_vdi_security_2026-05-06.md` — companion: project-coordinator summary of the cyber/CIO meeting one day prior
- `security/Notes/vendor-access-isolation-plan_2026-05-06.md` — the design state behind the VDI delay
- `correspondence/Document/vendor_email_horizon_vdi_security_revision_2026-05-06.md` — promoted email draft to Ksolves about the VDI redesign (covers context the vendor sees on their side)
- `correspondence/Document/Ksolves Network Firewall DNS Query.md` — the original DNS/firewall query Rohn sent 2026-04-30, now circling back with vendor responses
- `correspondence/Ready_For_Review/prod_architecture_questionnaire_responses_v1.0.md` — staged draft response to Ksolves' production architecture questionnaire (reconciliation needed per item 1 above)
- `TODO.md` — action items integrated under § Vendor Access Isolation and § Waiting for Vendor Reply

---

## Revisions

| Date | Summary |
|---|---|
| 2026-05-07 | Initial document — sanitized capture of Ksolves' formal meeting note from the 2026-05-07 daily stand-up |
