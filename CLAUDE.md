# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Infrastructure sizing tools for a 3-node Proxmox hyperconverged cluster running Apache Spark (via YARN), Ceph RGW (S3), and daily ETL ingest (2 TB/day) to Snowflake. Two calculators exist — production and development — each a single self-contained HTML file.

## Serving the Calculators

Always serve via HTTP, not `file://`. localStorage scoping differs between origins and scenarios saved under one will be invisible to the other.

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/production_spark_calculator.html` or the dev equivalent.

## Editing Rules

**Always back up before editing any HTML file in this project** — calculators, guides, or any other `.html` file. Do this before making any change, no exceptions:

```bash
cp production_spark_calculator.html production_spark_calculator.html.bak
cp development_spark_calculator.html development_spark_calculator.html.bak
cp prod_calculator_guide.html prod_calculator_guide.html.bak
cp dev_calculator_guide.html dev_calculator_guide.html.bak
```

Back up only the specific file(s) being edited. Never edit `.bak` files. When a change is made to either calculator, the corresponding guide file (`prod_calculator_guide.html`, `dev_calculator_guide.html`) may need updating — the guides contain inline base64 screenshots that become stale when the UI changes.

## Calculator Architecture

Both calculators are single-file HTML/CSS/JS with no external dependencies and no build step.

### Hardware Constants

Defined at the **top of the `<script>` block** as module-level constants — not inside `recalc()`. Update here when hardware specs change:

- **Production:** `NODES=3`, `CORES_NODE=64`, `NVME_COUNT=9`, `NVME_TB=3.2`, `SSD_COUNT=3`, `SSD_GB=0.48`
- **Development:** `NODES=3`, `CORES_NODE=32`, `NVME_COUNT=7`, `NVME_TB=3.84`, `SSD_COUNT=3`, `SSD_GB=0.48`

### `recalc()` Execution Order — Critical

`recalc()` is called on every slider/checkbox `oninput`/`onchange` event. Its internal order is load-bearing:

1. **Pre-scale block** (top, before any reads) — recomputes `ram_per_vm` slider `max` from current `ram_node` value, then proportionally rescales the slider value to maintain the same percentage position. This must run first.
2. Slider display updates (`setVal(...)`)
3. Read all input values into constants (`VMS_NODE`, `VCPU_VM`, etc.)
4. Infrastructure reservation math
5. Executor math
6. UI updates (bars, metrics, storage grid, param table, warnings)

### State Restoration Load Order

`loadState()` and `loadScenario()` must restore `ram_node` **before** iterating other range inputs:

```js
if (state.ram_node !== undefined) el('ram_node').value = state.ram_node;
document.querySelectorAll('input[type=range]').forEach(...);
```

This is required because the pre-scale block in `recalc()` reads `ram_node` to compute the valid max for `ram_per_vm`. Restoring out of order causes the RAM/VM slider to clamp incorrectly.

### localStorage Keys

| Key | Purpose | Written by |
|---|---|---|
| `spark_calc_prod` | Session continuity (production) | Save button only |
| `spark_calc_dev` | Session continuity (development) | Save button only |
| `spark_calc_prod_scenarios` | Named scenarios (production) | Save Scenario / Delete |
| `spark_calc_dev_scenarios` | Named scenarios (development) | Save Scenario / Delete |

Loading a named scenario applies sliders and calls `recalc()` but **does not write to localStorage**. Session continuity is only updated by an explicit Save button click.

### Key Sizing Math

```
SLOT_GB       = (RAM_VM - 2 GB NodeManager) / EXEC_PER_VM
MAX_EXEC_MEM  = (SLOT_GB - OFFHEAP) / (1 + OVH_PCT)
EXEC_MEM      = floor(MAX_EXEC_MEM * 0.95)          // 5% safety margin
OOM_MARGIN    = SLOT_GB - (EXEC_MEM * (1 + OVH_PCT) + OFFHEAP)

EXEC_PER_VM   = floor((VCPU_VM - 2) / EXEC_CORES)   // 2 vCPUs reserved for OS + NodeManager
TOTAL_EXEC    = max(1, EXEC_PER_VM * TOTAL_VMS - 1)  // -1 for YARN cluster-mode driver

CEPH_USABLE   = OSD_NODE * NVME_TB * NODES / CEPH_REP
SCRATCH_TB_PER_VM = (NVME_COUNT - OSD_NODE) / VMS_NODE * NVME_TB
```

OOM warning threshold: `< 4 GB`. Scratch warning threshold: `< 75%` of worst-case shuffle volume (`DAILY_TB * SHUF_AMP`).

### NUMA Constraint

Max 32 vCPUs per VM with NUMA pinning enabled (one NUMA domain = one CPU socket = 32 cores on production hardware). Exceeding this causes the NUMA boundary crossed error, with message text that varies based on whether NUMA pinning is currently on or off.

### Security Helpers

`_escHtml(s)` escapes `&`, `<`, `>`, `"` — must be applied to any user-supplied string (scenario names) before injecting into `innerHTML` or `document.write()`. This includes option values in `renderScenarioList()` and both the title and `<pre>` content in `viewScenario()`.

## Utility Scripts

`export_chat.py` — converts a Claude Code JSONL session file to readable Markdown. Hardcoded to the session file for this project; pass a path argument to use a different session.

## Hardware Reference

| | Production | Development |
|---|---|---|
| Nodes | 3 | 3 |
| Cores/node | 64 (2× 32c, dual NUMA) | 32 (1× 32c, single NUMA) |
| RAM/node | 768 GB (24× 32 GB DIMMs) | 384 GB (12× 32 GB DIMMs) |
| NVMe/node | 9× 3.2 TB | 7× 3.84 TB |
| SSD/node | 3× 480 GB (ZFS mirror + hot spare) | 3× 480 GB |
| RAM slider step | 32 GB (one DIMM) | 32 GB |

Infrastructure reservations per node: Proxmox 2c/8 GB, Ceph RGW 4c/8 GB, Ceph MON 2c/6 GB, Ceph OSD 1c/3 GB each.
