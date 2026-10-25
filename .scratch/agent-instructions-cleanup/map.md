# Agent instruction cleanup

Status: done

- Owner requested simpler everyday instructions and tracking while preserving
  Talon safety and the existing merge/push rules.
- Keep the four-file structure and the one-line CLAUDE.md pointer. Restrict
  shared orchestration to orchestration or delegation; remove routine model
  research settings. Use short records for solo tasks and tickets for larger work.
- Verification passed: Talon safety/runtime sections are unchanged, merge/push
  and file/comment rules are preserved, instruction links resolve, and
  git diff --check passes. No runtime changes or runtime test rerun needed.
