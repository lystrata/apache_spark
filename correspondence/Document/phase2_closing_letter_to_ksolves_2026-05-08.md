**Status:** Sent 2026-05-08 — awaiting vendor response
**From:** Rohn (fqdn)
**To:** vendor lead (Ksolves)
**CC:** Murali (per existing vendor-correspondence convention)
**Date:** 2026-05-08
**Subject:** Phase 2 Closure — Verification Items

---

Hi [vendor lead],

Thank you for the work to date on Phase 2 of the deployment. Before I sign off on Phase 2 closure, I'd like to verify a few items so we're aligned on scope and on what's complete vs. what remains.

## 1. Phase 2 scope confirmation

The Ksolves SOW V1.0 § 5 lists Phase 2 as "Proxmox & VM Creation, 3 wks". On the dev cluster (msb-pmc03), my current understanding of the state is:

- **Proxmox base configuration** — complete
- **Ceph cluster bootstrap** (MON, MGR, 9× OSD, RGW; HEALTH_OK) — complete
- **Worker VM hardware containers** (3× GKPR-SPARK-WK-01/02/03; vCPU + RAM + NVMe attached) — complete
- **YARN RM VM provisioning** — please confirm status
- **Worker VM RHEL 9.4 OS install** + base config (network / SSH / passwordless sudo) — not yet started, per my read
- **Subscription registration on the running VMs** — pending OS install

Could you confirm the items you consider **in scope for Phase 2 closure** so we can verify them against the SOW outline and either sign off or identify what remains? Specifically: does Phase 2 in your framing end at VM hardware creation, or does it extend through OS install + base config?

## 2. HIPAA-under-Phase-2 framing

I understand from your update on 2026-05-08 that HIPAA compliance is **closed under Phase 2**. The vendor configuration document (`Ksolves_Spark_YARN_Config_v1.0.pdf` § 8) enumerates three pillars:

- § 8.1 — Transmission security (TLS, Spark RPC encryption, SSL on Web UIs)
- § 8.2 — Data at rest (LUKS, drive-level encryption, server-side encryption on Ceph buckets)
- § 8.3 — Web UI access control (custom javax servlet filter)

Could you clarify which of these your "Phase 2 HIPAA closed" claim covers?

- Does it refer specifically to **§ 8.2 only** (drive-level encryption / LUKS posture) — i.e., hardware-level compliance?
- Or does it cover the **full three-pillar scope** including TLS, Spark RPC encryption, SSL on Web UIs, and the custom javax servlet filter referenced in § 8.3?

We've split our internal BLOCKER.3 tracking into **3a (hardware compliance — drive encryption / LUKS posture)** and **3b (software & network compliance — Spark RPC / TLS / SSL / Web UI ACL / javax filter)** so we can track these separately. Knowing which sub-gate(s) your "Phase 2 HIPAA closed" claim covers lets us reconcile the two views and update our tracking accordingly.

## 3. LUKS software on already-hardware-encrypted drives

Our NVMe scratch drives (drives 4–7 per node) are **already hardware-encrypted from the OEM** and were LUKS-prepared by fqdn before the Spark deployment work began. The vendor configuration document § 8.2 calls for LUKS at the OS level on these drives. Could you confirm:

1. Was **software LUKS applied** on top of the existing hardware encryption during the install?
2. If yes, what are the **implications for stability and CPU performance overhead** from double-encryption (hardware + software LUKS)?
3. What command(s) do you recommend we run to **verify the current LUKS / dm-crypt state** on each drive? Examples we'd consider:
   - `cryptsetup status <device>`
   - `lsblk -o NAME,FSTYPE,MOUNTPOINT,SIZE,TYPE` (look for `crypt` type entries)
   - `dmsetup ls` / `dmsetup info`
4. If software LUKS was applied **on top** of hardware encryption, do you recommend leaving it (defense in depth) or removing it (reduce overhead since the drives are already protected at the hardware level)?

Proxmox is reporting healthy so far, but we want to assess the operational posture before signing off on hardware-level HIPAA compliance (BLOCKER.3a in our tracking).

## Closing

Once we have your responses on the three items above, we can either close out Phase 2 cleanly or capture the remaining gap as a Phase 2 follow-up. Either is fine — the priority is alignment.

Thanks,

Rohn

---

## Internal tracking notes (not part of the email body)

- **Subject of letter:** Phase 2 closure verification — items 10 + 11 from the 2026-05-08 review punch-list
- **Cross-references:**
  - Main CP — `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md` § BLOCKER.3 (split 2026-05-08 into 3a + 3b)
  - HIPAA sub-project — `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md`
  - Vendor configuration document — `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` § 8
- **Pairs with:** `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md` (separate letter on § 8.3 javax filter ownership)
- **Action items captured separately:** verbal NVMe LUKS notification follow-up email at `correspondence/Document/nvme_luks_already_encrypted_followup_to_ksolves_2026-05-08.md`
