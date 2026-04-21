Scaffold a new collapsible section in the current HTML file following the project's established section pattern.

Ask the user for:
1. Section letter (A, B, C…)
2. Section title
3. Section subtitle/description line
4. Target file and insertion point (after which existing section)

Then generate the correct HTML using this exact pattern from CLAUDE.md:

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

Rules:
- `id` must be `sec_` followed by a short lowercase identifier matching the section letter or topic
- Section defaults closed — the DOMContentLoaded handler in the file handles this automatically
- If the file has a Revisions section, flag that it will need updating after content is added
- Back up the file with a pre-edit git commit before inserting
