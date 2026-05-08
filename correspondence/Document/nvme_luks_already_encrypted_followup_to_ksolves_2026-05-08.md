**Status:** Sent 2026-05-08 — written follow-up to the verbal already-given; awaiting vendor confirmation
**From:** Rohn (fqdn)
**To:** vendor lead (Ksolves)
**CC:** Murali (per existing vendor-correspondence convention)
**Date:** 2026-05-08
**Subject:** Written confirmation: NVMe scratch drives are LUKS-encrypted — please do not reformat

---

Hi [vendor lead],

Following up in writing on what we discussed verbally regarding the NVMe scratch drive encryption posture.

## Confirmation

The **four NVMe scratch drives per dev cluster node** (drives 4–7 on each of msb-pmc03-01 / -02 / -03) are **already LUKS-encrypted** by fqdn before the Spark deployment work began. The drives themselves are hardware-encrypted from the OEM, and we've established the LUKS layer on top. The encryption posture is in place and verified.

The vendor configuration document (`Ksolves_Spark_YARN_Config_v1.0.pdf` § 8.2) calls for LUKS encryption at the OS level on these drives as part of the HIPAA data-at-rest pillar — that's done.

## Action requested

Please ensure that the Spark / YARN install process **does not reformat, re-encrypt, or otherwise modify** the existing LUKS posture on these drives. Specifically:

- **Do not** run `cryptsetup luksFormat` on drives 4–7
- **Do not** run `mkfs.xfs` / `mkfs.ext4` on these drives without first preserving the existing LUKS volume
- **Do** mount the existing LUKS volumes via `cryptsetup luksOpen` if needed for the install workflow

If the install procedure includes a step that touches these drives (mount / format / encrypt), please flag it ahead of time so we can coordinate. We'd rather catch it before execution than recover from an accidental reformat.

## Tracking

This pairs with our internal BLOCKER.3a (HIPAA Hardware Compliance) tracking — the LUKS posture is the foundation for that sub-gate.

Thanks,

Rohn

---

## Internal tracking notes (not part of the email body)

- **Subject of letter:** Written confirmation that NVMe drives are already LUKS-encrypted — item 14 from the 2026-05-08 review punch-list. The verbal was given earlier; this is the written follow-up.
- **Cross-references:**
  - Main CP — `phases/phase2/development/Document/Phases_Critical_Path_Development_v1.5.md` § BLOCKER.3a (HIPAA Hardware Compliance)
  - HIPAA sub-project — `phases/phase2/development/Document/CP_HIPAA_Compliance_v1.0.md`
  - Vendor configuration document — `phases/phase2/development/Document/Ksolves_Spark_YARN_Config_v1.0.pdf` § 8.2
- **Companion letters from same review punch-list:**
  - `correspondence/Document/phase2_closing_letter_to_ksolves_2026-05-08.md` (Phase 2 closure verification — also covers LUKS software question)
  - `correspondence/Document/h1_javax_filter_verification_letter_to_ksolves_2026-05-08.md` (§ 8.3 javax filter ownership)
- **Note on overlap with the Phase 2 closing letter:** the Phase 2 closing letter asks the question "was software LUKS applied on top of hardware encryption?". This letter takes the *opposite direction* — instructing the vendor not to disturb existing LUKS — so they should be sent as separate communications. The Phase 2 closing letter asks "what did you do?"; this letter says "don't do anything more."
