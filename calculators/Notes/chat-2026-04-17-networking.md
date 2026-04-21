# Networking Discussion — 2026-04-17

## Context

Continuation of storage architecture and networking analysis for the 3-node dev Spark/Ceph cluster
(HPE DL385 Gen11, 32c/384GB/7×3.84TB NVMe per node). Discussion centers on feasibility of
remote CSV staging from a production Ceph cluster over the existing network fabric.

---

**Q: What is an ISL?**

**Inter-Switch Link** — a direct cable connecting two switches to each other, bypassing the core
router entirely.

In this context: a fiber or DAC cable running directly from the dev rack's top-of-rack switch pair
to the production rack's top-of-rack switch pair. Traffic between the two clusters would traverse
that dedicated link rather than going up to the core router and back down, avoiding contention with
general DC traffic on the trunk uplinks.

---

**Q: We have a vPC peer link between the switches.**

A vPC (Virtual Port Channel) peer link is a direct physical connection between the two switches in
a vPC pair. It carries:

- vPC control plane synchronization traffic
- BUM traffic (broadcast, unknown unicast, multicast)
- Orphan port failover traffic

**It is not a general-purpose data path.** Routing sustained bulk inter-cluster data over the vPC
peer link risks saturating it and destabilizing vPC operation.

### Questions raised for the network engineer

1. What is the speed of the vPC peer link — 40G, 100G, a port-channel of multiple links?
2. What is its current utilization?
3. Is there policy against using it for inter-cluster data traffic, or can a separate non-vPC ISL
   be added alongside it?

---

**Q: The peer-link is dual 25 Gb/s.**

- Aggregate bandwidth: **50 Gbps**
- At current 10G server NICs: 3 nodes × 10G = 30G demand — peer link has headroom
- If upgraded to 25G NICs: 3 nodes × 25G = 75G demand > 50G peer link — peer link saturated

Cisco does not recommend using the vPC peer link for sustained bulk data flows regardless of
headroom. A separate dedicated ISL alongside it would be the clean solution.

---

**Q: Scratch will not be on the remote CephFS cluster — it will be local to the nodes.**

Confirmed — scratch drives (NVMe local to each node, `spark.local.dir`) are always local. The
remote CephFS/S3 discussion applied only to the **raw ingest CSV read path**. Spark shuffle
intermediates never traverse the network.

The remote staging architecture under discussion was:

- **Remote Ceph (other rack):** holds ingest CSV — Spark reads it over the network
- **Local NVMe scratch:** shuffle intermediates — always local, unaffected
- **Local Ceph (same nodes):** Parquet output — written locally after processing

---

**Q: What does this mean — "Viable path — brings read time to ~12 min; still shared with shuffle"?**

That language was imprecise. Correction:

Shuffle traffic is **local** — it moves between executors within the same cluster over the local
switch. It does not use the inter-rack link at all. The correct statement should have been:

> **25G upgrade:** brings remote CSV read time to ~12 min; inter-rack link shared with **general
> DC traffic**, not with Spark shuffle.

---

**Q: Please reoutput the net assessment table with the clarification on shuffle.**

## Net Assessment — Remote CSV Staging Options

| Option | Status |
|---|---|
| Remote CSV staging at 10G | Non-starter — ~31 min/node read time, inter-rack link shared with general DC traffic |
| Upgrade to 25G (SFP28 DAC procurement) | Viable path — brings read time to ~12 min; inter-rack link shared with general DC traffic only (shuffle is local, does not use this path) |
| Direct ISL between ToR switch pairs | Depends on policy approval and QSFP28 procurement — dedicates a link to inter-cluster traffic, eliminating DC trunk contention |
| Cross-rack via core router at 100G | Possible but shared trunk — needs QoS reservation |
| RoCE v2 RDMA | Not usable without SR-IOV or PCIe passthrough reconfiguration on Proxmox |

---

**Q: Can you describe a topology that works? What would we need.**

Everything faster than current requires breaking the 100G northbound ceiling. Three paths:

### Option 1 — More Northbound Uplinks (lowest disruption)
Add additional 100G links between each N9300 access pair and the N9300 core, bundled into a larger
port-channel.

- 2×100G = 200G northbound → 5 TB in ~4 min
- 4×100G = 400G northbound → 5 TB in ~2 min
- **Requires:** available ports on both the access N9300s and core N9300, plus 100G QSFP28
  optics/DAC cables
- Shares bandwidth with other cluster traffic — still needs QoS

### Option 2 — Direct ISL Between Access N9300 Pairs (cleanest)
A dedicated link between the two rack switch pairs, bypassing the N9300 core entirely for
inter-cluster storage traffic.

- 100G dedicated ISL → 5 TB in ~7 min, **no contention**
- 400G dedicated ISL → 5 TB in ~2 min
- **Requires:** fiber run between racks, available QSFP28 ports on both pairs, optics, policy
  approval

### Option 3 — Dedicated Out-of-Band Storage Network (most robust, most expensive)
Separate NICs on each node connected to a dedicated storage switch fabric, completely independent
of the production network.

- No contention with DC traffic ever
- **Requires:** additional NICs, dedicated switches, separate cabling

### What to ask the network engineer

| Question | Why it matters |
|---|---|
| Exact N9300 model | Determines available port types and speeds |
| Available free ports on each access pair and core | Determines whether Option 1 is possible without new hardware |
| Policy on direct ISL between rack switch pairs | Determines whether Option 2 is permitted |
| Available 100G/400G QSFP28 optics in inventory | Determines procurement needs |

### Reality check
All three options assume remote CSV staging is worth the infrastructure investment. At 5 TB dev
ingest with CSV deleted after verify, **local ingest** (data delivered directly to local Ceph)
sidesteps this entire problem with no network upgrades required.

---

**Q: What if we had dual 25 Gb/s fiber from the nodes to the switch on the Spark cluster nodes?**

The BCM57414 already has two SFP28 ports — dual 25G means **bonding both ports via LACP**,
giving 50G per node.

| Config | Per-node bandwidth | Cluster aggregate | Northbound ceiling | Effective bandwidth | 5 TB read time |
|---|---|---|---|---|---|
| Current (10G single) | 10G | 30G | 100G | 30G | ~31 min |
| Single 25G upgrade | 25G | 75G | 100G | 75G | ~9 min |
| **Dual 25G bonded** | **50G** | **150G** | **100G** | **100G** | **~7 min** |

The dual 25G bond saturates the N9300 northbound uplink — 100G becomes the ceiling.

**Two caveats:**

1. **LACP and parallel flows:** LACP hashes individual TCP flows to one link or the other. Spark's
   S3A connector makes multiple parallel range requests, distributing across both links naturally —
   realistically approaches 50G per node.
2. **Uplink saturation:** At 100G you're consuming the entire northbound uplink. QoS becomes
   essential — without it, inter-cluster CSV reads starve everything else during the job.

**What you'd need:**
- 25G SFP28 DACs or SR optics on both ports of every dev cluster node (6 cables)
- Same on production Ceph nodes serving the data (6 cables)
- QoS reservation on the N9300 core
- LACP bond configuration on dev cluster nodes

---

**Q: The switches' northbound link to the N9300 core is 100 Gb/s aggregate.**

This confirms the hard ceiling. The inter-cluster path traverses **two** 100G northbound links —
one on each side:

```
Dev Spark nodes                          Prod Ceph nodes
     |                                        |
Dev N9300 pair                          Prod N9300 pair
     |                                        |
  100G northbound                        100G northbound
     |                                        |
     +------------- N9300 Core ---------------+
```

CSV reads flow through both northbound links. Each is shared with all other traffic from its
cluster.

- **Hard ceiling:** 100G — cannot be exceeded regardless of NIC speed or bonding
- **Realistic available bandwidth:** less than 100G once other cluster traffic is accounted for
- **Dual 25G bonding benefit:** marginal — shifts bottleneck from NIC to uplink, saves ~2 min

### Revised read time table

| Config | Cluster aggregate | Northbound ceiling | Realistic effective (w/ QoS) | 5 TB read time |
|---|---|---|---|---|
| Current 10G | 30G | 100G | ~30G | ~31 min |
| Single 25G | 75G | 100G | ~70G | ~10 min |
| Dual 25G bonded | 150G | 100G | ~90G | ~8 min |

---

**Q: What would faster require?**

Everything faster requires breaking the 100G northbound ceiling. Three paths:

### Option 1 — More Northbound Uplinks
- 2×100G = 200G → 5 TB in ~4 min
- 4×100G = 400G → 5 TB in ~2 min
- Still shared with DC traffic — QoS required

### Option 2 — Direct ISL Between Access N9300 Pairs
- 100G dedicated → 5 TB in ~7 min, no contention
- 400G dedicated → 5 TB in ~2 min
- Requires fiber between racks, policy approval, QSFP28 procurement

### Option 3 — Dedicated Out-of-Band Storage Network
- Fully isolated — no contention ever
- Highest cost and complexity

---

**Q: What would be required cable and ports for the ISL link?**

### Ports Required

| ISL Configuration | Ports per pair | Total ports | Bandwidth |
|---|---|---|---|
| Single link (non-redundant) | 1 port on one switch | 2 ports total | 100G |
| Dual link (redundant port-channel) | 1 port per switch in the pair | 4 ports total | 200G |

Port type: **QSFP28 (100G)**. Redundant dual-link recommended — survives single switch failure.

### Cable Type by Rack-to-Rack Distance

| Distance | Cable type | Notes |
|---|---|---|
| ≤ 3m | 100G QSFP28 passive DAC | Cheapest, no optics needed |
| 3–7m | 100G QSFP28 active DAC | Slightly more expensive |
| 7–100m | 100G QSFP28 SR4 + multimode fiber (OM3/OM4) | Requires optics at each end |
| > 100m | 100G QSFP28 LR4 + single-mode fiber | Unlikely for same DC |

### Minimum Procurement (single non-redundant ISL)
- 2× available QSFP28 ports (one per pair)
- 1× 100G DAC cable (≤7m) or 1× fiber run + 2× SR4 QSFP28 optics (>7m)

### Recommended Procurement (redundant 200G ISL)
- 4× available QSFP28 ports (one per switch in each pair)
- 2× 100G DAC cables or 2× fiber runs + 4× SR4 optics

---

**Q: For clarification — if we move both clusters to the same N9300 pair, do we still need the ISL?**

No. If both clusters connect to the **same N9300 access pair**, inter-cluster traffic never leaves
the switch — it switches locally at line rate.

```
Dev Nodes (3x)     Prod Nodes (3x)
      |                   |
      +---- N9300 pair ---+         ← single access pair, both clusters
                 |
           100G northbound
                 |
            N9300 Core
```

- **No ISL needed**
- **No northbound bandwidth consumed** for inter-cluster traffic
- **Latency:** one switch hop vs up/across core/back down
- **Effective inter-cluster bandwidth:** N9300 switching fabric (far exceeds 100G)

Key questions:
| Question | Why it matters |
|---|---|
| Does the N9300 pair have enough free ports for both clusters? | 6 additional server connections needed |
| Are existing SFPs 10G or 25G? | May still want 25G upgrade for throughput |
| Is there a policy/operational reason clusters are on separate pairs today? | Failure domain separation, VLAN isolation, etc. |

---

**Q: What is the count and type of ports we require for the switches?**

### Server-Facing Downlink Ports (SFP28, 10G/25G capable)

| Cluster | Nodes | Ports/node | Total SFP28 ports |
|---|---|---|---|
| Production | 3 | 1 (current) | 3 |
| Development | 3 | 1 (current) | 3 |
| **Single port per node total** | | | **6** |
| Production | 3 | 2 (bonded) | 6 |
| Development | 3 | 2 (bonded) | 6 |
| **Dual port bonded total** | | | **12** |

### Switch Infrastructure Ports (existing, already in use)

| Purpose | Type | Count | Notes |
|---|---|---|---|
| vPC peer link | SFP28 25G | 4 total (2 per switch) | Confirmed dual 25G, already in use |
| Northbound to core | QSFP28 100G | TBD | Already in use — engineer to confirm count |

### Questions for Network Engineer
1. Exact N9300 model — determines total port count and types available
2. How many SFP28 ports are currently free after existing connections
3. Rack-to-rack distance (for ISL cable type if ISL route is chosen)
4. Policy on direct ISL or consolidating both clusters onto one switch pair

---

**Q: I just learned the N9200s are actually N9300s. And when you say "exact model" — isn't N9200 and N9300 sufficient?**

Good correction — both layers are now confirmed as N9300s. Updated topology:

```
Dev Nodes          Prod Nodes
    |                   |
N9300 pair A       N9300 pair B   ← access layer
    |                   |
    +---- N9300 Core ---+          ← core layer
```

On "exact model": the **N9300 is a product family**, not a single switch. The specific model
number determines everything that matters for port planning:

| Model | Downlink ports | Uplink ports |
|---|---|---|
| C9348GC-FXP | 48× 1/10G SFP+ | 4× 100G QSFP28 |
| C9372PX | 48× 10G SFP+ | 6× 40G QSFP+ |
| C9364C | 64× 100G QSFP28 | — (all same) |
| C9336C-FX2 | 36× 40/100G QSFP28 | — (all same) |

The full model number (format: **N9K-C93xxX**) is on a label on the front or rear of the switch.
That is what the network engineer needs to look up.

---

## Open Items

- [ ] Network engineer to confirm exact N9300 access switch model (label on front/rear of switch)
- [ ] Network engineer to confirm available free port count on each access N9300 pair
- [ ] Network engineer to confirm rack-to-rack distance (for ISL cable selection)
- [ ] Policy decision: is a direct ISL between the two access N9300 pairs permitted?
- [ ] Decision: move both clusters to same N9300 pair (eliminates ISL need entirely)?
- [ ] Procurement: 25G SFP28 DAC/optics if NIC upgrade proceeds (not currently in inventory)
