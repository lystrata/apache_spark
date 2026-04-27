# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Infrastructure sizing tools for a 3-node Proxmox hyperconverged cluster running Apache Spark (via YARN), Ceph RGW (S3), and daily ETL ingest (2 TB/day) to Snowflake. Two calculators exist — production and development — each a single self-contained HTML file.

## Project Structure

The project is organized into four context hierarchies: `calculators/`, `remote_services/`, `security/`, and `correspondence/`. Each contains `Document/`, `Notes/`, `Ready_For_Review/`, `Incoming/`, and `Images/` subdirectories. Shared utilities live in `Scripts/` at the root. `Ready_For_Review/` directories are staging areas only — they should be empty between review cycles.

| Directory | Contents |
|---|---|
| `calculators/Document/` | Working HTML: calculators, guides, references, research summaries |
| `calculators/Notes/` | Research notes, planning documents, chat exports |
| `calculators/Ready_For_Review/` | Staging only — files pending user review before promotion |
| `calculators/Incoming/` | Source PDFs and reference material |
| `calculators/Images/` | Screenshots organized by `Development/` and `Production/` subdirectories |
| `remote_services/Document/` | Working HTML for remote services (Airflow, monitoring, bastion) |
| `remote_services/Notes/` | Research notes and planning for remote services context |
| `remote_services/Ready_For_Review/` | Staging for remote services documents |
| `remote_services/Incoming/` | Source PDFs and reference material for remote services context |
| `remote_services/Images/` | Screenshots for remote services documentation |
| `remote_services/Scripts/` | Context-specific scripts for remote services |
| `security/Document/` | Working HTML for security context — on-site revision control only |
| `security/Notes/` | Research notes and planning for security context — on-site revision control only |
| `security/Ready_For_Review/` | Staging for security documents |
| `security/Incoming/` | Source PDFs and reference material for security context — on-site revision control only |
| `security/Images/` | Screenshots for security documentation |
| `security/Scripts/` | Context-specific scripts for security |
| `correspondence/Document/` | Working documents for project correspondence — no revision control |
| `correspondence/Notes/` | Planning and notes for correspondence context |
| `correspondence/Ready_For_Review/` | Staging for correspondence documents |
| `correspondence/Incoming/` | Source material and reference PDFs for correspondence context |
| `correspondence/Images/` | Screenshots for correspondence documentation |
| `Scripts/` | Shared utility scripts (e.g. `export_chat.py`) |
| `Shared_References/` | Reference materials shared across all contexts |

## Session Context Convention

At the start of a session the user may type `set context <name>` to declare which fork is active. Valid names and their associated directories:

| Name | Vendor questions | Documents | Staging |
|---|---|---|---|
| `calculators` | `calculators/Notes/questions_for_vendors.txt` | `calculators/Document/` | `calculators/Ready_For_Review/` |
| `remote_services` | `remote_services/Notes/questions_for_vendors.txt` | `remote_services/Document/` | `remote_services/Ready_For_Review/` |
| `security` | `security/Notes/questions_for_vendors.txt` | `security/Document/` | `security/Ready_For_Review/` |
| `correspondence` | `correspondence/Notes/questions_for_vendors.txt` | `correspondence/Document/` | `correspondence/Ready_For_Review/` |

When the user types `set context <name>`:
1. Acknowledge the active context by name.
2. Read the master TODO file and surface items tagged `[<name>]` in `## Next Session` or unresolved `## Open Questions`.
3. For the remainder of the session, use that context's vendor questions file, document directory, and staging directory exclusively.

If no context is set, ask the user which context applies before doing any work that touches files.

## Session TODO Convention

All tasks across all contexts are tracked in a single master TODO file (`TODO.md` at root) with context tags (`[calculators]`, `[remote_services]`, `[security]`, `[correspondence]`) on each item.

**"show todos" prompt:** When the user types `show todos`:
- If a context is active, read and display the master TODO file filtering for that context's `[<name>]` tagged items only.
- If no context is set, read and display the full master TODO file.

**Format:** The master TODO file uses four sections — `## Waiting for Vendor Reply`, `## Open Questions`, `## Pending Tasks`, and `## Next Session`. Use Markdown checklist boxes (`- [ ]` unchecked, `- [x]` checked) for all items. Check items off as they are resolved rather than deleting them, so there is a record of what was completed and when. Each item is tagged with its context in square brackets at the start of the line.

**Source document rule:** When a TODO item is derived from a specific document, include the document's project-relative path in the item text so the user can locate it for context. Example: `- [ ] [calculators] Review OSD allocation strategy — see calculators/Document/dev-cluster-storage-reference.html`

## Vendor Questions Convention

When the user identifies a question that must be forwarded to a vendor, add it to the relevant `questions_for_vendors.txt` file with full context and a `- [ ]` entry under `## Waiting for Vendor Reply` in the TODO file. When a vendor reply is received, check off the TODO item and note the answer in `questions_for_vendors.txt`.

| Context | Vendor questions file |
|---|---|
| Spark calculators and cluster sizing | `calculators/Notes/questions_for_vendors.txt` |
| Remote services (Airflow, monitoring, bastion) | `remote_services/Notes/questions_for_vendors.txt` |
| Security | `security/Notes/questions_for_vendors.txt` |
| Project correspondence | `correspondence/Notes/questions_for_vendors.txt` |

---

## Citation Rules

These rules apply in the **security context** at full strength. In other contexts, citations are encouraged for non-obvious technical claims but not required at the two-source minimum.

- Every substantive claim in a security document must be supported by a minimum of **two verifiable external sources**, cited at the section level.
- A single-sentence claim that stands alone (not covered by the section's general citations) requires its own inline citation.
- **Acceptable sources:** official framework publications (NIST, CIS, AICPA), vendor documentation, peer-reviewed papers, and industry-recognized publications.
- **Personal blogs** carry low weight. Cite them only when multiple independent sources cluster on the same conclusion, and note that the sourcing is blog-level.
- If fewer than two corroborating sources can be found, state explicitly: *"I cannot find corroborated evidence for this claim."* Do not assert it.
- All citations must include a URL the user can verify directly. If a URL cannot be confirmed as live and correct, do not include it — state the source by title and publisher instead.

## Documents for Distribution: Turabian Style Format

Applies to **all contexts** (calculators, remote_services, security). Use this format for any HTML document intended for external distribution or formal review.

**Reference:** `Shared_References/Turabian-Style-Guide.080919.pdf` (2019 Turabian Style Guide, Calvary University)

**Turabian elements to apply (electronic communication):**

1. **Heading Hierarchy** (Turabian § 2.2.2)
   - Level 1: Italicized, centered (*main title*)
   - Level 2: Non-italicized, centered (**major sections**)
   - Level 3: Italicized, left-aligned (*subsections*)
   - Level 4: Non-italicized, left-aligned (**sub-subsections**)

2. **Footnotes** (Turabian § 16)
   - **Full form on first citation (Turabian § 16.4):** Author, "Title," in *Source*, accessed Date, URL.
   - **Shortened form on subsequent citations:** Author, "Short Title," in *Source*.
   - Superscript numbers placed after punctuation ending the sentence.
   - Single-spaced with blank line between each footnote.

3. **Block Quotations** (Turabian § 2.2.5)
   - Indented ½" from left margin (40px in HTML).
   - Single-spaced within the quotation.
   - No quotation marks at beginning/end (indentation replaces them).

4. **Bibliography** (Turabian § 2.2.6 and § 16.1)
   - Alphabetized by author last name (A–Z).
   - Hanging indent (first line flush left, subsequent lines indented ½").
   - Single-spaced entries with blank lines between sources.
   - Include all works cited plus quality works consulted.
   - Format: Author, "Title," in *Source*, accessed Date, URL.

**URL Line Breaking:**
- Break long URLs only when necessary to fit readable line width (approximately 110–130 characters).
- Break at directory boundaries using backslash continuation (`\<br/>`).
- Example: `https://github.com/keycloak/keycloak/blob/main/\<br/>docs/documentation/server_admin/...`

**Application:** All new distribution documents must follow this format. Documents in `calculators/Document/`, `remote_services/Document/`, and `security/Document/` directories should use Turabian styling.

---

## Compact Milestones

Applies to **all contexts** (calculators, remote_services, security, correspondence).

When a natural stopping point is reached — a document is complete and staged, a cluster of open questions is resolved, a planning phase closes — flag it and ask the user whether to `/compact` before continuing. What constitutes a milestone is a judgment call; when uncertain, ask rather than assume.

---

## Serving the Calculators

Always serve via HTTP, not `file://`. localStorage scoping differs between origins and scenarios saved under one will be invisible to the other.

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/calculators/Document/production_spark_calculator.html` or the dev equivalent.

## PDF Generation from Markdown

When converting markdown documents to PDF using Pandoc, always include the `--toc` flag to generate a clickable table of contents in the PDF (appears as bookmarks/outline in PDF readers). When the source markdown contains GFM checkboxes, also pass `--from=markdown+task_lists` so they render as real checkbox glyphs.

**Standard command:**
```bash
eval "$(brew shellenv)" && export PATH="/Library/TeX/texbin:$PATH" && \
pandoc <input.md> -o <output.pdf> --toc --pdf-engine=lualatex -V geometry:margin=1in --from=markdown+task_lists
```

**Benefits:**
- Auto-generates TOC from markdown headings
- Creates clickable bookmarks/outline in PDF readers (Acrobat, Preview, etc.)
- Readers can navigate via sidebar
- No manual anchor maintenance needed in PDF

## Document Versioning

Distribution markdown documents and their generated PDFs carry an explicit version in the filename: `<basename>_v<MAJOR>.<MINOR>.<ext>`.

**Format:** `_v<MAJOR>.<MINOR>` appended immediately before the extension. Both the `.md` and the `.pdf` always carry the **same** version number.

**Examples:**
- `Phases_Critical_Path_v1.0.md` and `Phases_Critical_Path_v1.0.pdf`
- `CP_Okta_v1.2.md` and `CP_Okta_v1.2.pdf`

**When to bump:**
- **MINOR** (`v1.0` → `v1.1`) — content additions, fixes, clarifications, or refinements within the existing document structure. Most edits are minor bumps.
- **MAJOR** (`v1.x` → `v2.0`) — structural overhauls, scope expansion, framework changes (e.g., new section taxonomy, renumbering of task families, fundamental redirection of the document's purpose). Reset MINOR to 0 when MAJOR bumps.

**Workflow per bump:**
1. `git mv <basename>_v<old>.md <basename>_v<new>.md` (and `.pdf`)
2. Update the document's internal `_Last updated_` line and version marker in the header block
3. Apply content edits in the renamed file
4. Regenerate the PDF under the new versioned name
5. Update every cross-reference in other repo files (use `grep -rln <basename>_v` to find them)
6. Commit the rename + content + PDF together so the version bump is one atomic commit
7. The prior version remains in git history for diff/blame

**Scope of this rule:** distribution markdown documents (planning documents, critical-path plans, design documents, technical specs intended for review or external sharing) and their PDFs. Does **not** apply to:
- `CLAUDE.md`, `MEMORY.md`, `TODO.md`, `README.md` — operational/index files that are continuously edited in place
- `Notes/`, `Incoming/` files — drafts and source material
- Vendor questions, meeting notes, conversation exports
- HTML calculators and references — those have their own in-document `Revisions` section per `Editing Rules` below

When in doubt, ask: "Will this document be distributed or referenced by others as a snapshot?" If yes, it gets a version. If no, edit in place.

## Ready_For_Review Staging Rule

**All new files and refactored existing files must be written to `Ready_For_Review/` first.** Do not write directly to the working location. The workflow is:

1. Write the output to `Ready_For_Review/<filename>` (same filename as the target)
2. User reviews the file
3. On approval, copy to `Document/` (the working location) and **delete from `Ready_For_Review/`**
4. Commit the promoted file

`Ready_For_Review/` must be empty between review cycles. A file remaining there after promotion is a mistake.

This applies to: new HTML documents, calculator updates, reference document updates, and any file where content changes are being made. It does not apply to CLAUDE.md, memory files, or minor in-place fixes explicitly approved by the user.

**Index update rule:** When any new HTML file is promoted to `calculators/Document/`, add a corresponding entry to `calculators/Document/index.html` in the appropriate section (Calculators, Guides, Reference, or Research & Correspondence) as part of the same commit. The index must always reflect the current contents of `Document/`.

## Editing Rules

This project uses git for version control. **Commit before making significant edits** so any state can be restored.

### Corporate Identifier Sanitization

Before committing any file, replace corporate identifiers with the literal placeholder `fqdn`. The exact patterns to match are stored in `~/.config/spark-hooks/patterns` (never committed).

**Rule:** any occurrence of the corporate FQDN or company name (standalone, any case) must be replaced with `fqdn` before staging. This applies to all file types: HTML, Markdown, config files, and scripts.

Example: a Keycloak realm export filename containing the company name becomes `fqdn-realm.json`.

The pre-commit hook detects any remaining matches and blocks the commit. Apply substitutions before staging rather than relying on the hook to catch them.

### Pre-Commit Sanitization Hook

A pre-commit hook at `.git/hooks/pre-commit` scans staged content for corporate identifiers before every commit. When a match is found, the commit is interrupted and prompts for action: sanitize, force, or quit.

**Patterns are stored outside the repo** in `~/.config/spark-hooks/patterns` (owner read-only, `600`). This file is never committed and contains no patterns in the repo itself.

**Neither the hook nor the pattern file is tracked by git.** Both must be installed manually on each machine after cloning.

#### Step 1 — Create the pattern file

```bash
mkdir -p ~/.config/spark-hooks
# Add corporate identifier strings to this file, one per line
nano ~/.config/spark-hooks/patterns
chmod 600 ~/.config/spark-hooks/patterns
```

#### Step 2 — Install the hook

```bash
# From the repo root
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit 2>/dev/null || true
curl -fsSL https://raw.githubusercontent.com/lystrata/apache_spark/main/.git/hooks/pre-commit 2>/dev/null || \
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
PATTERN_FILE="$HOME/.config/spark-hooks/patterns"
if [ ! -f "$PATTERN_FILE" ]; then
  echo "  pre-commit: pattern file not found at $PATTERN_FILE — skipping identifier scan"
  exit 0
fi
PATTERNS=$(paste -sd'|' "$PATTERN_FILE")
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
- `calculators/Document/development_spark_calculator.html` — section id `sec_revisions`
- `calculators/Document/production_spark_calculator.html` — section id `sec_revisions`
- `calculators/Document/dev_cluster_math_reference.html` — section id `revisions`
- `calculators/Document/dev-cluster-storage-reference.html` — section id `sec_revisions`
- `phases/phase1/deliverables/dev_cluster_phase1_model.html` — section id `sec_revisions`

When a change is made to either calculator, the corresponding guide file (`calculators/Document/prod_calculator_guide.html`, `calculators/Document/dev_calculator_guide.html`) may need updating — the guides contain inline base64 screenshots that become stale when the UI changes.

## Markdown Documents

This project uses Markdown extensively for planning, specification, and documentation. Follow these standards for consistency and cross-editor compatibility.

### Table of Contents and Anchor Generation

**Rule:** Use explicit HTML anchor tags `<a id="anchor-name"></a>` for markdown tables of contents, not auto-generated markdown anchors.

**Why:** Markdown editors auto-generate anchor IDs differently. Emojis, special characters (—, &), and heading case handling vary across Obsidian, GitHub, VS Code, and other viewers. Explicit HTML anchors are universal and work identically across all platforms and tools (including PDF conversion via Pandoc).

**Pattern:**
```markdown
## Table of Contents
- [Section Name](#section-anchor-id)

---

<a id="section-anchor-id"></a>

## Section Name
```

**Anchor ID rules:**
- Use lowercase only
- Replace spaces with hyphens
- Remove or simplify special characters (— becomes dash, & becomes ampersand, etc.)
- Keep IDs short and readable
- Example: `phase-1-planning-discovery-completed` not `phase-1-planning-discovery-completed-on-april-24`

**Obsidian note:** Obsidian auto-generates anchors from headings but does not consistently honor them when viewing markdown in other tools. Always use explicit HTML anchors for any TOC intended to work cross-editor.

**Markdown file version control:** As per project rules, commit markdown files each time they are updated. Do not leave markdown changes unstaged between sessions.

See `Shared_References/markdown-standards.md` for detailed examples, troubleshooting, and cross-editor compatibility notes.

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

### Theme Toggle

**All new calculator and reference HTML files must include a light/dark theme toggle.** This is a project-wide requirement.

- Set `data-theme="dark"` on the `<html>` element as the default.
- Place the toggle button in the page header alongside the title (use `page-header-inner` flex layout with `.header-text` and `.btn-theme`).
- Use the warm amber palette for light mode — defined in `Shared_References/html-css-style-guide.html` Section B.
- Use a unique `localStorage` key per file using the pattern `spark_theme_<context>` to avoid cross-page conflicts.
- Existing keys in use: `spark_theme` (dev calc), `spark_theme_prod` (prod calc), `spark_theme_phase1` (phase1 model), `spark_theme_styleguide` (style guide).

```js
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('spark_theme_<context>', theme);
  document.getElementById('btn_theme').textContent = theme === 'dark' ? '\u2600 Light' : '\u263e Dark';
}
function toggleTheme() {
  var current = document.documentElement.getAttribute('data-theme') || 'dark';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}
applyTheme(localStorage.getItem('spark_theme_<context>') || 'dark');
```

The `applyTheme()` call must run immediately (not inside DOMContentLoaded) to prevent a flash of the wrong theme on load.

**Style guide:** `Shared_References/html-css-style-guide.html` — global reference containing the complete CSS variable palette, component patterns, light/dark overrides, and JS patterns. Consult it instead of grepping existing calculators when building new files.

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

Required CSS (add to `<style>` block — copy from `calculators/Document/dev_cluster_math_reference.html`):
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

Infrastructure reservations per node: Proxmox 2c/8 GB, ZFS ARC —/8 GB (zfs_arc_max=8589934592), Ceph RGW 4c/8 GB, Ceph MON 2c/6 GB, Ceph OSD 1c/3 GB each, Ceph MGR 1c/2 GB (active Node01 · standby Node02/03). Total: **12c / 33 GB** per node · leaves 20c / 351 GB for VM allocation.
