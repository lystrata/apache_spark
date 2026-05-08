#!/usr/bin/env bash
# check_fqdn.sh — Sanitization-pattern check for one or more files.
#
# Reads patterns from the user's private patterns file at
# ~/.config/spark-hooks/patterns (one pattern per line, OR-joined for grep -E),
# then greps each given file for any case-insensitive match.
#
# Exit codes:
#   0 — script ran cleanly (matches printed if found; no matches printed if not)
#   1 — patterns file missing or no files given
#
# Usage:
#   ./Scripts/check_fqdn.sh <file> [<file> ...]
#
# Example:
#   ./Scripts/check_fqdn.sh phases/phase2/development/Notes/proxmox_audit_2026-05-08.md
#
# Output: matches printed with filename:line:content ; "No matches" if clean.

set -u

PATTERN_FILE="${SPARK_HOOK_PATTERNS:-$HOME/.config/spark-hooks/patterns}"

if [ ! -f "$PATTERN_FILE" ]; then
  echo "check_fqdn.sh: pattern file not found at $PATTERN_FILE" >&2
  echo "  set SPARK_HOOK_PATTERNS env var to override the location" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "check_fqdn.sh: no files given" >&2
  echo "  usage: $0 <file> [<file> ...]" >&2
  exit 1
fi

PATTERNS=$(paste -sd'|' "$PATTERN_FILE")

if [ -z "$PATTERNS" ]; then
  echo "check_fqdn.sh: pattern file is empty — nothing to check" >&2
  exit 1
fi

clean=1
for f in "$@"; do
  if [ ! -f "$f" ]; then
    echo "check_fqdn.sh: skipping (not a file): $f" >&2
    continue
  fi
  hits=$(grep -inE "$PATTERNS" "$f" || true)
  if [ -n "$hits" ]; then
    echo "=== $f ==="
    echo "$hits"
    clean=0
  fi
done

if [ "$clean" -eq 1 ]; then
  echo "No matches in $# file(s)."
fi
