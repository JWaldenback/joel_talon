# Project conventions for Claude

## Git

- **Always merge, never rebase** when pulling from upstream or integrating
  parallel work. Use `git merge upstream/main` (or equivalent) and accept the
  merge commit. Rationale: I want individual commits to stay distinct in the
  history, not blended into a linear sequence. Rebase rewrites commit SHAs
  and forces a force-push, which I don't want.

- **Don't push to any remote without explicit permission.** Stop after the
  commit lands locally and ask before running `git push`. Same applies to
  any push variant (`--force`, `--force-with-lease`, etc.).

## Code style

- **Don't add comments to `.talon` files without asking first.** They're
  voice-command grammar files; I want them to stay minimal and read like
  a clean list of commands. If you think a comment is genuinely needed
  (e.g. to explain why a command is disabled), check with me before
  adding it.

- **Comments in `.py` files are fine and encouraged** when you're adding
  new logic, non-obvious control flow, or anything that needs context
  for future-me to understand. Default to keeping them.
