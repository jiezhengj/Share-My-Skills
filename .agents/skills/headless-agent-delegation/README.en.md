# Installation

Node.js 20+ and npm are required. If the target skill directory already exists, resolve the conflict before installing; do not overwrite it. In the target project, ask the agent to run:

> Run in the current project: `npx degit jiezhengj/Share-My-Skills/.agents/skills/headless-agent-delegation .agents/skills/headless-agent-delegation`

# Scope

Use this skill only when the user explicitly asks to delegate a task to an installed external coding agent such as `agy`, `cmdc`, OpenCode, or Pi. Do not start delegation for questions about installation, versions, flags, or troubleshooting.

# Reviews

- Use the named CLI. If none is named, check `last_successful_cli` in the project-root `.headless-agent-delegation.json`; ask the user when no installed choice is recorded.
- State the goal, scope, question, and requested conclusion. For an ordinary review, use the CLI's default tools, permissions, and configuration; do not add read-only modes, tool allowlists, sandbox flags, or a custom agent just because the task is a review.
- Start in the target project root and preserve its configuration and the current runtime environment. Let the CLI search and read a large repository; do not pack the whole repository into the prompt argument.
- If the user explicitly forbids attempting a tool, verify that the CLI can actually exclude it. A runtime denial does not prove the tool was never requested.
- A successful exit or protocol status does not prove the review is complete. Check that the final answer contains the requested conclusion and evidence; inspect native CLI events when diagnosing a run.

See [SKILL.md](SKILL.md) and `references/` for CLI-specific invocations and event fields.
