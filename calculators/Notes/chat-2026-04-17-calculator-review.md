# Spark Calculator Mathematical Review — 2026-04-17

## Context

Third-party mathematical review of the Spark sizing calculators was submitted for verification.
Each issue was researched against the actual calculator source code
(`development_spark_calculator.html` and `production_spark_calculator.html`) before findings
were issued.

---

## Confirmed Correct (reviewer agrees, verified against code)

**Q: Are the core executor formulas correct?**

All three core formulas verified correct and consistently applied:

- **Executor Memory Model:** `MAX_EXEC_MEM = (SLOT_GB - OFFHEAP) / (1 + OVH_PCT)` with 5% safety margin
- **Executor Density:** `EXEC_PER_VM = floor((VCPU_VM - 2) / EXEC_CORES)` — correctly reserves 2 vCPUs for NodeManager + OS
- **Total Executor Count:** `TOTAL_EXEC = max(1, EXEC_PER_VM * TOTAL_VMS - 1)` — correct -1 for YARN cluster-mode driver

---

## Issue 1: Blast Radius Calculation — **Disagree with reviewer**

**Q: The reviewer claims `100 / TOTAL_EXEC` is inverted and should be labeled "Per-Executor Impact."**

**Code:** `const BLAST_PCT = TOTAL_EXEC > 0 ? 100 / TOTAL_EXEC : 100;`

The reviewer states "blast radius typically means cluster data loss." That is not the standard
definition in distributed systems. Blast radius of an executor failure = percentage of total
cluster compute capacity lost when one executor dies. With 12 executors, losing one = 8.3% of
capacity — that IS the blast radius, correctly calculated and correctly labeled.

**Finding: No issue. Reviewer's definition was incorrect.**
**Action: None.**

---

## Issue 2: OOM Threshold Logic — **Partially valid**

**Q: The reviewer says the thresholds (4, 5, 6 GB) are arbitrary and undocumented.**

**Code:**
```js
const OOM_THRESHOLD = SKEW_PROFILE === 'heavy' ? 6 : SKEW_PROFILE === 'moderate' ? 5 : 4;
```

The values are not arbitrary — they represent the minimum headroom needed to absorb task-level
memory spikes from skewed partitions (Parquet read buffer + sort buffer + spill buffer all in
flight simultaneously under skew). However, the reviewer is correct that they were undocumented
in code comments.

**Finding: Logic is correct. Documentation was missing.**
**Action: Expanded inline comments added to both calculators explaining the 4/5/6 GB basis.**

### Comments added (both calculators):
```js
// OOM threshold: minimum safe executor slot headroom to absorb task-level memory spikes from data skew.
// Uniform (4 GB): tasks near average partition size — standard Parquet read buffer + overhead.
// Moderate (5 GB): occasional oversized partitions — Parquet read buffer + sort buffer + spill can spike simultaneously.
// Heavy (6 GB): frequent outsized partitions — full Parquet stripe + multiple concurrent spill buffers in flight.
const OOM_THRESHOLD = SKEW_PROFILE === 'heavy' ? 6 : SKEW_PROFILE === 'moderate' ? 5 : 4;
```

---

## Issue 3: Join Scratch Factor — **Partially valid**

**Q: The reviewer says the multipliers (1.0, 1.1, 1.25) are not justified and don't account for join selectivity.**

**Code:**
```js
const JOIN_SCRATCH_FACTOR = JOIN_TYPE === 'wide' ? 1.25 : JOIN_TYPE === 'mixed' ? 1.1 : 1.0;
```

The reviewer's concern about broadcast joins is already handled — `broadcast` type correctly gets
1.0, reflecting that broadcast joins generate no shuffle materialization. The multipliers are
engineering estimates for planning purposes, not empirically derived, but are reasonable and
conservative. They were undocumented.

**Finding: Logic is correct. Documentation was missing.**
**Action: Expanded inline comments added to both calculators explaining each multiplier.**

### Comments added (both calculators):
```js
// Join scratch factor: additional scratch multiplier applied on top of base shuffle volume (DAILY_TB × SHUF_AMP).
// Broadcast (1.0): small table broadcast to all nodes — no shuffle data materialized on scratch.
// Mixed (1.1): blend of broadcast and sort-merge; repartition/coalesce ops add ~10% intermediate data.
// Wide (1.25): multi-table sort-merge shuffles materialize intermediate join keys — ~25% additional scratch.
const JOIN_SCRATCH_FACTOR = JOIN_TYPE === 'wide' ? 1.25 : JOIN_TYPE === 'mixed' ? 1.1 : 1.0;
```

---

## Issue 4: Service Amortization Using ceil() — **Valid, acceptable by design**

**Q: The reviewer says ceil() over-reserves resources for small services across 3 nodes.**

**Code:** `const SVC_CORES_NODE = Math.ceil(SVC_CORES / NODES);`

The over-reservation is real. With NODES=3:
- YARN RM alone (2c): `ceil(2/3) = 1` → 3 cores reserved vs 2 needed (+1 over-reserved)
- YARN RM + Airflow (4c): `ceil(4/3) = 2` → 6 cores reserved vs 4 needed (+2 over-reserved)

Maximum over-reservation is 2 cores out of 32 per node (~6%). The reviewer's suggested fix
(pinning services to a specific node) does not fit the calculator's per-node abstraction model.
For a sizing tool, conservative over-reservation is preferable to under-reservation.

**Finding: Behavior is intentionally conservative. Magnitude is small and acceptable.**
**Action: None.**

---

## Issue 5: TARGET_OUT_MB = 150 — **Disagree with reviewer**

**Q: The reviewer says 150 MB is too small for Snowflake COPY INTO.**

**Code:** `const TARGET_OUT_MB = 150;`

Snowflake's documentation recommends **100–250 MB** per file for optimal COPY INTO performance.
150 MB is squarely in the middle of that range, not on the low end as the reviewer claims.

**Finding: No issue. Reviewer's claim was incorrect.**
**Action: None.**

---

## Issue 6: Network Bottleneck Uses Simple min() — **Valid simplification, appropriate for scope**

**Q: The reviewer says flat 80% utilization is wrong for WAN and missing TCP/MTU effects.**

**Code:**
```js
const BOTTLENECK_G = Math.min(AGG_NODE_G, NET_SWITCH_G, NET_WAN_G);
const UTIL         = 0.80;
const EFF_GBPS     = BOTTLENECK_G * UTIL;
```

For LAN, 80% is conservative (achievable and common). For WAN at high latency, 80% may be
optimistic. However, this calculator is a cluster sizing tool, not a network modeling tool.
The simplification is appropriate for planning-level estimates.

**Finding: Valid simplification for tool scope. Not a correctness issue.**
**Action: None. A LAN/WAN profile selector could be a future enhancement if the network section expands.**

---

## Issue 7: Ceph Retention Doesn't Account for Compaction — **Disagree with reviewer**

**Q: The reviewer says CEPH_DAYS assumes all data stays in Ceph with no aged-off data.**

**Code (original):** `const CEPH_DAYS = CEPH_USABLE / DAILY_TB;`

The reviewer misunderstands the metric. `CEPH_DAYS` is a **capacity headroom indicator** —
how many days of ingest volume the Ceph cluster could theoretically hold. It is not a retention
counter. The warning at `< 3 days` serves as a minimum planning margin check, which remains
valid regardless of actual retention policy.

**Finding: No issue. Reviewer misunderstood the metric's purpose.**
**Action (original): None.**

> **⚑ Revised 2026-04-18** — The formula was subsequently updated (independent of the reviewer's
> critique) to account for architectural constraints confirmed after this review. See Revisions
> section below.

---

## Issue 8: Scratch Coverage Doesn't Validate Spill Duration — **Reviewer is incorrect**

**Q: The reviewer says "if 12 executors write shuffle concurrently, 1.5 TB scratch fills in seconds" and proposes a per-executor validation formula.**

**Code:**
```js
const scratchCoverage = (e.SCRATCH_TB_PER_VM / (e.DAILY_TB * e.SHUF_AMP)) * 100;
```

The reviewer conflates **throughput** with **capacity**. Scratch sizing is a capacity question.
The total shuffle data written equals `DAILY_TB × SHUF_AMP` regardless of how many executors
write it concurrently. Executor count affects write rate, not total volume needed.

The reviewer's proposed formula is mathematically equivalent to the existing check when expanded:
```
SCRATCH_TB_PER_VM / TOTAL_EXEC > (DAILY_TB × SHUF_AMP) / TOTAL_EXEC
→ SCRATCH_TB_PER_VM > DAILY_TB × SHUF_AMP
```
This is exactly what the existing check does, plus the JOIN_SCRATCH_FACTOR and 0.75 safety margin.

**Finding: Existing formula is correct. Reviewer's logic was flawed.**
**Action: None.**

---

## Summary

| Issue | Reviewer Verdict | Actual Finding | Action Taken |
|---|---|---|---|
| Executor memory allocation | ✅ Correct | ✅ Confirmed | None |
| VM resource budgeting | ✅ Correct | ✅ Confirmed | None |
| Ceph capacity math | ✅ Correct | ✅ Confirmed (original) — formula revised 2026-04-18 | See Revisions |
| Blast radius naming | ⚠️ Misleading | ✅ Correct — reviewer's definition was wrong | None |
| OOM thresholds | ⚠️ Undocumented | Valid — logic correct, comments missing | Comments added to both calculators |
| Join scratch factors | ⚠️ Arbitrary | Valid — logic correct, comments missing | Comments added to both calculators |
| Service amortization ceil() | ⚠️ Over-reserves | Valid but small (≤2 cores), conservative by design | None |
| Output file sizing 150 MB | ⚠️ Too small | ✅ Incorrect — 150 MB is within Snowflake recommended range | None |
| Network utilization 80% | ⚠️ Simplified | Valid simplification, appropriate for tool scope | None |
| Scratch coverage validation | ⚠️ Incomplete | ✅ Reviewer's logic was flawed — formula is correct | None |

### Changes made to source files
- `development_spark_calculator.html` — expanded OOM threshold and join scratch factor comments in `recalc()`
- `production_spark_calculator.html` — added OOM threshold and join scratch factor comments in `recalc()` (previously had none)

### Location in code
Both changes are in the `recalc()` function, in the block that reads input values and computes
derived constants — just after the optional service checkbox reads and before the infrastructure
reservation math. In terms of UI sections, the constants drive:
- **Section B — Fixed Overhead Reservations**
- **Section C — Executor Sizing**
- **Section D — Storage & Workload Sizing**

---

## Revisions

### 2026-04-01 — Initial calculator release

Core executor and storage formulas established in both calculators. Baseline math against which all subsequent changes are measured.

| Formula | Expression |
|---|---|
| Executor slot RAM | `SLOT_GB = (RAM_VM - 2) / EXEC_PER_VM` |
| Max executor memory | `MAX_EXEC_MEM = (SLOT_GB - OFFHEAP) / (1 + OVH_PCT)` |
| Executor memory (5% margin) | `EXEC_MEM = floor(MAX_EXEC_MEM * 0.95)` |
| Executors per VM | `EXEC_PER_VM = floor((VCPU_VM - 2) / EXEC_CORES)` |
| Total executors | `TOTAL_EXEC = max(1, EXEC_PER_VM * TOTAL_VMS - 1)` |
| Ceph usable | `CEPH_USABLE = OSD_NODE * NVME_TB * NODES / CEPH_REP` |
| Ceph headroom days | `CEPH_DAYS = CEPH_USABLE / DAILY_TB` |
| Scratch per VM | `SCRATCH_TB_PER_VM = (NVME_COUNT - OSD_NODE) / VMS_NODE * NVME_TB` |

---

### 2026-04-03 — Parquet partitioning and network transfer cards added

Added two new calculation blocks. No changes to executor or storage math.

**Parquet partitioning:**

| Formula | Expression |
|---|---|
| Parquet output size | `PARQ_MB = CSV_MB / PARQ_COMP` |
| Input read tasks | `INPUT_PARTS = ceil(CSV_MB / MAX_PART_MB)` |
| Target output file size | `TARGET_OUT_MB = 150` (fixed — within Snowflake-recommended 100–250 MB range) |
| Output part files | `OUTPUT_PARTS = max(1, ceil(PARQ_MB / TARGET_OUT_MB))` |

**Network transfer:**

| Formula | Expression |
|---|---|
| Network bottleneck | `BOTTLENECK_G = min(AGG_NODE_G, NET_SWITCH_G, NET_WAN_G)` |
| Effective throughput | `EFF_GBPS = BOTTLENECK_G * 0.80` (80% utilization) |
| Transfer time | `TRANSFER_SEC = PARQ_GB / (EFF_GBPS / 8)` |

---

### 2026-04-15 — Skew profile, join type, blast radius, and dynamic slider bounds added

Major math additions from sandbox promotion to dev calculator; simultaneously ported to production.

**OOM threshold (skew-aware):**
```js
// Uniform (4 GB): standard Parquet read buffer + overhead
// Moderate (5 GB): Parquet read buffer + sort buffer + spill spike simultaneously
// Heavy (6 GB): full Parquet stripe + multiple concurrent spill buffers in flight
const OOM_THRESHOLD = SKEW_PROFILE === 'heavy' ? 6 : SKEW_PROFILE === 'moderate' ? 5 : 4;
```

**Join scratch factor:**
```js
// Broadcast (1.0): no shuffle materialized
// Mixed (1.1): repartition/coalesce ops add ~10% intermediate data
// Wide (1.25): sort-merge join keys add ~25% additional scratch
const JOIN_SCRATCH_FACTOR = JOIN_TYPE === 'wide' ? 1.25 : JOIN_TYPE === 'mixed' ? 1.1 : 1.0;
```

**Blast radius:**
```js
const BLAST_PCT = TOTAL_EXEC > 0 ? 100 / TOTAL_EXEC : 100;
// Percentage of cluster compute capacity lost on single executor failure
```

**Scratch adequacy check (updated to include join factor):**
```js
const scratchOk = SCRATCH_TB_PER_VM >= DAILY_TB * SHUF_AMP * JOIN_SCRATCH_FACTOR * 0.75;
```

**Dynamic slider bounds** — vCPU max and `exec_cores` max are now clamped at runtime based on available cores after infrastructure reservation, preventing physically impossible configurations.

---

### 2026-04-17 — OOM threshold and join scratch factor comments added (third-party review)

No formula changes. Inline code comments expanded in both calculators explaining the basis of the 4/5/6 GB OOM thresholds and the 1.0/1.1/1.25 join scratch multipliers, which had been undocumented. See Issues 2 and 3 above for full rationale.

---

### 2026-04-18 — CEPH_DAYS formula revised; Ceph warning language updated

#### Context

Architectural review confirmed the following constraints not captured in the original formula:

1. Snowflake has no inbound network access. Transfer is performed by an outbound batch job — not Snowflake-triggered.
2. Parquet output persists on local Ceph until the batch transfer job confirms successful delivery. Deletion is batch-triggered, not job-completion-triggered.
3. Up to N concurrent Parquet outputs may coexist on local Ceph during the window between job completion and batch transfer confirmation.
4. Worker VM OS disks (80 GB per VM, Ceph RBD) consume logical Ceph usable permanently and were not previously deducted.

#### Formula change

**Before:**
```js
const CEPH_DAYS = CEPH_USABLE / DAILY_TB;
```

**After:**
```js
const PARQ_COMP       = +el('parquet_compression').value;
const N_PARQUET       = +el('n_parquet').value;
const VM_OS_USABLE_TB = VMS_NODE * NODES * 80 / 1024;   // 80 GB OS disk per VM, logical Ceph usable
const PARQ_PENDING_TB = N_PARQUET * (DAILY_TB / PARQ_COMP);
const CEPH_RESERVED   = VM_OS_USABLE_TB + PARQ_PENDING_TB;
const CEPH_EFFECTIVE  = Math.max(0, CEPH_USABLE - CEPH_RESERVED);
const CEPH_DAYS       = CEPH_EFFECTIVE / DAILY_TB;
```

`CEPH_DAYS` now represents **effective ingest headroom** — available Ceph capacity after deducting VM OS disk allocation and N pending Parquet outputs — divided by daily ingest volume.

#### New UI input (both calculators)

| Property | Value |
|---|---|
| Label | Parquet outputs pending transfer |
| ID | `n_parquet` |
| Range | 1–5, step 1, default 2 |
| Description | Max concurrent Parquet sets on Ceph awaiting outbound batch transfer confirmation |

#### Warning language updated

All references to "Snowflake flush schedule" and "Snowflake load pipeline" replaced with "outbound batch transfer pipeline" in both calculators.

#### Metric display updated

- **"Ceph usable" metric** now shows `CEPH_EFFECTIVE` with sub-label: `X.X TB raw usable − Y.YY TB reserved (N× Parquet + VM OS)`
- **"Days of ingest" sub-label** updated to: `effective · after N× pending Parquet + VM disks`

#### Files modified
- `development_spark_calculator.html`
- `production_spark_calculator.html`
