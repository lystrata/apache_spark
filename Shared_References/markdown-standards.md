# Markdown Standards & Best Practices

_Reference guide for markdown document generation across this project_

---

## Table of Contents

- [Overview](#overview)
- [Table of Contents and Anchors](#table-of-contents-and-anchors)
- [Cross-Editor Compatibility](#cross-editor-compatibility)
- [Obsidian-Specific Notes](#obsidian-specific-notes)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

<a id="overview"></a>

## Overview

Markdown in this project is used for:
- Planning documents and TODOs
- Infrastructure specifications
- Phase planning and detailed task breakdowns
- Technical references

All markdown files are version-controlled and committed as they are updated. Markdown may be converted to PDF via Pandoc, so anchor/linking behavior must be consistent across multiple platforms.

---

<a id="table-of-contents-and-anchors"></a>

## Table of Contents and Anchors

### The Problem: Auto-Generated Anchors

Markdown editors auto-generate anchor IDs from heading text to enable internal linking. However, the generation rules differ across tools:

**Inconsistencies:**
- Emoji handling: Some editors strip emojis, others include them, others convert them
- Special characters: Em-dashes (—), ampersands (&), parentheses are handled differently
- Case conversion: Most convert to lowercase, but some don't
- Character replacement: Spaces → hyphens vs spaces → underscores varies
- URL encoding: Some editors percent-encode special chars, others don't

**Examples of the same heading generating different anchors:**
```
Heading: "## YAML ResourceManager HA (Active/Standby)"

GitHub:           #yaml-resourcemanager-ha-activstandby
Obsidian:         #yaml-resourcemanager-ha-activstandby
VS Code (ext):    #yaml-resourcemanager-ha--activstandby
Some renderers:   #yaml_resourcemanager_ha_activestandby
```

### The Solution: Explicit HTML Anchors

Use HTML anchor tags placed directly before the section heading:

```markdown
<a id="anchor-id-here"></a>

## Section Heading
```

**Why this works:**
- HTML is a standard; all markdown viewers/renderers understand `<a id="..."></a>` tags
- Pandoc preserves them for PDF generation
- No ambiguity in ID generation
- Works in Obsidian, GitHub, VS Code, browsers, PDF readers, etc.

---

<a id="cross-editor-compatibility"></a>

## Cross-Editor Compatibility

### Tested Platforms

| Platform | Auto-Anchor Support | Explicit Anchor Support | Notes |
|----------|---------------------|------------------------|-------|
| GitHub   | ✅ Works            | ✅ Works               | Auto-anchors reliable; explicit better for complex headings |
| Obsidian | ⚠️ Partial          | ✅ Works               | Auto-anchors generated but inconsistent in external viewers |
| VS Code  | ✅ Works            | ✅ Works               | With markdown preview extension |
| Pandoc   | ❌ Unreliable       | ✅ Works               | Converting MD → PDF; explicit anchors become PDF bookmarks |
| Browser  | ⚠️ Partial          | ✅ Works               | Depends on renderer; explicit always works |

### Recommendation

**Always use explicit HTML anchors** for any markdown document containing:
- Tables of contents
- Cross-references between sections
- Links intended to work across multiple platforms
- Documents that will be converted to PDF

---

<a id="obsidian-specific-notes"></a>

## Obsidian-Specific Notes

### Obsidian's Anchor Behavior

Obsidian auto-generates anchors from headings and displays them in the interface (the "link to heading" feature). However:

1. **Obsidian's auto-anchors are not reliable outside Obsidian.** When the markdown is viewed in GitHub, VS Code, or converted to PDF, Obsidian's auto-anchor IDs may not match the external renderer's IDs.

2. **Emoji handling:** Obsidian strips emojis from auto-generated anchors. A heading like `## 🔒 BLOCKER.1` becomes `#blocker1`, but GitHub might generate `#-blocker1`.

3. **Special characters:** Obsidian treats em-dashes and other special characters differently than GitHub's markdown parser.

### HTML Anchor Links in Obsidian

**Known limitation:** Obsidian does not reliably resolve HTML anchor tags (`<a id="..."></a>`) for internal linking, even after file reload or vault restart.

**Cross-platform compatibility matrix:**

| Viewer/Platform | HTML Anchors | Obsidian Native (`^anchor-id`) | Status |
|-----------------|--------------|--------------------------------|--------|
| Obsidian        | ❌ Broken    | ✅ Works                       | Obsidian plugin may fix |
| GitHub          | ✅ Works     | ⚠️ Displays as text            | HTML anchors recommended |
| VS Code         | ✅ Works     | ⚠️ Displays as text            | HTML anchors recommended |
| OneRead         | ✅ Works     | ⚠️ Displays as text            | HTML anchors recommended |
| Pandoc (PDF)    | ✅ Works     | ⚠️ Ignored                     | HTML anchors recommended |
| Browser Render  | ✅ Works     | ⚠️ Displays as text            | HTML anchors recommended |

**Recommendation:** Use **HTML anchors** (`<a id="..."></a>`) for documents that need broad compatibility across multiple platforms (GitHub, PDF, web, various markdown viewers). Accept that Obsidian TOC links will not work natively.

### Workaround for Obsidian Users

If you need TOC links to work in Obsidian:
1. Check for an Obsidian plugin that adds HTML anchor support (search Community Plugins for "anchor", "link", or "toc")
2. Alternative: Use Obsidian's native `^anchor-id` syntax, but note this breaks links in other viewers
3. Alternative: Use Obsidian's built-in "link to heading" feature (right-click headings) to create links, but manually maintain the TOC

**Trade-off:** Obsidian compatibility vs. broad cross-platform compatibility. This project prioritizes cross-platform compatibility.

---

<a id="examples"></a>

## Examples

### Example 1: Simple TOC

```markdown
# Phase 1–2 Infrastructure Plan

## Table of Contents

- [Phase 1](#phase-1-planning)
- [Phase 2](#phase-2-implementation)
- [Appendix](#appendix)

---

<a id="phase-1-planning"></a>

## Phase 1 — Planning & Discovery

Content here...

---

<a id="phase-2-implementation"></a>

## Phase 2 — Implementation

Content here...

---

<a id="appendix"></a>

## Appendix

Content here...
```

### Example 2: Nested Sections with TOC

```markdown
## Table of Contents

- [Main Topic](#main-topic)
  - [Subtopic A](#subtopic-a)
  - [Subtopic B](#subtopic-b)

---

<a id="main-topic"></a>

## Main Topic

<a id="subtopic-a"></a>

### Subtopic A

Content...

<a id="subtopic-b"></a>

### Subtopic B

Content...
```

### Example 3: Complex Headings with Special Characters

❌ **Don't do this** (auto-generated anchors unreliable):
```markdown
## YAML ResourceManager HA (Active/Standby) — Ksolves Documentation

See [YARN HA](#yaml-resourcemanager-ha-activstandby-ksolves-documentation) below.
```

✅ **Do this instead** (explicit anchor):
```markdown
<a id="yarn-ha-overview"></a>

## YAML ResourceManager HA (Active/Standby) — Ksolves Documentation

See [YARN HA](#yarn-ha-overview) below.
```

---

<a id="troubleshooting"></a>

## Troubleshooting

### TOC Links Don't Work

**Symptom:** Clicking a TOC link in markdown editor doesn't jump to the section.

**Diagnosis:**
1. **In Obsidian:** This is a known Obsidian limitation with HTML anchors. HTML anchors work in all other viewers (GitHub, VS Code, OneRead, browsers, PDF) but not natively in Obsidian.
2. In other editors: Check if you're using auto-generated anchors. They often fail with emojis or special characters.
3. Verify the anchor ID matches exactly (case-sensitive).
4. Check if the heading exists (typo in anchor ID).

**Solution:**
- **For cross-platform documents:** Use explicit HTML anchors `<a id="anchor-id"></a>`. They work everywhere except Obsidian. This is the recommended approach for project documents.
- **For Obsidian-only documents:** Use Obsidian's native `^anchor-id` syntax instead (but this breaks links in other viewers).
- **For Obsidian users on cross-platform docs:** Search Community Plugins for "anchor" or "link" support; a plugin may add HTML anchor resolution.
- Test the link in multiple editors (GitHub, VS Code, OneRead, browser) to confirm cross-platform compatibility.

### Emoji in Heading Breaks Anchors

**Symptom:** Heading like `## 🔒 BLOCKER.1` generates unpredictable anchor IDs across editors.

**Solution:**
- Use explicit anchor: `<a id="blocker1-remote-access"></a>`
- Place it above the heading with the emoji
- The emoji stays in the heading; the anchor ID is simple and predictable

### Links Work in Obsidian but Not in GitHub

**Symptom:** TOC links work fine in Obsidian, but broken on GitHub.

**Cause:** Obsidian's auto-generated anchors don't match GitHub's markdown parser.

**Solution:**
- Use explicit HTML anchors instead
- They work in Obsidian AND GitHub (and everywhere else)

### PDF Conversion Loses Anchor Links

**Symptom:** When converting markdown to PDF with Pandoc, internal links don't work.

**Cause:** Auto-generated anchors may not survive the conversion, or the ID format changes.

**Solution:**
- Use explicit HTML anchors in markdown
- **Use Pandoc's `--toc` flag when generating PDFs** — this automatically generates a clickable table of contents (bookmarks/outline) from markdown headings
- The `--toc` flag is the recommended approach for PDF generation from markdown

**Standard Pandoc command:**
```bash
pandoc input.md -o output.pdf --toc --pdf-engine=lualatex -V geometry:margin=1in
```

**Result:** PDF includes clickable bookmarks/outline with all headings, no manual anchor maintenance needed.

---

## Related Resources

- **CLAUDE.md** § Markdown Documents — Project rules and quick reference
- **CLAUDE.md** § Editing Rules — Version control and file management
- **Pandoc Documentation** — https://pandoc.org/MANUAL.html#extension-bracketed_spans (for cross-format compatibility)

---

_Last updated: April 24, 2026_  
_Based on cross-editor testing across Obsidian, GitHub, VS Code, and Pandoc_
