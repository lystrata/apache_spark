Scan all tracked and staged files in this project for corporate identifiers that must not be committed to the public GitHub repository.

Patterns to check: load from `~/.config/spark-hooks/patterns` (one pattern per line). Do not reproduce the pattern strings in any output or file.

Steps:
1. Run a grep across all `.html`, `.md`, `.py`, `.json`, and `.txt` files in the project directory for the above patterns.
2. Report every match: file path, line number, and the matching line content.
3. If no matches are found, confirm the project is clean.
4. If matches are found, show them clearly and ask whether to sanitize each one, and what replacement to use, before making any changes.

Do not make any edits until the user has reviewed the findings and confirmed the action.
