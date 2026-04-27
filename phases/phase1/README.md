# Phase 1 — Infrastructure Sizing & Configuration

Coordination point for Phase 1 deliverables across all project contexts (calculators, remote_services, security, correspondence).

## Directory Structure

- **`planning/`** — Phase 1 specifications, requirements, timeline, dependencies
- **`deliverables/`** — Final Phase 1 outputs (models, sizing docs, deployment guides)
- **`vendor_comms/`** — Vendor communications, RFQs, quotes, vendor responses specific to Phase 1
- **`research/`** — Supporting research, analysis, architecture diagrams, benchmark data

## Phase 1 Scope

See `TODO.md` for current Phase 1 tasks tagged `[Phase1]`. Priority levels:

- **P0 (Critical Path)** — Tasks blocking Phase 1 validation (cloud staging target, RHEL subscriptions, Hadoop install, shuffle factor measurement)
- **P1 (Phase 1 Support)** — Deployment tasks and infrastructure components required for Phase 1 operations

## Ksolves Remote Access — Phased Deployment

Phase 1 infrastructure provisioning by Ksolves depends on establishing remote access to both Proxmox clusters. Two phases:

**Phase 1A (Interim) — Shared Webex Desktop**
- Immediate deployment (no dependencies)
- fqdn infrastructure team shares Webex desktop with Ksolves
- Ksolves executes infrastructure provisioning under fqdn team oversight
- Provides audit trail via Webex recording
- **Ksolves can begin Phase 1 work immediately via this path**

**Phase 1B (Permanent) — VMware Horizon Desktop**
- Two dedicated Horizon desktops provisioned for Ksolves
- Requires fqdn Horizons Teams infrastructure setup
- Requires fqdn Cyber Security approval (in parallel, does not block Phase 1A)
- Estimated 2–4 weeks after security approval
- Phase 1A continues until Horizon is live

See `Ready_For_Review/Phases_Critical_Path_v1.0.md` § BLOCKER.1 for full access strategy and dependencies.

## Daily Coordination

Phase 1 items appear at the top of the daily TODO email for quick status review.
