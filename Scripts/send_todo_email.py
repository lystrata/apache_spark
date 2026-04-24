#!/usr/bin/env python3
"""Send TODO.md as formatted plain-text email via macOS Mail.app."""

import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

EMAIL_FILE = Path.home() / ".config/spark-hooks/todo-email"
TODO_FILE  = Path(__file__).parent.parent / "TODO.md"

# ── organize checked items to Completed ──────────────────────────────────────

def reorganize_todo(md: str) -> str:
    """Move all checked items not in Completed section to Completed."""
    lines = md.splitlines()

    # Find where Completed section starts
    completed_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^## Completed", line):
            completed_idx = i
            break

    # Collect checked items that appear BEFORE Completed section
    checked_outside = []
    active_lines = []

    for i, line in enumerate(lines):
        # If we've reached Completed section, keep the header and everything after
        if completed_idx is not None and i >= completed_idx:
            active_lines.append(line)
            continue

        # Before Completed section: extract checked items, keep unchecked items
        m = re.match(r"^- \[x\] (.*)", line, re.IGNORECASE)
        if m:
            checked_outside.append(f"- [x] {m.group(1)}")
            continue
        active_lines.append(line)

    # If no Completed section exists, add it
    if completed_idx is None:
        active_lines.extend(["", "---", "", "## Completed"])

    # Add collected checked items after Completed header
    if checked_outside:
        if completed_idx is not None:
            # Items already in active_lines after the header; append new ones
            active_lines.append("")
        for item in checked_outside:
            active_lines.append(item)

    return "\n".join(active_lines)

# ── inline markdown stripping ─────────────────────────────────────────────────

def _strip(s: str) -> str:
    s = re.sub(r"`([^`]+)`",        r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*",  r"\1", s)
    s = re.sub(r"_([^_\s][^_]*)_",  r"\1", s)
    return s

# ── markdown → plain text ─────────────────────────────────────────────────────

_H1_RULE = "━" * 50
_H2_RULE = "─" * 40

def md_to_text(md: str) -> str:
    lines = md.splitlines()
    out   = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("")
            in_ul = False

    for raw in lines:
        line = raw.rstrip()

        # Skip horizontal rules — sections provide their own spacing
        if re.fullmatch(r"-{3,}", line):
            close_ul()
            continue

        # H1
        m = re.match(r"^#{1}\s+(.*)", line)
        if m:
            close_ul()
            out.extend(["", _strip(m.group(1).strip()).upper(), _H1_RULE])
            continue

        # H2
        m = re.match(r"^#{2}\s+(.*)", line)
        if m:
            close_ul()
            out.extend(["", _strip(m.group(1).strip()).upper(), _H2_RULE])
            continue

        # H3
        m = re.match(r"^#{3}\s+(.*)", line)
        if m:
            close_ul()
            out.append(_strip(m.group(1).strip()) + ":")
            continue

        # Checked item  - [x]
        m = re.match(r"^- \[x\] (.*)", line, re.IGNORECASE)
        if m:
            in_ul = True
            out.append(f"  ✓  {_strip(m.group(1))}")
            continue

        # Unchecked item  - [ ]
        m = re.match(r"^- \[ \] (.*)", line)
        if m:
            in_ul = True
            out.append(f"  ☐  {_strip(m.group(1))}")
            continue

        # Plain bullet  -
        m = re.match(r"^- (.*)", line)
        if m:
            in_ul = True
            out.append(f"  •  {_strip(m.group(1))}")
            continue

        # Standalone bold label  **text:**
        m = re.match(r"^\*\*(.+)\*\*$", line)
        if m:
            close_ul()
            out.extend(["", m.group(1)])
            continue

        # Blank line
        if not line:
            close_ul()
            out.append("")
            continue

        # Paragraph fallback
        close_ul()
        out.append(_strip(line))

    close_ul()

    today_str = date.today().strftime("%A, %B %-d, %Y")
    return today_str + "\n\n" + "\n".join(out).strip() + "\n"

# ── send via Mail.app ─────────────────────────────────────────────────────────

def send(to_addr: str, subject: str, body: str) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as f:
        f.write(body)
        tmp = f.name

    safe_to      = to_addr.replace("\\", "\\\\").replace('"', '\\"')
    safe_subject = subject.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
set bodyContent to do shell script "cat {tmp}"
tell application "Mail"
    set msg to make new outgoing message with properties {{subject:"{safe_subject}", content:bodyContent, visible:false}}
    tell msg
        make new to recipient at end of to recipients with properties {{address:"{safe_to}"}}
    end tell
    send msg
end tell
'''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"osascript error:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)
    finally:
        os.unlink(tmp)

# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not EMAIL_FILE.exists():
        sys.exit(f"Error: email address file not found — {EMAIL_FILE}")
    to_addr = EMAIL_FILE.read_text().strip()
    if not to_addr:
        sys.exit("Error: email address file is empty")

    if not TODO_FILE.exists():
        sys.exit(f"Error: TODO.md not found — {TODO_FILE}")

    today_str = date.today().strftime("%A, %B %-d, %Y")
    subject   = f"Daily TODO — {today_str}"

    # Read TODO.md and reorganize (move checked items to Completed)
    todo_content = TODO_FILE.read_text()
    todo_organized = reorganize_todo(todo_content)
    body = md_to_text(todo_organized)

    send(to_addr, subject, body)
    print(f"Sent to {to_addr}")

if __name__ == "__main__":
    main()
