# Installation

Node.js 20+ and npm are required. Resolve an existing target directory before installation; do not overwrite it. In the target project, ask the agent:

> Run: `npx degit jiezhengj/Share-My-Skills/.agents/skills/agent-cli-delegation .agents/skills/agent-cli-delegation`

# Usage

Use when the user explicitly asks an installed agy, CMDc, OpenCode, or Pi to execute, review, or inspect a task. The skill records observed failures, apparent successes without delivery, and recovery experience. The caller chooses and tries flags and modes using current capabilities, help, and runtime evidence. Installation, version, or troubleshooting questions alone do not start delegation.

Users can name a CLI, request random selection of several different CLIs, or ask to continue an earlier task. The caller locates the native session without requiring an internal ID; ambiguous sessions or missing valid defaults require clarification. Independent opinions use separate external processes.

Use an explicitly named model, or retain the default/existing session model when unspecified. The skill does not select models from preferences such as low cost or strong reasoning. Model substitution follows specific user-provided candidates and order.

# Practical Lessons

- Event output helps observe tool-heavy work and does not grant permissions. Help and startup checks respond to unknown capabilities, changed environments, or failures; they need not repeat every call.
- Headless automatic denial may use a user denied template. Identify its source using actual instructions, effective rules, and CLI diagnostics; the template does not add a user prohibition. The caller may choose invocation-level approval options within an authorized task. Actual user refusals and enforced restrictions remain binding.
- Reviews do not automatically require restricted tools or default permissions. SUCCESS, exit codes, and intermediate PASS statements do not establish completion; verify evidence and final delivery.
- Repeated file names do not establish stagnation. Use new evidence, changed methods, and cost to decide whether to wait, request closure, or recover, without a universal retry count.

Project records retain compact associations and summaries, support legacy choices, and exclude credentials, full history, and permanent permissions. If project writes are forbidden, keep associations in the current conversation.

# References

[SKILL.md](SKILL.md) describes delegation agreements; [sessions](references/sessions.md) covers discovery and record compatibility; [models](references/models.md) covers identity and fallback; [review experience](references/review.md) covers phase confusion and closure.

CLI differences: [agy](references/agy.md), [CMDc](references/cmdc.md), [OpenCode](references/opencode.md), [Pi](references/pi.md).
