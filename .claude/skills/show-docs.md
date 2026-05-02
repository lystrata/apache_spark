Inventory all HTML, PDF, and Markdown documents in the project, grouped by context, with type, size, last-modified, and staging status.

Optional argument narrows the scope:
- A context name — `calculators`, `remote_services`, `security`, `correspondence`, `phases`, `Shared_References`, `Scripts`
- A type — `html`, `pdf`, `md`
- `staged` — only files under any `Ready_For_Review/` directory
- `current` — only files under any `Document/` directory
- `tree` — render as an indented path tree instead of grouped tables

If no argument is given, show everything grouped.

Steps:

1. Enumerate matching files via a single `find`. Excludes are non-negotiable: `.git/`, `.obsidian/`, `.claude/`, `.trash/`, `node_modules/`, `.claudecheckpoints/`. Use `-printf` to capture mtime (as `YYYY-MM-DD`), size, and path in one pass:
   ```bash
   find . -type f \( -name "*.html" -o -name "*.pdf" -o -name "*.md" \) \
     -not -path "./.git/*" -not -path "./.obsidian/*" -not -path "./.claude/*" \
     -not -path "./.trash/*" -not -path "./node_modules/*" \
     -not -path "./.claudecheckpoints/*" \
     -printf "%TY-%Tm-%Td\t%s\t%p\n" 2>/dev/null | sort -k3
   ```
2. Run `git ls-files` once and use the result to mark any path *not* in the tracked set with `⚠️` in the output (it's a working copy, not committed).

3. Apply the user's filter argument before grouping (skip non-matching files entirely).

4. Group results first by top-level directory (the first path component after `./`). Within each group, sub-group by canonical sub-folder using these icons:
   - `Document/` → ✅ Live
   - `Ready_For_Review/` → 🟡 Staged
   - `Notes/` → 🗒 Notes
   - `Incoming/` → 📥 Incoming
   - `Images/` → 🖼 Images
   - `deliverables/` → 📦 Deliverables
   - `vendor_comms/` → ✉️ Vendor comms
   - anything else → 📁 Other

5. Render each non-empty sub-group as a Markdown table with columns: **File** · **Type** · **Size** · **Updated** · **⚠** (only filled for untracked rows). File path shown relative to the sub-folder root; type as `HTML`/`PDF`/`MD`; size human-readable (KB or MB); updated as `YYYY-MM-DD`.

6. Top of the output: a one-line summary — `N files: H HTML · P PDF · M MD`. Then per-context counts as section headers: `## calculators (15 files)`.

7. Cap each individual table at 30 rows. If exceeded, show the first 25 and append `(+N more — narrow with a filter arg, e.g. /show-docs <context>)`.

8. If the user passed `tree`, skip tables entirely. Output a single indented tree of paths sorted lexicographically; no size or date columns.

Be terse. The goal is a single scannable view, not a verbose report. Don't add commentary unless the user asks. Don't suggest follow-up actions unless something is genuinely anomalous (e.g., a `Ready_For_Review/` that's been non-empty for >7 days, suggesting a missed promotion).
