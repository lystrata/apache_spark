# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Infrastructure sizing tools for a 3-node Proxmox hyperconverged cluster running Apache Spark (via YARN), Ceph RGW (S3), and daily ETL ingest (2 TB/day) to Snowflake. Two calculators exist — production and development — each a single self-contained HTML file.

## Project Structure

All working HTML documents live in `Document/`. Scripts live in `Scripts/`. Research notes and planning documents live in `Notes/`. `Ready_For_Review/` is a staging area only — it should be empty between review cycles.

| Directory | Contents |
|---|---|
| `Document/` | All working HTML: calculators, guides, references, research summaries |
| `Scripts/` | Utility scripts (e.g. `export_chat.py`) |
| `Notes/` | Research notes, planning documents, chat exports |
| `Ready_For_Review/` | Staging only — files pending user review before promotion |
| `Images/` | Screenshots organized by `Development/` and `Production/` subdirectories |
| `Incoming/` | Source PDFs and reference material |

## Session TODO Convention

Each chat context maintains a TODO file tracking outstanding tasks, open questions, and next steps. At the end of a session — or when the user signals they are wrapping up — create or update the relevant TODO file with current status.

| Context | TODO file |
|---|---|
| Spark calculators and cluster sizing | `Notes/todos_calculator.md` |
| Remote services (Airflow, monitoring, bastion) | `Notes_remote_services/todos_remote_services.md` |

**"show todos" prompt:** When the user types `show todos`, read and display the contents of both TODO files. If only one context is active in the current session, display that one and note the other exists.

**Format:** Each TODO file uses three sections — `## Waiting for Vendor Reply`, `## Open Questions`, `## Pending Tasks`, and `## Next Session`. Use Markdown checklist boxes (`- [ ]` unchecked, `- [x]` checked) for all items. Check items off as they are resolved rather than deleting them, so there is a record of what was completed and when.

## Vendor Questions Convention

When the user identifies a question that must be forwarded to a vendor, add it to the relevant `questions_for_vendors.txt` file with full context and a `- [ ]` entry under `## Waiting for Vendor Reply` in the TODO file. When a vendor reply is received, check off the TODO item and note the answer in `questions_for_vendors.txt`.

| Context | Vendor questions file |
|---|---|
| Spark calculators and cluster sizing | `Notes/questions_for_vendors.txt` |
| Remote services (Airflow, monitoring, bastion) | `Notes_remote_services/questions_for_vendors.txt` |

---

## Serving the Calculators

Always serve via HTTP, not `file://`. localStorage scoping differs between origins and scenarios saved under one will be invisible to the other.

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/Document/production_spark_calculator.html` or the dev equivalent.

## Ready_For_Review Staging Rule

**All new files and refactored existing files must be written to `Ready_For_Review/` first.** Do not write directly to the working location. The workflow is:

1. Write the output to `Ready_For_Review/<filename>` (same filename as the target)
2. User reviews the file
3. On approval, copy to `Document/` (the working location) and **delete from `Ready_For_Review/`**
4. Commit the promoted file

`Ready_For_Review/` must be empty between review cycles. A file remaining there after promotion is a mistake.

This applies to: new HTML documents, calculator updates, reference document updates, and any file where content changes are being made. It does not apply to CLAUDE.md, memory files, or minor in-place fixes explicitly approved by the user.

## Editing Rules

This project uses git for version control. **Commit before making significant edits** so any state can be restored.

### Pre-Commit Sanitization Hook

A pre-commit hook at `.git/hooks/pre-commit` scans staged content for corporate identifiers before every commit. Patterns checked (case-insensitive): `allegiance`, `askallegiance`, `rohn.wood@`. When a match is found, the commit is interrupted and prompts for action: sanitize, force, or quit.

**This hook is not tracked by git** (`.git/` is never committed). It must be installed manually on each machine after cloning:

```bash
# From the repo root — run once after cloning
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
PATTERNS="allegiance|askallegiance|rohn\.wood@"
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
if [ -z "$STAGED" ]; then exit 0; fi
MATCHES=$(git diff --cached -U0 | grep -iE "^\+" | grep -iE "$PATTERNS")
if [ -z "$MATCHES" ]; then exit 0; fi
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  pre-commit: corporate identifier(s) found in staged files  │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""
echo "$MATCHES" | sed 's/^+/  /'
echo ""
echo "  Options:"
echo "    s  sanitize — abort commit and review manually"
echo "    f  force    — commit anyway (intentional)"
echo "    q  quit     — abort commit, no action"
echo ""
exec < /dev/tty
read -rp "  Choice [s/f/q]: " CHOICE
echo ""
case "$CHOICE" in
  f|F) echo "  Proceeding with commit."; exit 0 ;;
  s|S) echo "  Commit aborted. Sanitize flagged lines before committing."; exit 1 ;;
  *)   echo "  Commit aborted."; exit 1 ;;
esac
EOF
chmod +x .git/hooks/pre-commit
```

```bash
git add <file>
git commit -m "Pre-edit snapshot: <brief description>"
```

To restore a previous state:

```bash
git checkout <commit-hash> -- <file>
```

**Any new HTML or Markdown file added to the project must be placed under git revision control immediately** — `git add <file>` at creation time, before any edits are made. Markdown files must also be committed each time they are updated — do not leave changes unstaged between sessions.

**Any HTML file that contains a Revisions section must have that section updated as part of the same edit** whenever a formula, calculation, or content change is made. The Revisions section entry must include the date, a short title, and a description of what changed and why. Documentation-only changes (comments, labels, styling) should be noted briefly rather than given a full entry. Do not update the Revisions section for navigation, layout, or styling changes alone.

Files with Revisions sections:
- `Document/development_spark_calculator.html` — section id `sec_revisions`
- `Document/production_spark_calculator.html` — section id `sec_revisions`
- `Document/dev_cluster_math_reference.html` — section id `revisions`
- `Document/dev-cluster-storage-reference.html` — section id `sec_revisions`

When a change is made to either calculator, the corresponding guide file (`Document/prod_calculator_guide.html`, `Document/dev_calculator_guide.html`) may need updating — the guides contain inline base64 screenshots that become stale when the UI changes.

## HTML Document Conventions

These patterns are established and must be used consistently across all HTML files in this project.

### Section Collapsible Pattern

All content sections use `<details class="section-details">` with `<summary class="section-summary">`. Every section must have:
- A `<span class="section-letter">` (A, B, C…) or `<span class="section-title">` for untitled sections (e.g. Overview, Revisions)
- A `<span class="section-sub">` for the subtitle/description line
- A `<a href="#top" class="btt" onclick="event.stopPropagation()">↑ Top</a>` back-to-top link in the summary
- A `<div class="section-close">` at the bottom of the section body with a close link

```html
<details class="section-details" id="sec_x">
  <summary class="section-summary">
    <span class="section-letter">X</span>
    <span class="section-title">Section Title</span>
    <span class="section-sub">· subtitle · description</span>
    <a href="#top" class="btt" onclick="event.stopPropagation()">&#8593; Top</a>
  </summary>
  <div class="section-body">
    <!-- content -->
    <div class="section-close"><a onclick="this.closest('details').open=false">&#x25B2; Close section</a></div>
  </div>
</details>
```

### Section Default State

All sections default **closed** on page load. Enforce with a `DOMContentLoaded` handler that overrides browser session memory:

```js
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('details.section-details').forEach(function(d) { d.open = false; });
});
```

Exception: reference documents may have one section open by default (e.g. Overview & Assumptions). Add its `id` to the exclusion condition: `if (d.id !== 'sec_overview') d.open = false;`

### Sub-Section Pattern (within a section)

When a section has multiple named sub-topics, convert them to nested collapsibles using `sub-details`. Sub-sections default closed (the parent `DOMContentLoaded` handler closes `details.section-details` only; sub-details are closed by the browser's default since they have no `open` attribute). The close link uses `closeSub()` to scroll the summary back into view after close.

```html
<details class="sub-details">
  <summary class="sub-summary">
    <span class="sub-title">SUB-SECTION TITLE</span>
    <span class="sub-desc">short description of contents</span>
  </summary>
  <div class="sub-body">
    <!-- content -->
    <div class="sub-close"><a onclick="closeSub(this)">&#x25B2; Close</a></div>
  </div>
</details>
```

Required JS (add to script block):
```js
function closeSub(el) {
  var d = el.closest('details');
  d.open = false;
  setTimeout(function() { d.querySelector('summary').scrollIntoView({behavior:'smooth', block:'start'}); }, 30);
}
```

Required CSS (add to `<style>` block — copy from `Document/dev_cluster_math_reference.html`):
`.sub-details`, `.sub-summary`, `.sub-title`, `.sub-desc`, `.sub-body`, `.sub-close`

### Cross-Reference Jump Links

Whenever a section references content in a different section, use `jumpTo()` to open the target section and scroll to the anchor. Never use bare `href="#anchor"` for cross-section links — the target section will be closed and the anchor invisible.

```html
<a href="#anchor-id" onclick="jumpTo('anchor-id', 'sec_target')">link text</a>
```

Required JS (add to script block — one copy per file):
```js
var _jumpedTo = null;
function jumpTo(hash, sectionId) {
  event.preventDefault();
  _jumpedTo = {hash: hash, sectionId: sectionId};
  history.pushState(null, '', '#' + hash);
  var d = document.getElementById(sectionId);
  if (d) d.open = true;
  setTimeout(function() { var t = document.getElementById(hash); if (t) t.scrollIntoView({behavior:'smooth'}); }, 50);
}
window.addEventListener('popstate', function() {
  if (_jumpedTo && location.hash !== '#' + _jumpedTo.hash) {
    var sec = document.getElementById(_jumpedTo.sectionId);
    if (sec) sec.open = false;
    _jumpedTo = null;
  }
});
```

Anchor targets must have an `id` on the element being linked to (e.g. `<h3 id="config-i-spec">`). Add `id` attributes to h3/h2 elements when they are likely cross-reference targets.

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

All scripts live in `Scripts/`.

`Scripts/export_chat.py` — converts a Claude Code JSONL session file to readable Markdown. Hardcoded to the session file for this project; pass a path argument to use a different session.

## Hardware Reference

| | Production | Development |
|---|---|---|
| Nodes | 3 | 3 |
| Cores/node | 64 (2× 32c, dual NUMA) | 32 (1× 32c, single NUMA) |
| RAM/node | 768 GB (24× 32 GB DIMMs) | 384 GB (12× 32 GB DIMMs) |
| NVMe/node | 9× 3.2 TB | 7× 3.84 TB |
| SSD/node | 3× 480 GB (ZFS mirror + hot spare) | 3× 480 GB |
| RAM slider step | 32 GB (one DIMM) | 32 GB |

Infrastructure reservations per node: Proxmox 2c/8 GB, ZFS ARC —/8 GB (zfs_arc_max=8589934592), Ceph RGW 4c/8 GB, Ceph MON 2c/6 GB, Ceph OSD 1c/3 GB each.
