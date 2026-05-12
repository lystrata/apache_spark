
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
| `correspondence/Document/` | Working drafts of correspondence (in-progress letters, doc preparation) |
| `correspondence/Notes/` | Planning and notes for correspondence context |
| `correspondence/Ready_For_Review/` | Staging for correspondence documents |
| `correspondence/Incoming/` | Raw source material (PDFs, attachments, files received via other channels) |
| `correspondence/Received/` | Inbound emails / letters from external parties (replies, vendor responses) |
| `correspondence/Sent/` | Outbound emails / letters that have been delivered |
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

## Verifying External Assertions

Applies to **all assertions of external fact** in any context — what a standard says, how a tool behaves, what a vendor product does, what industry practice is, etc. Strengthens and operationalizes the Citation Rules above.

**Rule:** No assertion of external fact without verified correlation to an authoritative external source.

**Verification mechanism:** Always verify via WebFetch (or `curl` + a parser for non-HTML resources). Search-engine snippets and AI-summarized previews are starting points, not verification. For PDFs, extract to text (`pdftotext`) and grep for the cited passage to confirm it appears verbatim in the source.

**Verbatim quotes** must appear verbatim in the source. Paraphrase is acceptable when not framed as a quote. Paraphrase-creep — a quote acquiring words or phrasing not present in the source — is a frequent failure mode; guard against it by direct text-level verification, especially before a document leaves the team.

**Failure modes — state explicitly, no hedging:**

- **Cannot verify** (paywalled, authentication-walled, URL doesn't resolve, cited text not located in the source): state *"I cannot find corroborated evidence for this claim"* and either drop the assertion or flag it as unverified.
- **Don't know** (the relevant knowledge is simply not held): state *"I don't know"* and stop. Do not fill the gap with plausible-sounding language.

There is no shame in admitting uncertainty. The cost of "I don't know" is small; the cost of an unsupported assertion that later proves wrong — particularly one that travels up an organizational chain — is high.

This rule is strict for **security-context documents** and applies in all contexts. "Industry research suggests" and similar hedge-phrases are not substitutes for verified sources; if the verification cannot be done, the claim does not appear in the document.

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

## Critical Path Document Synchronization

Applies to **all contexts**. Whenever new operational data is captured — meeting outcomes, vendor responses, decisions, status changes, infrastructure events, scope corrections, topology changes — **check every Critical Path document to determine which need updating, then update them in the same work cycle.** Don't capture an event in one place and let the others go stale; CP docs that drift become unreliable.

**Critical Path documents in scope (current as of 2026-05-08; verify the version number is current at edit time):**

| Document | Path | Type |
|---|---|---|
| Main Critical Path | `phases/development/phase2/Document/Phases_Critical_Path_Development_v1.x.md` | Versioned distribution doc |
| Visual Tracker (HTML) | `phases/development/phase2/Document/phases_critical_path_development_tracker_v1.x.html` | Versioned, lockstep with main |
| HIPAA sub-project | `phases/development/phase2/Document/CP_HIPAA_Compliance_v1.x.md` | Versioned distribution doc |
| Okta sub-project | `phases/development/phase2/Document/CP_Okta_v1.x.md` | Versioned distribution doc |
| Airflow host briefing (companion) | `phases/development/phase2/Document/MSB-PMC01_airflow_host_briefing_v1.x.md` | Versioned companion doc |
| SOW timeline tracker | `phases/development/phase2/Document/SOW_timeline_status.md` | In-place operational |
| Vendor-isolation planning note | `security/Notes/vendor-access-isolation-plan_2026-05-06.md` | On-site planning (not git-tracked) |
| Production CP fork | `phases/production/phase2/Document/Phases_Critical_Path_Production_v0.x.md` | Versioned distribution doc |
| Master TODO | `TODO.md` | In-place operational index |

**For each new piece of operational data:**

1. **Identify** which CP documents the data affects. Most data lands in one doc primarily but ripples to others — a vendor email may close a TODO item, change a BLOCKER status in the main CP, change a sub-task in a planning note, and need a cross-reference in a sub-project. The default assumption is "more than one document needs touching" — verify before assuming "only one".
2. **Update each affected document.** For versioned distribution docs, prefer in-place edits during a working cycle and bump the version at the natural cut point (per the Document Versioning rule). For in-place operational files (TODO.md, README.md, SOW_timeline_status.md, planning notes), edit immediately.
3. **Refresh cross-references.** When one document changes, others that reference it may need their cross-refs bumped. Use `grep -rln <basename>_v` (or equivalent) to find them.
4. **Mirror structural changes** between paired documents (e.g., main CP § BLOCKER.4 ↔ `security/Notes/vendor-access-isolation-plan_2026-05-06.md` should carry compatible sub-task tables and owner sections; updating one without the other creates drift).

**When this applies (not exhaustive):**

- A meeting summary or correspondence captures a decision (CIO call, vendor sync, internal team call)
- A vendor sends a response or update (email, status report, technical document)
- An infrastructure event lands (provisioning complete, blocker resolved, new gate added, hardware spec change)
- A scope correction or topology change is decided
- A new task family is identified or an existing task is completed/closed
- A version-controlled artifact (calculator, model) gets a behavior or default change

**When in doubt, ask:** "Which Critical Path documents does this data belong in?" — and treat the answer as "these N docs, in this order" rather than "this one doc". The audit trail and decision history depend on consistency across the set.

---

## Serving the Calculators

Always serve via HTTP, not `file://`. localStorage scoping differs between origins and scenarios saved under one will be invisible to the other.

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/calculators/Document/production_spark_calculator.html` or the dev equivalent.

## PDF Generation from Markdown

When converting markdown documents to PDF using Pandoc, always include the `--toc` flag to generate a clickable table of contents in the PDF (appears as bookmarks/outline in PDF readers). When the source markdown contains GFM checkboxes, also pass `--from=markdown+task_lists` so they render as real checkbox glyphs.

**Preferred invocation (use this):**
```bash
Scripts/regenerate_pdf.sh <input.md> [<output.pdf>]
```

The script wraps the standard command below. Output path defaults to the input path with `.md` swapped for `.pdf` in the same directory; pass an explicit second argument for a non-standard location. The script reports the resolved input → output paths and the generated PDF's byte count.

**Why prefer the script:** the raw `eval "$(brew shellenv)" && ...` form below trips Claude Code's bash parser (`"Contains shell syntax that cannot be statically analyzed"`) and triggers a permission prompt every time. The script's invocation form parses cleanly without a prompt.

**Standard command (what the script wraps; use directly only if the script is unavailable):**
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
- `Phases_Critical_Path_Development_v1.3.md` and `Phases_Critical_Path_Development_v1.3.pdf`
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

## File Naming — Embedded Date

Files we author should embed the date of authorship in the filename, immediately before the extension, in ISO format. This makes files easier to find via timeline, prevents collisions when topics recur, and gives a quick read of "how recent is this?" without opening it.

**Format:** `<basename>_<YYYY-MM-DD>.<ext>`

**Examples:**
- `dev_data_flow_diagram_2026-05-06.png`
- `spark_vm_management_ips_2026-05-06.png`
- `msb-pmc01-04_resource_analysis_2026-05-06.md`
- `vendor-access-isolation-plan_2026-05-06.md`

**Applies to:**
- Notes files — planning, analysis, design proposals, meeting captures
- Reference images and source captures (e.g., files in `reference_images/`)
- Any file where a date helps disambiguation when grepping or browsing

**Does NOT apply to:**
- **Versioned distribution documents** — they use `_v<MAJOR>.<MINOR>` per the Document Versioning section above. Version is the identifier; the body's `_Last updated_` line carries the date.
- **Operational / index files** edited in place — `CLAUDE.md`, `MEMORY.md`, `TODO.md`, `README.md`, `index.html`.
- **Vendor-supplied files in `Incoming/`** — we don't rename their files. (Once promoted to `reference_images/` or another tracked location, give them descriptive + dated names.)
- **Rolling files** that accumulate over time — e.g., `questions_for_vendors.txt`. These are not point-in-time snapshots.
- **Changelog files** that are already tied to a version — e.g., `..._v1.0_changelog.md`. The version pins the moment.

**Significant later rewrites:** if a file's content evolves substantially after creation, `git mv` it to embed the new date. Update any cross-references. For minor edits, keep the original date — the body's revision history captures the change history.

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

### Push Workflow — One-Word Trigger

When the user types `push` (or any clear instruction to push — `git push`, `push it`, `push commits`, etc.), run the following sequence:

1. `git log --oneline origin/main..HEAD` — show the user what's about to be pushed (one line per commit)
2. `git push origin main` — push to the canonical remote
3. Report the ref-update line from the push output (e.g., `0683052..1eb6d78  main -> main`)

If nothing is ahead of `origin/main`, skip the push and report "in sync (0 commits ahead)" rather than running a no-op.

The `Bash(git push:*)` deny was lifted 2026-05-08; absent that deny, the one-word trigger is the simplest workflow. If the deny rule is restored later, this convention still describes the intended behavior — the user types `push`, and (under the current permissions) the push happens; under restored deny, the user types `! git push origin main` themselves and the same result lands. Either way, the trigger word is `push`.

**Scope:** the rule defaults to `git push origin main`. For non-default cases (push to a different remote, force-push, push tags, push a different branch) the user should be explicit; do not assume.

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
nano ~/.config/spark-hooks/patterns   # one pattern per line
chmod 600 ~/.config/spark-hooks/patterns
```

#### Step 2 — Install the hook

The hook is not tracked by git. On a fresh clone, copy `.git/hooks/pre-commit` from an existing installation and make it executable:

```bash
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
- `phases/development/phase1/deliverables/dev_cluster_phase1_model.html` — section id `sec_revisions`

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

### Self-Contained HTML — Mandatory

**Rule (project-wide, all HTML output):** every HTML file produced or maintained in this project must be **self-contained** — CSS, JavaScript, and any in-document images must be inlined or data-URI embedded, not loaded via external `<link>`/`<script src="...">`/`<img src="external/...">` references.

The native working HTML files (calculators, tracker, references, calculator guide, phase model deliverables, compliance frameworks reference) already follow this — they're single-file HTML/CSS/JS with no external dependencies (per the existing Calculator Architecture rule: "Both calculators are single-file HTML/CSS/JS with no external dependencies and no build step").

**Why mandatory:** any HTML in this project is a candidate for emailing as an attachment, opening from a thumb drive, viewing offline, or being archived for HIPAA / SOC 2 audit. External resource references break in any of those scenarios — the recipient sees an unstyled mess. Self-contained HTML keeps each file shippable as a single artifact.

**For pandoc-rendered Markdown → HTML:** always pass `--embed-resources` (modern pandoc; older releases used `--self-contained`). Combined with `--standalone` and a `--css=<path>` argument, pandoc will inline the CSS contents into a `<style>` block rather than emit a `<link rel="stylesheet">` tag. Verify with `grep -c 'rel="stylesheet"' <output.html>` — should be `0`.

**For hand-built HTML:** include the CSS in a `<style>` block in the document `<head>`; do not link to an external CSS file. The same applies to JS — `<script>` blocks inline only.

**Exception (none):** there is no exception. If a file is too large for inlining (e.g., a 1 MB JS library), reconsider whether it belongs in this project's HTML at all; HIPAA-scope artifacts should not depend on external CDNs in any case.

**Verification:** after rendering or editing any HTML, check there are zero `<link rel="stylesheet"` and zero `<script src="..."` references that point to a path outside the document. Inline references (anchor `#fragment` links to in-document IDs) are fine and expected.

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
    <div class="section-close"><a onclick="closeSub(this)">&#x25B2; Close section</a></div>
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

### Global & Scoped Open/Close Controls

Every HTML page that uses the section + sub-section pattern must include both:

**Page-level (global) controls** — two buttons in the page header alongside the theme toggle: `▾ Expand all` and `▴ Collapse all`. They toggle every `<details class="section-details">` only — sub-sections inside are not touched, so any sub-section state the user has set is preserved when sections are reopened.

**Section-level (scoped) controls** — within each main section that contains sub-sections, a two-link strip at the top of the `section-body`, above the first sub-section: `▾ Open all sub-sections · ▴ Close all`. Each strip operates only on `details.sub-details` within its parent main section — it never cascades to sibling sections. Sections that contain only cards (no `sub-details`) — like a pure Overview section — omit the scoped strip.

Required JS functions (`expandAllSections`, `collapseAllSections`, `expandSubs(el)`, `collapseSubs(el)`) and the corresponding HTML/CSS (`div.page-header-buttons`, `div.sub-controls`) are in `Shared_References/html-css-style-guide.html` Section B — copy from there, not from other calculators.

### Theme Toggle

**Scope — applies to interactive / reference / tracker HTML, not email-bound HTML.**

In scope (must include the toggle):
- All HTML in `calculators/Document/` — calculators, guides, references, models, research summaries, glossaries, flow diagrams, the index
- All HTML in `phases/<phase>/<env>/Document/` — Critical Path trackers, sub-project trackers, profile pages, deliverable models
- Any new interactive tool, reference, model, or tracker added in a fork's `Document/` directory

Out of scope (no toggle):
- HTML email bodies and attachments under `ready_for_delivery/` — they target Outlook MSO renderer; theme toggling is a recipient-runtime concern that does not apply (see *Email HTML Styling — Outlook-Safe Profile* below)
- One-off recipient-specific drafts (e.g., `vendor-letter-draft.html`) where the document is going to be rendered once and shipped, not re-opened by the user
- Operational source files in `Notes/` or `Incoming/`

**Implementation:**

- Set `data-theme="dark"` on the `<html>` element as the default.
- Place the toggle button in the page header alongside the title (use `page-header-inner` flex layout with `.header-text` and `.btn-theme`).
- Use the warm amber palette for light mode — defined in `Shared_References/html-css-style-guide.html` Section B.
- Use a unique `localStorage` key per file using the pattern `spark_theme_<context>` to avoid cross-page conflicts.
- Existing keys in use: `spark_theme` (dev calc), `spark_theme_prod` (prod calc), `spark_theme_phase1` (phase1 model), `spark_theme_styleguide` (style guide).
- `applyTheme()` must be called immediately on script load (not inside DOMContentLoaded) to prevent a flash of the wrong theme.

Full JS implementation (`applyTheme`, `toggleTheme`) is in `Shared_References/html-css-style-guide.html` Section B — the canonical reference for the CSS variable palette, component patterns, and light/dark overrides. Consult it instead of grepping existing calculators when building new files.

### Sub-Section Pattern (within a section)

When a section has multiple named sub-topics, convert them to nested collapsibles using `sub-details`. Sub-sections default closed (the parent `DOMContentLoaded` handler closes `details.section-details` only; sub-details are closed by the browser's default since they have no `open` attribute). The close link uses `closeSub()` to collapse the `<details>` while keeping the user's eye stable: it captures the click's viewport Y, closes, then scrolls so the now-collapsed summary lands at the same viewport position the close link occupied. This compensates for the document-shrink jump that browsers don't always anchor away — important for `file://` distribution and deeply nested collapses. The same `closeSub()` is used for **both** sub-section close and main-section close — replace any inline `<a onclick="closeSub(this)">` with `<a onclick="closeSub(this)">`.

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
  // Position-preserving close — keeps user's eye stable when document shrinks
  var clickY = el.getBoundingClientRect().top;
  var d = el.closest('details');
  d.open = false;
  var summary = d.querySelector(':scope > summary');
  if (summary) {
    var summaryY = summary.getBoundingClientRect().top;
    if (summaryY < clickY) window.scrollBy(0, summaryY - clickY);
  }
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

`Scripts/check_fqdn.sh` — sanitization-pattern check for one or more files. Reads patterns from `~/.config/spark-hooks/patterns` (the same private patterns file used by the pre-commit hook), grep-checks each given file case-insensitively, and prints matches with `filename:line:content`. Use this before staging any new or edited file to confirm no corporate identifiers leaked. Usage: `./Scripts/check_fqdn.sh <file> [<file> ...]`. Exit code 0 always (script reports findings; doesn't fail the shell).

## Project-Local Temporary Files

Use `/Users/rohn/Serve/tmp/` for any temporary / scratch / helper files (Python helper scripts, intermediate outputs, sanity-check artifacts). Do **not** write to system `/tmp/` — that's outside the project directory and explicitly excluded from the project's permission posture.

The `tmp/` directory is gitignored (entry added 2026-05-07). Files in it are local-only; safe to leave between sessions or delete at will.

## Correspondence Lifecycle — `correspondence/Document/`, `correspondence/Sent/`, `correspondence/Received/`

The four `correspondence/<sub>/` directories track different lifecycle stages of inbound and outbound correspondence:

- **`correspondence/Document/`** — working drafts (in-progress letters, multi-revision documents, anything still being written or refined). Status header at the top of each file tracks state: `Draft`, `Approved YYYY-MM-DD`, `Sent YYYY-MM-DD`, etc.
- **`correspondence/Sent/`** — outbound emails / letters that have been delivered to a recipient. Move (or copy) the canonical source from `Document/` to `Sent/` once the message is actually transmitted. The Status header should read `Sent YYYY-MM-DD — awaiting recipient response` (or similar).
- **`correspondence/Received/`** — inbound emails / letters from external parties (vendor replies, partner responses, signed documents coming back). File these here when they land, separate from raw source material like PDFs or attachments.
- **`correspondence/Incoming/`** — raw source material received via other channels (full PDFs, attachments, dump files, transcripts). Different from `Received/`: `Incoming/` is where the unstructured stuff lands; `Received/` is where the typed-out / transcribed inbound emails live.

**Naming:** all files in `Sent/` and `Received/` follow the project file naming rule with the date embedded (`<basename>_<YYYY-MM-DD>.<ext>`). The basename should match the original source in `Document/` so the pairing between draft and sent / received state is obvious.

**Migration of existing files (optional, on direction):** as of 2026-05-08 the existing inbound/outbound emails in `correspondence/Document/` (Sean / Austin replies; alignment emails; vendor letters; the audit thread) have not been moved into `Received/` and `Sent/`. They can stay in `Document/` with their `Status: Sent` / `Status: Received` headers, or be moved later — directional call. New correspondence going forward should land in the appropriate lifecycle directory.

**Audit trail:** every `Sent/` artifact pairs with a corresponding `ready_for_delivery/<basename>_<YYYY-MM-DD>.<ext>` git commit (the rendered version that was actually sent — see below). Together they give a "what we drafted" + "what we sent" record.

## Email-Bound Documents — `ready_for_delivery/`

`/Users/rohn/Serve/ready_for_delivery/` is the staging location for documents that are about to be sent (email attachments, cover-letter HTML, signed copies, etc.). Anything in this folder is:

- **Send-ready** — final form, no `[placeholder]` substitutions left to do (or any remaining substitutions are explicitly noted at the top), no internal-tracking appendices, sanitized per the project's FQDN rule
- **Self-contained** per the HTML rule above (CSS/JS inlined; no external resource refs)
- **Outlook-safe when the format calls for it** — for HTML email *bodies* (not attachments), use Outlook MSO-compatible HTML: inline styles only, table-based layout, web-safe fonts (Calibri / Segoe UI / Arial / Helvetica fallback chain), no flex/grid, no CSS variables
- **Tracked in git** — keeps an audit trail of what was actually sent (and when, via the commit timestamp). The rendered HTML is the recipient-visible artifact; the source markdown lives in `correspondence/Document/` for revision history but the `ready_for_delivery/` HTML is what the recipient saw.

**Workflow:**

1. Draft the source markdown in `correspondence/Document/<basename>_<YYYY-MM-DD>.md` (the canonical, revisable form)
2. Render to HTML in `ready_for_delivery/<basename>_<YYYY-MM-DD>.html` when approved for send
3. Send the email; attach / paste the rendered HTML as appropriate
4. Commit the `ready_for_delivery/` artifact to record what was sent
5. Source markdown stays in `correspondence/Document/` (where revisions / status updates continue to land if a follow-up is needed)

**Naming:** same date-embedded convention as the rest of the project — `<basename>_<YYYY-MM-DD>.<ext>`. The basename should match the source markdown so the pairing is obvious.

**Two HTML profiles to know:**

- **Self-contained-and-rich** (the project default): pandoc `--standalone --embed-resources` rendering with the full `html_review/style.css` palette inlined. Use this for *attachment* HTMLs the recipient opens in a browser — the audit-findings HTML is an example.
- **Outlook-safe**: hand-built HTML with inline styles only, tables for layout, web-safe fonts. Use this for the *email body* (cover letter HTML the recipient sees in Outlook compose / mail client). Outlook MSO renderer doesn't support modern CSS (no flex, no grid, no variables) so the styling has to stay conservative. See *Email HTML Styling — Outlook-Safe Profile* below for the full ruleset.

---

## Email HTML Styling — Outlook-Safe Profile

Applies to **all HTML email bodies** authored in this project — vendor-bound, internal-bound, partner-bound, single-recipient or distribution. The Outlook MSO (Microsoft Office HTML) renderer is the lowest-common-denominator across business mail clients; styling that survives MSO will also render correctly in Apple Mail, Gmail web, Outlook web, and most mobile clients.

**This rule is generic and recipient-agnostic** — do not hand-roll variants per recipient. One profile, applied uniformly.

### What "email body" means here

The HTML that the recipient **pastes into the compose window** or that their mail client renders inline. This includes:

- Cover-letter HTML for a vendor or internal sync
- Inline emails composed from a markdown source in `correspondence/Document/`
- Any HTML in `ready_for_delivery/` whose intended use is the email *body*, not an attachment

It does **not** include:

- HTML *attachments* the recipient opens in a browser (those use the self-contained-rich profile)
- Internal HTML (calculators, references, trackers) which use the project's CSS-variable palette and theme toggle

### MSO-safe ruleset (mandatory for email bodies)

1. **Inline styles only.** No `<style>` blocks, no external CSS, no class-based selectors. Every styling directive lives in a `style="..."` attribute on the element it styles. (MSO ignores `<style>` rules in many configurations; class selectors are stripped intermittently.)

2. **Table-based layout.** Use `<table>` / `<tr>` / `<td>` for any multi-column or boxed layout. No `<div>`-based flex or grid. Set `cellpadding="0" cellspacing="0" border="0"` on layout tables and use inline `padding`/`margin` on cells.

3. **Web-safe font fallback chain.** Use `font-family: Calibri, 'Segoe UI', Arial, Helvetica, sans-serif;` on every text-bearing element. Do not specify Google Fonts, Cascadia Code, Fira Mono, or any font not present on stock Windows + macOS. (Spark project's native HTMLs use Cascadia Code with stack fallback — that's fine for native HTML, **not** fine for email.)

4. **No CSS variables.** MSO does not resolve `var(--name)`. Hard-code every color, every dimension. (This is the cost of recipient-agnostic styling — the source-of-truth color values from `html-css-style-guide.html` get copy-pasted as hex literals into each email body.)

5. **No flex / no grid / no modern positioning.** No `display: flex`, no `display: grid`, no `position: absolute`. Layout is tables-and-floats only. (Some clients support modern layout, but a non-zero share don't, and email *must not* degrade based on client.)

6. **Hex colors, not named or HSL.** `#1a1a1a` not `dimgray` or `hsl(0,0%,10%)`. (Named colors are fine, but consistency is the rule and hex is the universal lingua franca.)

7. **Inline images.** Either embed as `data:image/...;base64,...` URIs (MSO renders these inline) or skip them. Do not link to remote `<img src="https://...">` — many clients block remote-image fetch by default and the recipient sees a "show images" prompt or a broken-image icon.

8. **No JavaScript.** Mail clients strip `<script>` unconditionally. Anything interactive is impossible; all logic must be expressed as static HTML.

9. **Conservative max-width.** Constrain the body table to ~600–680 px max width using `style="max-width:680px"` or a fixed `width="680"`. Outlook + many mobile clients render the body inside a narrow column; wide tables break or scroll horizontally.

10. **No theme toggle, no dark mode CSS.** The recipient's mail client decides light/dark. Author one styling — the high-contrast neutral version (dark text on light background) — and let the client invert if it wants. Do not include `data-theme` attributes or a `[data-theme="light"]` block.

### Skeleton template

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Subject Line</title></head>
<body style="margin:0; padding:20px; font-family: Calibri, 'Segoe UI', Arial, Helvetica, sans-serif; color:#1a1a1a; background:#ffffff;">
  <table cellpadding="0" cellspacing="0" border="0" style="max-width:680px; width:100%;">
    <tr><td style="padding:0 0 12px 0; font-size:14px; line-height:1.5;">
      <p style="margin:0 0 12px 0;">Hi <Name>,</p>
      <p style="margin:0 0 12px 0;">Body paragraph 1.</p>
      <p style="margin:0 0 12px 0;">Body paragraph 2.</p>
    </td></tr>
    <tr><td style="padding:8px 0; font-size:13px; line-height:1.4; color:#444444; border-top:1px solid #cccccc;">
      <p style="margin:0;">Regards,<br>Rohn</p>
    </td></tr>
  </table>
</body>
</html>
```

### Verification

After authoring an email-body HTML, verify:

- Zero `<style>` blocks: `grep -c '<style' <file>` → `0`
- Zero `<script>` blocks: `grep -c '<script' <file>` → `0`
- Zero `var(--...)` references: `grep -c 'var(--' <file>` → `0`
- Zero `display: flex` / `display: grid`: `grep -cE 'display: ?(flex|grid)' <file>` → `0`
- Web-safe font chain present: `grep -c "Calibri.*Segoe UI.*Arial" <file>` → `1+`

### Reference

`Shared_References/html-css-style-guide.html` Section B carries the project's color palette in CSS-variable form for native HTML. When adapting for email bodies, copy the relevant hex values out of that section and inline them — do not link to or import the style guide.

---

## Hardware Reference

| | Production | Development |
|---|---|---|
| Nodes | 3 | 3 |
| Cores/node | 64 (2× 32c, dual NUMA) | 32 (1× 32c, single NUMA) |
| RAM/node | 768 GB (24× 32 GB DIMMs) | 320 GB (10× 32 GB DIMMs) |
| NVMe/node | 9× 3.2 TB | 7× 3.84 TB |
| SSD/node | 3× 480 GB (ZFS mirror + hot spare) | 3× 480 GB |
| RAM slider step | 32 GB (one DIMM) | 32 GB |

Infrastructure reservations per node: Proxmox 2c/8 GB, ZFS ARC —/8 GB (zfs_arc_max=8589934592), Ceph RGW 4c/8 GB, Ceph MON 2c/6 GB, Ceph OSD 1c/3 GB each, Ceph MGR 1c/2 GB (active Node01 · standby Node02/03). Total: **12c / 33 GB** per node · leaves 20c / 351 GB for VM allocation.
