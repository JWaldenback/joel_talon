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
