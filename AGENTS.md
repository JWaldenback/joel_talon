# Agent instructions

Read [project settings](docs/agents/project.md) before working in this repo.
For implementation or tracked follow-up work, also read the
[work-record protocol](docs/agents/issue-tracker.md). These files are complete
on their own. Explicit task instructions override them.

For orchestration (`Orchestrate Light` / `Orchestrate Thorough`) or multi-agent
dispatch, also use the dotagents shared workflow: resolve its checkout from
`DOTAGENTS_ROOT`, else the installed
`orchestrate` skill's enclosing checkout, else `~/.agents`, and read
`instructions/base.md` and `skills/orchestrate/SKILL.md` there. This project's
rules override it. If the checkout is missing, say so and continue without
orchestration. Ordinary solo implementation uses the local rules above.
