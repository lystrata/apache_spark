**Status:** Draft — cover email for the attached HTML report. Send when ready.
**From:** Rohn (fqdn)
**To:** Ksolves lead
**CC:** Murali (per existing Ksolves-correspondence convention)
**Date:** 2026-05-08
**Subject:** Proxmox / Ceph cluster audit — findings for verification (HTML attached)
**Attachment:** `proxmox_audit_findings_to_ksolves_2026-05-08.html`

---

Hi [Ksolves lead],

I ran an audit of the dev cluster from `msb-pmc03-01` after your installation and configuration work. The cluster looks healthy overall — `HEALTH_OK`, full MON quorum (3/3), all 9 OSDs up and in, 209 placement groups `active+clean`, MGR active, RGW responding. Most of what I see matches expectations.

I've attached the full audit report as HTML (`proxmox_audit_findings_to_ksolves_2026-05-08.html`). It covers:

- Ceph version, cluster status, health detail
- MON quorum, MGR / OSD / RGW state
- OSD tree and capacity / utilization tables
- Pool composition (8 pools, 209 PGs)
- Placement-group state
- CephFS / MDS status
- Ceph config diff (non-default values)
- A redacted authentication-keys section confirming the structure of the auth posture without exposing secrets

For reference, I've also attached the raw output of the audit script (`proxmox_audit_raw_output_2026-05-08.txt`) so you can see the underlying `ceph` CLI output the report was built from. Authentication-key values are redacted in transit (`[REDACTED]`); entity names and capabilities are preserved so the auth-posture structure is visible.

The audit script ran cluster-wide Ceph commands from one node, so it doesn't include per-node OS / Proxmox / drive-encryption state. I'll run a per-node script on each of `msb-pmc03-01 / -02 / -03` separately to capture that. **If you have a recommended audit script you've used on prior installations, please share it** so we can align our verification with your install patterns.

A handful of items I'd like to clarify before signing off on Phase 2. They're spelled out with full context in § 13 of the attachment. The summary table below is for the quick look.

Once we have responses on the items below, we can either close out Phase 2 cleanly or capture remaining items as Phase 2 follow-ups.

## Items for verification (summary — full context in the attached HTML § 13)

| # | Topic                       | What we'd like to confirm                                                                                                                                                              |
| - | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Ceph version                | Configuration baseline references **Reef 18.2.x**; deployed version is **Squid 19.2.3**. Was the upgrade intentional? Compatibility testing against Spark 3.5.3 + Hadoop 3.4.1?        |
| 2 | CephFS MDS state            | Both deployed MDS daemons in STANDBY; no active MDS. Is CephFS expected to be active at this stage? `mds.msb-pmc03-02-cephFS` has a key but isn't appearing in the MDS status output. |
| 3 | OSD device class            | All 9 OSDs tagged `ssd`. Underlying drives are 3.84 TB NVMe. Was `ssd` deliberate, or should the class be `nvme`?                                                                      |
| 4 | Pool naming / posture       | Pools `phi-data`, `audit-logs`, `vm-disks` named in production-style. Is SSE configured on `phi-data`? Is `audit-logs` for centralized audit logging with WORM / object-lock? Is `vm-disks` the production-style RBD pool? |
| 5 | mclock IOPS calibration     | `osd_mclock_max_capacity_iops_ssd` calibrated values present for OSDs 1, 2, 3, 5, 8; missing for 0, 4, 6, 7. Calibration not run on those, or values matched defaults?                |
| 6 | RGW server-side tuning      | Configuration document § 6.4 recommends `rgw_thread_pool_size = 512` and `rgw_max_concurrent_requests = 1024`, plus a daemon restart. Not visible in current config diff. Has this been applied?       |
| 7 | LUKS posture on NVMe drives | Covered in separate follow-up correspondence; mentioned here for completeness.                                                                                                         |

Thanks,

Rohn

---

## Internal tracking notes (not part of the email body)

- **Subject of email:** Cover for the attached vendor-facing audit findings HTML (`proxmox_audit_findings_to_ksolves_2026-05-08.html`)
- **What this email body does:** introduces the attachment, summarises the green-light findings, lists the 7 verification items as a quick-look table. Full context for each item is in § 13 of the attached HTML.
- **Pairs with:**
  - Vendor-facing audit detail: `correspondence/Document/proxmox_audit_findings_to_ksolves_2026-05-08.md` (HTML rendering attached to the email)
  - Internal version: `phases/phase2/development/Notes/proxmox_audit_2026-05-08.md` (with internal tracking codes; not for sending)
  - Phase 2 closing letter: `correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md`
  - H1 javax filter letter: `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md`
  - NVMe LUKS follow-up: `correspondence/Document/nvme_luks_already_encrypted_followup_to_ksolves_2026-05-08.md`
- **Format note:** the table uses Markdown pipe syntax. Most modern email clients render this cleanly when the message is sent as plain text (the pipes line up visually). If a particular client renders it poorly, the items can be flattened to a numbered list with **bold** topic labels — same content, different formatting.
- **Substitution before send:** replace `[Ksolves lead]` with the actual recipient name, and confirm the CC line matches your current convention. The `corp.fqdn` placeholder can be substituted with the real corporate FQDN if useful (the vendor has access to the actual hosts and knows the FQDN, but their copy of the audit will look more natural with the real domain).
