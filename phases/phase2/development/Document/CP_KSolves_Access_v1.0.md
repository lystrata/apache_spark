# Critical Path — KSolves Dev-Cluster Access

_Version 1.0 · Last updated 2026-05-05_
_Source meeting: 2026-05-01 18:09 — Paul Barber, Murali Noonela, Harper Dunning, Michelle Packert, Sean Klette, Austin Koburi, Wood, Rohn_
_Source transcript: `phases/phase2/development/Incoming/Paul Barber's meeting-20260501 1809-1.txt`_
_Status: Active — 13 fqdn-side items + 17 external-attendee dependencies_

---

## Document Overview

Sub-project critical path for giving Ksolves the access they need to install and configure Spark on the dev cluster (`msb-pmc03`) **without exposing them to the trusted corporate network.** The thread spans Proxmox AD/PAM auth, guest-VM permission delegation, hostname-vs-IP config dependencies, and the Horizon VDI / business-partner VLAN model.

This document is a companion to — and **does not duplicate** — `Phases_Critical_Path_Development_v1.3.md`, which covers Phase 2 infrastructure provisioning end-to-end. The KSolves-access concerns captured here are **upstream gates** to several Phase 2 items but are operationally separable enough to track in their own Critical Path.

### Methodology

**Scope captured:** Every commitment Wood, Rohn made during the 2026-05-01 meeting (numbered #1–#13), plus every task assigned to or recognized for another attendee that **triggers, blocks, validates, or consumes** an `#N` item. External tasks that are merely adjacent (no causal edge to an `#N`) are noted but not numbered.

**Exclusions:**
- Phase 2 infrastructure provisioning (P0.x, P1.x, P2.x) — see `Phases_Critical_Path_Development_v1.3.md`
- BLOCKER.1 Webex remote-control hardware prerequisite — see `Phases_Critical_Path_Development_v1.3.md` § BLOCKER.1
- Ksolves-side OpsWat client installation, OpsWat policy setup, and KSolves Tuesday call logistics — vendor-internal / fqdn-only

**Cross-reference convention:** Each item cites the meeting transcript section number. Dependencies between items are explicit; the **Critical Path Sequence** section near the end shows the dependency graph as a single connected diagram.

**Versioning:** This is the v1.0 cut. Subsequent material content changes get the standard `_v<MAJOR>.<MINOR>` bump per the project's distribution-doc convention.

---

## Schedule Context

The dev cluster is sitting fully provisioned (msb-pmc03-01/02/03) with baseline captures taken on 2026-04-30 (v1.0) and 2026-05-05 (v1.1 — see `node01_profile_v1.1.txt` etc. in Document/). What's blocking productive Ksolves Spark-install work is **not** the cluster — it's getting Ksolves operationally on it through a path that's secure, low-latency, and doesn't require Wood, Rohn screen-sharing 12 timezones away.

The 2026-05-01 meeting laid out the proposed solution (Horizon VDI + business-partner VLAN + AD-group-bound Proxmox console login) and the owner of each piece. This document tracks execution from there.

---

## Active Items — fqdn-side

<a id="item-4"></a>

### #4 — Verify `fqdn` AD login on Proxmox

- **Status:** IN PROGRESS
- **Priority:** HIGH (foundational — informs the design of #6, #7, #13)
- **Owner:** Wood, Rohn
- **Depends on:** None
- **Triggers / informs:** #6, #7, #13
- **Source:** Meeting §166–167

Verify that the `fqdn` AD account authenticates to the Proxmox cluster, and document Proxmox's PAM vs AD permission model. The model needs to be understood before designing `fqdn` group permissions on Proxmox so we can predict how AD-group permissions resolve at the Proxmox layer (PAM realm vs AD realm vs a hybrid).

**User actions:**
- [ ] Test `fqdn` login via Proxmox web UI and SSH on at least one msb-pmc03 node
- [ ] Document whether Proxmox is configured for PAM realm, AD realm, or both
- [ ] Confirm whether AD groups (vs individual users) can be granted Proxmox roles in the current setup
- [ ] Capture findings in this CP doc and feed into #7 design

---

<a id="item-5"></a>

### #5 — Install Tanium on the Proxmox hosts

- **Status:** TO DO
- **Priority:** MEDIUM (security visibility, not on the critical path)
- **Owner:** Wood, Rohn
- **Depends on:** None
- **Triggers / informs:** None — independent of the network-isolation thread
- **Source:** Meeting §200

Tanium (corporate security agent) is not yet installed on the msb-pmc03 nodes. Adding it gives Cybersecurity (Paul) the same telemetry/alerting visibility on these hosts that exists for the rest of the corporate fleet. **Independent** of the KSolves access work — completing this does not unblock anything else, but it's a security gap worth closing while the rest of the thread is unblocked.

**User actions:**
- [ ] Coordinate with Paul / Cybersecurity for the Tanium install package and any deployment guidance
- [ ] Install on msb-pmc03-01, -02, -03
- [ ] Verify the agents are reporting back to the Tanium console
- [ ] Confirm with Paul that visibility is in place

---

<a id="item-6"></a>

### #6 — Investigate Proxmox guest-level permission delegation

- **Status:** TO DO
- **Priority:** HIGH (gates #7)
- **Owner:** Wood, Rohn
- **Depends on:** #4 (auth model understood)
- **Triggers / informs:** #7 (selective guest access)
- **Source:** Meeting §201–217

Goal: design a Proxmox permission scheme where Ksolves can manage **only the dev VMs** they're meant to provision — not prod-grade VMs, not Grafana, not anything else hosted on the cluster. Proxmox's permission model supports per-VM or per-pool ACLs, but the exact configuration to express "fqdn gets Operator on dev pool, nothing else" needs to be tested on a real cluster.

**User actions:**
- [ ] Map all currently-provisioned VMs across msb-pmc03 (likely none yet for prod)
- [ ] Decide on the Proxmox permission scope unit (per-VM vs per-pool vs per-node)
- [ ] Draft the permission scheme on paper before applying to the cluster
- [ ] Validate the scheme against Proxmox's documented role/privilege matrix

---

<a id="item-7"></a>

### #7 — Configure console-login + selective guest access for Ksolves

- **Status:** TO DO
- **Priority:** HIGH (the operational outcome of the access thread)
- **Owner:** Wood, Rohn
- **Depends on:** #4 (auth model), #6 (permission scheme), Michelle (M1+M2: `fqdn` account & group)
- **Triggers / informs:** None — this is a leaf item
- **Source:** Meeting §218–221

Combine the auth findings from #4, the permission scheme from #6, and the AD group/account from Michelle into the actual Proxmox configuration that grants Ksolves the access they need and nothing more. "Console login + selective guest access" was Paul's framing — meaning a working Proxmox shell-or-web-UI session on the cluster nodes, scoped to the dev VMs only.

**User actions:**
- [ ] Once `fqdn` group exists in `remote.corp` (Michelle M2), create the matching Proxmox AAA realm entry
- [ ] Apply the permission scheme from #6 to the realm
- [ ] Test login as a `fqdn` member; confirm dev-VM operations succeed and prod-VM operations fail
- [ ] Document the configuration in a runbook for the production cluster (msb-pmc02) when it comes online

---

<a id="item-8"></a>

### #8 — Research hostname-based config feasibility

- **Status:** TO DO (in active discussion with Sean / Austin)
- **Priority:** HIGH (gates #9 and the entire VLAN-move option)
- **Owner:** Wood, Rohn
- **Depends on:** None
- **Triggers / informs:** #9
- **Source:** Meeting §267–286

Determine whether Proxmox + Apache Spark configurations can be driven by hostnames (resolved via DNS) instead of literal IP addresses. The reason this matters: the cleanest way to give Ksolves cluster access without exposing them to the corporate network is to **re-IP the cluster into the KSolves business-partner VLAN**, do the install work there, then re-IP back to corp at production cutover. This only works if every config file (corosync, Ceph monmap, Spark master/worker URIs, Proxmox cluster join records, /etc/hosts, /etc/network/interfaces) tolerates a hostname → IP swap underneath it.

**User actions:**
- [ ] Audit all Proxmox cluster config files for hardcoded IPs vs hostnames
- [ ] Audit all Spark / YARN configs (yarn-site.xml, spark-defaults.conf, etc.) for hardcoded IPs
- [ ] Audit Ceph monmap and OSD config for hardcoded IPs
- [ ] Document where IPs are unavoidable (i.e. a re-IP would require config edits + restart)
- [ ] Decide go/no-go on the VLAN-move approach based on findings

---

<a id="item-9"></a>

### #9 — Test IP / VLAN move on a non-Proxmox server first

- **Status:** TO DO (in active discussion)
- **Priority:** HIGH (proves the concept before risking the cluster)
- **Owner:** Wood, Rohn
- **Depends on:** #8 (research must complete first)
- **Triggers / informs:** Austin A1 (executes the actual move on the cluster)
- **Source:** Meeting §286

Before risking a re-IP on the actual Proxmox cluster — where a missed hardcoded IP could brick the corosync or Ceph layer — exercise the procedure on a less-critical Linux server. Pick a server that has some networking but no clustering dependencies. Walk through: hostnamed entries → DNS update → IP change → service restart → reverse. Validate the playbook end-to-end.

**User actions:**
- [ ] Identify a non-cluster Linux server suitable for the test
- [ ] Coordinate with networking team (Sean / Austin) on a test VLAN to move it into
- [ ] Document the move procedure in a runbook
- [ ] Execute the move; capture every config touched and every service that needed restart
- [ ] Reverse the move; confirm the server returns cleanly to its original state
- [ ] If clean, hand the runbook to Austin for cluster execution (A1)

---

<a id="item-10"></a>

### #10 — Document a Ksolves remote-config workflow

- **Status:** OPEN (awaiting Mirali Mi3)
- **Priority:** MEDIUM (latency mitigation, not on the critical path)
- **Owner:** Wood, Rohn
- **Depends on:** Mirali Mi3 (asks Ksolves whether a written ops list works for them)
- **Triggers / informs:** None
- **Source:** Meeting §221–224

Latency-mitigation alternative to live SSH-via-Webex sessions. If Ksolves is willing to send a written list of operations they want executed, Wood, Rohn drives the configuration on PMC01 himself rather than co-screen-sharing across 12 timezones. Faster turnaround per command. **Conditional** — viable only if Ksolves can fully describe their intended operations in advance, which is uncertain for an exploratory install phase.

**User actions:**
- [ ] Coordinate with Mirali on the ask (Mi3) — is Ksolves willing?
- [ ] If yes, design the handoff format (text file, git repo, ticket queue?)
- [ ] If yes, draft a runbook template Ksolves can fill in for each operation
- [ ] If no, this item closes with note "vendor preferred live sessions"

---

<a id="item-12"></a>

### #12 — Test new Horizon VDI pool as a Ksolves-equivalent user

- **Status:** OPEN (awaiting Jason J1 + J2)
- **Priority:** HIGH (proves the access path before turnover to Ksolves)
- **Owner:** Wood, Rohn
- **Depends on:** Jason J1 (VDI pool ready), Jason J2 (grants test access)
- **Triggers / informs:** None — final pre-turnover validation
- **Source:** Meeting §298–301

Once Jason finishes the Horizon VDI pool and grants access, log in as a Ksolves-equivalent user and walk through the entire access path: VDI desktop → SSH session to a msb-pmc03 node → can do work / can't escape sandbox. Verify in person, with Paul and Mirali also testing, before flipping the switch and giving Ksolves real credentials.

**User actions:**
- [ ] Wait for Jason notification that the VDI pool is ready (J1 / J2)
- [ ] Log in to the VDI; verify the desktop loads and standard tools are available
- [ ] SSH from the VDI to msb-pmc03; verify the connection succeeds and is scoped correctly
- [ ] Attempt at least one prohibited operation (e.g. ssh to a corp server outside scope); verify it's blocked
- [ ] Compare experience with Paul and Mirali; surface any concerns before turnover

---

<a id="item-13"></a>

### #13 — Assign console-login rights on Proxmox to the `fqdn` AD group

- **Status:** IN PROGRESS
- **Priority:** HIGH
- **Owner:** Wood, Rohn
- **Depends on:** Michelle M1 (account), Michelle M2 (group), Paul P2 (relays group name to Wood, Rohn)
- **Triggers / informs:** None — operational endpoint
- **Source:** Meeting §303–305

Once Michelle creates `fqdn` in `remote.corp` and Paul relays the group name back to Wood, Rohn, configure the Proxmox cluster's AAA so members of `fqdn` get console-login rights with the scoped permissions designed in #7. This is the literal moment Ksolves becomes able to log in.

**User actions:**
- [ ] Wait for Paul P2 (group name relay)
- [ ] Add `remote.corp` realm to Proxmox AAA if not already present
- [ ] Bind the `fqdn` AD group to the appropriate Proxmox role (per #7 design)
- [ ] Test login as a member of the group; verify role enforcement
- [ ] Document the configuration in a Phase 2 runbook for production-cluster reuse

---

## External Dependencies — Other Meeting Attendees

These items belong to other people; they are tracked here because each one **triggers**, **blocks**, **validates**, or **consumes** an `#N` item above. Check-marks here aren't expected — they're someone else's checkboxes.

### Michelle Packert — fqdn Networking / AD

- **M1** — _(blocks #7 + #13)_ Create `fqdn` test admin **account** in `remote.corp`. _(Meeting §225–226)_
- **M2** — _(blocks #7 + #13)_ Create `fqdn` admin **group** in `remote.corp` and share the name with Paul / Wood, Rohn. _(Meeting §303)_
- **M3** — Create a file share on the business-partner file server for KSolves document handoff. _(Meeting §307)_
- **M4** — _(validates approach for #7)_ Test whether `remote.corp` AD account permissions can be applied to a corp-domain Proxmox host. _(Meeting §155–160)_
- **M5** — Find the OpsWat persistent-client install link / instructions and share with Paul. _(Meeting §239–243)_

### Paul Barber — Cybersecurity

- **P1** — Send meeting notes summarizing what was defined / decided 2026-05-01. _(Meeting §291)_
- **P2** — _(triggers #13)_ Tell Wood, Rohn the AD group name once Michelle creates it. _(Meeting §304)_
- **P3** — Walk Ksolves through OpsWat install on a Tue+ Ksolves call (~08:00 MDT, scheduled by Mirali). _(Meeting §245–253)_
- **P4** — _(adjacent to #7 / #9)_ Plan SSH-from-KSolves-VLAN-to-cluster firewall policies (with Sean). _(Meeting §294)_
- **P5** — Lock down the OpsWat client download link + steps (with Michelle). _(Meeting §227–243)_

### Mirali Noonela — fqdn Project Lead

- **Mi1** — Schedule a Ksolves call where Paul can walk them through OpsWat install. _(Meeting §245–251)_
- **Mi2** — _(re-opens held #3 if needed)_ Report completed responsibilities back to Wood, Rohn so the Phases Critical Path doc stays current. _(Meeting §47–48)_
- **Mi3** — _(triggers #10)_ Ask Ksolves whether they can send a written ops list so Wood, Rohn can drive config from PMC01 instead of co-screen-share. _(Meeting §221–224)_

### Sean Klette — fqdn Networking

- **S1** — Continue Azure ExpressRoute / virtual-private-link setup. _(Meeting §101–102)_
- **S2** — _(related to #9)_ Plan SSH firewall policies for KSolves VLAN → cluster (with Paul). _(Meeting §294)_

### Austin Koburi — fqdn Networking

- **A1** — _(consumes output of #9)_ Once hostname-feasibility lands and the move is validated, execute the IP / VLAN move + DNS updates on the cluster. _(Meeting §283)_

### Jason Waites — fqdn VDI / Horizon

- **J1** — _(blocks #12)_ Finish setting up the KSolves Horizon VDI pool — currently working through PowerShell-command issues. _(Meeting §296–297)_
- **J2** — _(blocks #12)_ Grant Paul, Wood, Rohn, and Mirali access to the VDI pool as KSolves-equivalent users for testing. _(Meeting §298–302)_

### Harper Dunning — Project Manager

- **H1** — Update the EDS data-flow / roadmap diagram to include the Azure private-link / ExpressRoute icon. _(Meeting §88)_

---

## Closed Items

- [x] **#1** — Run baseline capture commands on the other two cluster nodes. _Resolution: outputs cleaned and promoted as `node01_profile_v1.1.txt`, `node02_profile_v1.1.txt`, `node03_profile_v1.1.txt` in `phases/phase2/development/Document/`._ _(Meeting §2)_
- [x] **#2** — Add Paul Barber to the Phases Critical Path distribution list. _Resolution: closed — confirmed 2026-05-05._ _(Meeting §108)_
- [x] **#11** — Send network / firewall / DNS questions to Ksolves. _Resolution: verified sent. Source: `correspondence/Document/Ksolves Network Firewall DNS Query.md` (2026-04-30)._ _(Meeting §313)_

---

## Held Items

- **#3** — Update Phases Critical Path doc as Mirali reports progress. _Status: Held — no action at this time. Re-opens automatically if/when Mirali Mi2 fires (i.e. an update arrives that warrants a doc bump)._ _(Meeting §47–48)_

---

## Critical Path Sequence

The dependency chain from blockers to outcomes. Solid arrows indicate **blocks**; dashed arrows indicate **informs / triggers / validates**.

```
                                      ┌──────────────────────────┐
                                      │  Michelle M1: account    │
                                      │  Michelle M2: group      │
                                      │  in remote.corp          │
                                      └────────────┬─────────────┘
                                                   │ (blocks)
                                                   ▼
                                          ┌────────────────┐
                                          │ Paul P2: relay │
                                          │ group name to  │
                                          │ Wood, Rohn     │
                                          └────────┬───────┘
                                                   │ (triggers)
                                          ┌────────┴────────┐
                                          ▼                 ▼
                          ┌──────────────────┐   ┌──────────────────────┐
       Wood, Rohn #4  ─ ─▶ #7: console-login │   │ #13: assign console- │
       (PAM/AD model)     │ + selective       │   │ login rights to AD  │
                          │ guest access      │   │ group on Proxmox    │
                          └────────▲──────────┘   └──────────────────────┘
                                   │ (informs)
                          ┌────────┴──────────────┐
                          │ #6: investigate guest │
                          │ permission delegation │
                          └───────────────────────┘
                                   ▲
                                   │ (validates)
                          ┌────────┴──────────────┐
                          │ Michelle M4: AD-perm  │
                          │ feasibility test      │
                          └───────────────────────┘


       Wood, Rohn #8 ────▶ Wood, Rohn #9 ─────▶ Austin A1: execute
       hostname             test IP move on    IP/VLAN move + DNS
       feasibility          non-cluster server


       Mirali Mi3 ───────▶ Wood, Rohn #10:
       (ask Ksolves for     drive config remotely
       written ops list)    on PMC01


       Jason J1 ─────────▶ Jason J2 ─────────▶ Wood, Rohn #12:
       VDI pool ready      grant access        test VDI as
                                                Ksolves-equivalent user


       Wood, Rohn #5 ─── independent — no external dependency
       (Tanium install)


       Paul P4 / Sean S2 ─── adjacent — depends on outcome of #9
       (SSH firewall policy planning)
```

### Reading the chain

- **Top cluster (centered):** Two Michelle items + one Paul relay step gate **both** of Wood, Rohn's near-term operational items (#7 and #13). Wood, Rohn's #4 and #6 feed the design but don't gate the unlock; they happen in parallel with Michelle's work.
- **Middle chain (left):** The hostname-feasibility → IP-move-test sequence has a clear handoff from Wood, Rohn to Austin. If #8 returns "no" (hardcoded IPs are unavoidable), this entire chain is moot and the team falls back to permission-only isolation via the top cluster.
- **Right side:** Three independent threads — Mirali's vendor question (Mi3 → #10), Jason's VDI work (J1+J2 → #12), and the Tanium install (#5).

### Halt / fork conditions

- **#8 returns "no":** the VLAN-move plan dies; #9 closes as "not viable"; rely entirely on the permission-only path (#7 + #13) for isolation.
- **Michelle M4 returns "no":** the entire AAA approach for #7 needs rethinking — likely reverts to local-Proxmox-account-only, without `remote.corp` integration.
- **Mirali Mi3 returns "no":** #10 closes as "vendor preferred live sessions"; Wood, Rohn continues co-screen-sharing for the foreseeable future.
- **Jason J1 stalls indefinitely:** #12 stays open; if BLOCKER.1 (Phase 1A Webex hardware) closes first, work proceeds via Webex while VDI catches up.

---

## Notes

- Interdependencies among #6 / #7 / #8 / #9 / #12 are loose — the order of resolution may shift as research items resolve.
- Tanium (#5) is parallel and unrelated to the network-isolation chain; it's listed here only because it was a meeting commitment.
- Items #8 and #9 are in active discussion with Sean (network) and Austin.
- **#13 has two upstream blockers** (Michelle's M1+M2, then Paul's P2) — the diagram above makes this two-step gate explicit.
- The companion **interactive HTML tracker** at `phases/phase2/development/Document/cp_ksolves_access_tracker_v1.0.html` mirrors this content with collapsible sections, per-checkbox auto-save to browser localStorage, and a critical-path-sequence visual.
- Daily digest of the in-progress state lands in inbox at 07:30 Mon–Fri (see `Scripts/send_subproject_digest.py`). Source for that digest is currently the working `Notes/ksolves_dev_access_subproject.md` — to be migrated to this CP doc once stabilized.

---

## Footnotes

¹ Meeting transcript: `phases/phase2/development/Incoming/Paul Barber's meeting-20260501 1809-1.txt` — section numbers in this document refer to the WEBVTT cue numbers in that transcript.

² `Phases_Critical_Path_Development_v1.3.md` (in this Document/ directory) — the parent Phase 2 critical path. KSolves-access concerns gate several P0/P1 items there; this CP doc isolates them for cleaner tracking.

³ `Scripts/send_subproject_digest.py` — the daily digest script that emails the working tracker (sanitized) to the user every weekday morning.
