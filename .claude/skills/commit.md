Prepare and execute a git commit for the current session's changes.

Steps:
1. Run `git status` to show what has changed.
2. Run `git diff --cached -U0` plus `git diff -U0` to review staged and unstaged changes.
3. Check for corporate identifiers in changed files by grepping for: `allegiance`, `askallegiance`, `rohn.wood@` (case-insensitive). Report any matches before proceeding.
4. If matches are found: stop, report the findings, and ask the user to sanitize before continuing.
5. If clean: propose a concise commit message based on what changed.
6. Stage the appropriate files (`git add <specific files>` — never `git add .` or `git add -A`).
7. Present the final commit command for the user to run manually in their terminal (because the pre-commit hook requires interactive input that Claude Code's bash environment cannot provide).

Format the commit command ready to copy-paste:
```
git commit -m "short description of change"
git push
```

Do not run the commit — output it for the user to execute. Flag if any file with a Revisions section was changed but the Revisions section was not updated.
