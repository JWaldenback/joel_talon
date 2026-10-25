# Work records

Use Git-tracked Markdown at `.scratch/<effort>/map.md`. Read an existing record
before resuming that effort. Routine work needs no external issue or pull request.

## Everyday work

A small implementation task needs a short record covering:

- Status and outcome: what changed, or what remains to do.
- Important decisions, permissions or deferrals that affect continuing the work.
- Verification performed and any remaining checks or blockers.

Use a few bullets and update the same record as work progresses. Summarize
results rather than copying routine commands, conversation transcripts or
unchanged status. Read-only advice needs a record only when it creates
actionable follow-up work.

Use `in-progress`, `blocked`, `ready-for-human` or `done` as appropriate. Distinguish
implemented behavior from unverified physical checks. Preserve permission scope
and limits when handing off or resuming. Task-specific authorization ends with
that task unless the owner grants a longer term. Record changed decisions or
revoked permission clearly; follow the project's Git approval rules.

Keep completed records useful for future work without rewriting them as a
routine cleanup. Record actionable unrelated findings as separate brief follow-ups.

## Larger or delegated efforts

Add a specification and numbered `issues/<NN>-<slug>.md` tickets when work needs
separate owners or dependencies. Each ticket states its outcome, scope,
acceptance criteria, verification and prerequisites. Use `Claimed by` and
`Blocked by` when they help coordinate work. Claim tickets before dispatch and
respect their dependencies. Additional states such
as `ready-for-agent` and `in-review` are available for this workflow.

Link shared evidence rather than repeating it in every ticket. Record the
accepted candidate and remaining external or physical checks before closing
work. A human gate blocks only the actions that depend on it.

When a skill expects hosted issues, comments or PR tracking, use these local
records unless the owner or project workflow calls for a hosted artifact.
