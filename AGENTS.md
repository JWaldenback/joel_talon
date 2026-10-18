# Agent instructions

Before acting, read [project settings](docs/agents/project.md) and the
[tracker protocol](docs/agents/issue-tracker.md). They are complete on their
own. Explicit task instructions override them.

For orchestration (`Orchestrate Light` / `Orchestrate Thorough`), multi-agent
dispatch, or implementing a specification, also use the dotagents shared
workflow: resolve its checkout from `DOTAGENTS_ROOT`, else the installed
`orchestrate` skill's enclosing checkout, else `~/.agents`, and read
`instructions/base.md` and `skills/orchestrate/SKILL.md` there. This project's
settings override it. If the checkout is missing, say so and continue
without orchestration.
