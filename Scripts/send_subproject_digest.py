#!/usr/bin/env python3
"""
Send the daily KSolves Dev-Cluster Access sub-project digest via macOS Mail.app.

Reads the markdown sub-project tracker, sanitizes corporate identifiers
(using the same `~/.config/spark-hooks/patterns` file enforced by the
project pre-commit hook), runs it through the same markdown→plain-text
converter that `send_todo_email.py` uses (so the formatting matches the
existing daily TODO email), and emails it via macOS Mail.app to the
address in `~/.config/spark-hooks/todo-email`.

Default tracker:
    phases/development/phase2/Notes/ksolves_dev_access_subproject.md

Override:
    python3 send_subproject_digest.py <markdown-file>
"""

import re
import sys
from datetime import date
from pathlib import Path

# Reuse the existing markdown-to-text converter and Mail.app sender so the
# digest email matches the daily TODO email's visual style.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from send_todo_email import md_to_text, send  # noqa: E402

REPO_ROOT       = Path(__file__).resolve().parent.parent
DEFAULT_TRACKER = REPO_ROOT / "phases/development/phase2/Notes/ksolves_dev_access_subproject.md"
EMAIL_FILE      = Path.home() / ".config/spark-hooks/todo-email"
PATTERN_FILE    = Path.home() / ".config/spark-hooks/patterns"
SUBJECT_PREFIX  = "KSolves Dev-Cluster Access — Daily Digest"

# Per-pattern replacement overrides for the digest only (the pre-commit hook
# still treats every line in PATTERN_FILE as a flat denylist). The override
# map lives outside the repo at `~/.config/spark-hooks/sanitize-overrides`,
# format `pattern=replacement` per line. Keys are lowered at load time;
# matching here is case-insensitive. Anything not in the override map falls
# back to DEFAULT_REPLACEMENT. Externalizing the map keeps this source file
# from ever containing the same identifiers the pre-commit hook is blocking.
OVERRIDE_FILE       = Path.home() / ".config/spark-hooks/sanitize-overrides"
DEFAULT_REPLACEMENT = "fqdn"


def _load_substitutions() -> dict:
    if not OVERRIDE_FILE.exists():
        return {}
    out = {}
    for raw in OVERRIDE_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip().lower()] = v.strip()
    return out


SUBSTITUTIONS = _load_substitutions()


def sanitize(text: str) -> str:
    """Replace any corporate identifier listed in PATTERN_FILE.

    Default replacement is `fqdn`; per-pattern overrides come from
    SUBSTITUTIONS. Case-insensitive; longest pattern first so a hyphenated
    multi-token pattern is matched before a single-word substring of it
    could be picked up by a shorter pattern.
    """
    if not PATTERN_FILE.exists():
        print("warn: no pattern file found — sending unsanitized", file=sys.stderr)
        return text

    raw = [p.strip() for p in PATTERN_FILE.read_text().splitlines()]
    patterns = sorted({p for p in raw if p}, key=len, reverse=True)
    if not patterns:
        return text

    for p in patterns:
        replacement = SUBSTITUTIONS.get(p.lower(), DEFAULT_REPLACEMENT)
        text = re.sub(re.escape(p), replacement, text, flags=re.IGNORECASE)
    return text


def main() -> None:
    tracker = Path(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_TRACKER
    if not tracker.exists():
        sys.exit(f"Error: tracker file not found — {tracker}")

    if not EMAIL_FILE.exists():
        sys.exit(f"Error: email-address file not found — {EMAIL_FILE}")
    to_addr = EMAIL_FILE.read_text().strip()
    if not to_addr:
        sys.exit("Error: email address file is empty")

    today_str = date.today().strftime("%A, %B %-d, %Y")
    subject   = f"{SUBJECT_PREFIX} — {today_str}"

    # Sanitize first so md_to_text never sees the corporate identifiers.
    raw_md   = tracker.read_text()
    clean_md = sanitize(raw_md)
    body     = md_to_text(clean_md)

    send(to_addr, subject, body)
    print(f"Sent to {to_addr}")


if __name__ == "__main__":
    main()
