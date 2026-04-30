# Vendor Query — Network, Firewall, and DNS Requirements

**To:** Ksolves
**From:** Rohn Wood
**Date:** 2026-04-30
**Subject:** Network, firewall, and DNS requirements for msb-pmc01 / msb-pmc02 / msb-pmc03 deployment — vendor assumptions and scope

---

Hi [Vendor contact],

As we plan our on-site network and security configuration, we want to capture your assumptions and requirements across the full deployment scope before we finalize switch, VLAN, firewall, and DNS configurations. The network fabric and security perimeter are on our side, so anything your provisioning assumes about reachability needs to be made explicit so we can build the corresponding policies. We'd rather over-document this now than discover a blocked path during cutover.

For reference, the in-scope infrastructure is:

- **msb-pmc01** — **4-node** Proxmox hyperconverged cluster hosting Airflow, Nginx, Ansible, and supporting services. Airflow on this cluster orchestrates **both** the development and production Spark environments.
- **msb-pmc02** — 3-node Proxmox hyperconverged cluster reserved for the future Spark **production** environment (YARN, Spark, Ceph, RGW S3, Spark History Server).
- **msb-pmc03** — 3-node Proxmox hyperconverged cluster hosting the Spark **development** environment (YARN, Spark, Ceph, RGW S3, Spark History Server).
- **Office / user network** — endpoints reaching the Airflow UI and bastion.
- **Azure cloud object storage** — two separate destination buckets (one for dev, one for prod), populated by per-cluster Stage-2 batch Spark jobs. Snowflake reads from these Azure buckets via external stage; **Snowflake has no direct connection to either on-premises cluster.**

**Data flow (per environment):**

1. The primary Spark ETL job on msb-pmc02 (or msb-pmc03) writes to the **local** Ceph RGW (S3 GW) on the same cluster, into a **local S3 bucket**.
2. A **separate Spark batch job on the same cluster** reads the local bucket and writes the data to the **per-environment Azure cloud bucket** (prod bucket for msb-pmc02, dev bucket for msb-pmc03).
3. Snowflake queries the Azure cloud bucket directly, independently of the on-prem clusters.

**Critical security constraints:**

- msb-pmc02 (production) and msb-pmc03 (development) **must not communicate with each other** at L2 or L3.
- The connectivity model is hub-and-spoke through msb-pmc01:
  - msb-pmc01 ↔ msb-pmc02 — allowed (orchestration of prod)
  - msb-pmc01 ↔ msb-pmc03 — allowed (orchestration of dev)
  - msb-pmc02 ↔ msb-pmc03 — denied
  - msb-pmc02 → Azure prod cloud bucket — allowed (Stage-2 batch egress)
  - msb-pmc03 → Azure dev cloud bucket — allowed (Stage-2 batch egress)

Please confirm your design honors this, and call out any assumed connection that would break it.

Could you confirm or fill in the following:

## 1. Services and footprint on each cluster

- **msb-pmc01:** We have on record Airflow (scheduler, webserver, workers), Nginx, and Ansible. Please list everything else your provisioning installs here — metadata DB (Postgres/MySQL), Celery broker (Redis/RabbitMQ), metrics/log shipper, monitoring agents, DAG-sync, secrets store, etc.
- **msb-pmc03 (development):** We expect YARN ResourceManager / NodeManagers, Spark workers (including the Stage-2 batch sync workload), Ceph (OSDs, MONs, RGW), Spark History Server. Please confirm and list anything additional, plus which VMs / nodes host each role.
- **msb-pmc02 (future production):** Will the production footprint mirror development, or are there services that exist only in production (separate metadata DB, Hive Metastore, dedicated monitoring, secrets manager)? Please specify.

## 2. Inter-cluster connections from msb-pmc01

Because Airflow orchestrates both clusters, we expect **the same access matrix** from msb-pmc01 to apply to both msb-pmc02 (prod) and msb-pmc03 (dev), with each cluster receiving identical but separate ACL entries. For each path below, please list source service, destination, protocol, and port — and confirm whether the requirement is symmetric across dev and prod or differs in any way:

- Airflow scheduler → YARN ResourceManager (default 8032)?
- Airflow → Ceph RGW S3 endpoint — VIP, DNS name, or per-node IPs? Port 443 TLS or 80?
- Airflow / Nginx → Spark History Server (default 18080)?
- Ansible → Proxmox host SSH on cluster nodes — which user, key-based, port?
- Ansible → VM-level SSH — which subnets / VMs are in scope?
- Any direct OSD or MON traffic from msb-pmc01? (We expect "no, only via RGW" — please confirm.)
- Any callbacks from msb-pmc02 or msb-pmc03 → msb-pmc01 (Spark driver logs, metrics push, status webhooks, Airflow callbacks)?

## 3. Intra-cluster on msb-pmc02 and msb-pmc03

For each Spark cluster:

- Ceph public network and Ceph cluster (private) network — confirm subnets and which traffic each carries.
- Spark shuffle traffic between YARN NodeManagers — flat within the cluster, or do you assume any segmentation?
- YARN RPC / heartbeats — any non-default ports?
- Internal connectivity between the primary Spark ETL workload and the Stage-2 batch sync workload (whether they run as separate Spark applications under the same YARN, separate YARN queues, or otherwise) — please describe.
- Will the dev and prod clusters use **identical IP ranges** (mirrored), **distinct ranges**, or overlapping ranges with NAT? This affects how we implement dev/prod isolation at the network layer.

## 4. Office / user network and bastion access

- Office → Nginx on msb-pmc01 (443) — confirmed?
- Office → bastion → cluster SSH — which bastion host, which subnets does it gate, does it gate dev and prod separately?
- Any other inbound paths from the office network to any of the three clusters that your design assumes?

## 5. Outbound egress to Azure cloud storage

For each Spark cluster (msb-pmc02 and msb-pmc03), the Stage-2 batch Spark job egresses to a per-environment Azure cloud bucket. Please specify:

- **Endpoints:** Azure storage account FQDN(s), container names, port (443), and whether you use the native Azure ABFS/WASBS SDK or an S3-compatible API endpoint.
- **Authentication method:** SAS tokens, service principal, managed identity, or storage account keys? Where are the credentials provisioned and rotated?
- **Source IP / SNAT:** What source IP does your design assume each cluster egresses from? Single SNAT'd IP, per-VM addresses, or a mobile gateway IP? This is critical for any IP allow-listing on the Azure side.
- **Azure-side IP allow-listing:** Do you assume the destination Azure storage accounts have an IP allow-list configured (and if so, what source IPs/ranges should we ensure are permitted), or are they open to public egress with auth-only?
- **Dev/prod separation:** Confirm that msb-pmc02 writes only to the prod Azure bucket and msb-pmc03 writes only to the dev Azure bucket, and that the credentials provisioned in each cluster scope only to its respective bucket.
- **msb-pmc01 → Azure:** Does Airflow on msb-pmc01 need any direct Azure access (for instance, polling either bucket to confirm Stage-2 completion, or writing audit/log artifacts)? If so, list endpoints and auth.
- **Other outbound from any cluster:** Internet access for package updates, vendor support tooling, telemetry, license-check destinations — please list explicitly.

## 6. Firewalling — explicit configuration vs. assumed environment

Please clarify both halves:

- **Explicit firewalling done by your provisioning:** Will your installation configure or enable any host-based firewall (firewalld, ufw, nftables/iptables) on any of the hosts or VMs across the three clusters? Will you set Proxmox firewall rules at the datacenter, node, or VM level? If yes, please share the rule sets or playbooks so we can review and reconcile with our network policy.
- **Assumed perimeter / inter-cluster firewall:** Does your design assume an existing firewall is already enforcing policy between any of the three clusters, between any cluster and the office network, between any cluster and Azure, or between dev and prod? If so, what specifically do you assume is already permitted? We need this list explicitly so we can verify our network configuration matches your assumptions before you begin.

If your model is "no firewalling configured on our side, customer handles all of it," that is also a fine answer — we just need it stated so we can scope our work accordingly.

## 7. Network topology assumptions

- Are you assuming a flat L2 network across all in-scope hosts/VMs, or are you designing for routed and/or segmented access?
- If segmented, which VLAN boundaries do you expect to traverse, and have you tested that path through a firewall in a representative environment?
- For msb-pmc02 and msb-pmc03 specifically: confirm the Ceph public and Ceph cluster networks are on separate VLANs/subnets, and identify which physical NICs/bonds carry each.

## 8. DNS and service discovery

This area needs a complete answer because we configure DNS on our side and need to align with whatever your provisioning expects:

- **Full hostname inventory:** Please provide the complete list of VM hostnames and their roles for **all three clusters** — Airflow VM, Nginx VM, Ansible host, YARN ResourceManager, NodeManagers, Ceph MONs, Ceph OSDs, RGW gateways, Spark History Server, and anything else your provisioning instantiates.
- **Naming convention:** What naming scheme do you follow (e.g., `<cluster>-<role>-<index>`)? This lets us predict naming for future expansion or replacement nodes.
- **Forward and reverse DNS:** Does your provisioning assume forward and reverse DNS records are already in place when you begin, or do you provision via static `/etc/hosts` entries on each host? If DNS is required, identify which records and zones must exist before cutover.
- **Dev/prod hostname conflicts:** If hostnames overlap between msb-pmc02 (prod) and msb-pmc03 (dev) — for example, both having a `spark-master-01` — how do you expect DNS to disambiguate them? Do you require split-horizon DNS, FQDN suffixes per cluster, or unique short names per cluster?
- **Resolver placement:** Where do you expect DNS resolvers to live, and which resolvers should each cluster point at?
- **Service registries:** Do any of your services use Consul, etcd, or a similar registry alongside or instead of DNS?

## 9. Bandwidth and latency expectations

- Peak and sustained throughput expected on each path: msb-pmc01 ↔ msb-pmc02, msb-pmc01 ↔ msb-pmc03, intra-cluster on each Spark cluster, and outbound from each Spark cluster to the corresponding Azure cloud bucket.
- Acceptable round-trip latency between Airflow and YARN, and between Spark workers and the local RGW S3 endpoint.
- We're on bonded 25 GbE on the cluster side, so we expect headroom, but please flag any latency-sensitive paths or jumbo-frame expectations.

## 10. Failure modes

If a connection is blocked at the network layer, how does each service surface the failure (timeout, retry, hard fail, silent backoff)? This will help us scope our cutover test plan and triage cleanly when something is misconfigured.

---

Thanks — once we have your answers, we'll lock down the VLAN design, the **combined ACL matrix** (covering inter-VLAN firewall rules, switch VLAN ACLs, and RGW S3 IAM/bucket policies), and the dev/prod isolation rules, and share them back to you for confirmation before we configure anything.

Rohn Wood
