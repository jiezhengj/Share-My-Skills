# Installation

Node.js 20+ and npm are required. If the target skill directory already exists, resolve the conflict before installing; do not overwrite it. In the target project, ask the agent to run:

> Run in the current project: `npx degit jiezhengj/Share-My-Skills/.agents/skills/agent-cli-delegation .agents/skills/agent-cli-delegation`

# Scope

Use this skill only when the user explicitly asks to delegate a bounded task to an installed external coding agent such as `agy`, `cmdc`, OpenCode, or Pi. Do not start delegation for questions about installation, versions, flags, or troubleshooting. The caller needs process launch, output observation, and termination capabilities; the available invocation mode depends on the CLI and the host's verified controls.

# Choosing the CLI, Session, and Model

- Use the named CLI; stop its delegation when it is missing or cannot launch, without installing or substituting another CLI. Verify current command resolution and bounded help/version startup; old successes and stale shims do not prove availability, and launchability does not prove service access.
- For an explicit random new delegation, use the host's random sampling tool on currently launchable supported candidates meeting task constraints. Report candidates and selection; zero stops and one is direct. For multiple different CLIs, sample without replacement; when counts match, use all and randomize only order. Recheck each round; failure exclusions apply only to current known task conditions. Do not redraw indefinitely or randomly migrate a native continuation.
- Without a named CLI or random request, read the last successful choice from `.agent-cli-delegation.json`, retaining legacy `.headless-agent-delegation.json` support. Ask when no currently valid installed choice exists or records conflict. Uninstallation preserves history; an unavailable original CLI blocks native continuation, and an accepted cross-CLI transfer creates a new association.
- Treat “continue the previous task” as a continuation request. Locate the native session using the current conversation, project associations, and accessible history from the same project. Verify the project, full identity, topic, result, and running state. Continue a unique matching session; offer summaries when several match. If none can be found, explain the limitation rather than silently starting over or asking for an internal session ID.
- Create a new association for an independent opinion, a new session, or a fork. When several CLIs are named, launch independent external processes; use a target CLI's internal subagent only when explicitly requested.
- Resolve an explicitly requested model to its exact provider/model/variant. Otherwise retain the CLI default or the existing session's valid model. Preferences such as “cheap” or “strong reasoning” require the user to name a model; the skill does not rank or select models on its own. Record requested and native actual models separately, with `null` for an unknown actual identity.

# Running a Task

- State the goal, scope, questions, and requested conclusion. Ordinary reviews use the CLI's default tools, permissions, and configuration; do not add read-only modes, tool allowlists, sandbox flags, or a custom agent simply because the task is a review. File changes require explicit authorization, a defined scope, and acceptance criteria.
- Start in the target project root and preserve its configuration, account, provider, and runtime environment. Let the CLI search and read a large repository rather than packing it into the prompt argument.
- Check the installed CLI's help before calling it, and choose permissions and output mode separately. Use progress events from the first call for tasks involving multiple files, multiple turns, tools, or progress observation. Event output does not grant tool permissions.
- Default to a single call or successive calls targeting an explicit session. Independent processes do not mandate headless/print mode; choose interactive operation when host control has been verified. Persistent stdin, RPC, ACP, or PTY requires tested bidirectional control, observation, cancellation, and native session verification.
- Use the [review and closure guide](references/review.md) to state the phase, required coverage, evidence-based blockers, and closure conditions without predetermining a verdict. Set an observation budget and track new ranges, queries, results, and evidence. Repeated tool/file names alone do not prove stagnation. Allow at most one targeted closure attempt; if progress remains absent, stop and report partial results and limits. Update the user only for new evidence, blockers, recovery, or a terminal result.
- If the user forbids attempting a tool, verify that the CLI can actually exclude it. A runtime denial does not prove the tool was never requested.
- A successful exit or protocol status does not prove completion. Check the final answer for the requested conclusion, evidence, and format, and inspect actual file changes. Report the CLI, invocation mode, session handling, requested and actual models, substitution grounds, and unverified items.

# Records and Recovery

Project records retain compact session associations, result summaries, and the last successful CLI, without full prompts, responses, credentials, or permanent permissions. If the user forbids project writes, keep associations in the current conversation and explain the limits of recovery from another host. Legacy choice records remain supported and are not automatically deleted.

After a failure or tool denial, inspect native events, completed actions, partial results, and session state before handling the affected operation. Separate launchability, material reading, command execution, and task completion; file review cannot replace required execution tests. Pause suspicious Unknown tool or host-action signals and inspect project/session, tools, configuration, and routing evidence without claiming an unproven contamination cause or changing accounts/providers. A fixed model failure stops automatic model substitution unless the user has authorized specific fallback candidates in a finite order; try each fallback at most once. If context cannot be preserved, obtain acceptance of a new delegation with background before starting it, and avoid replaying completed actions.

# References

- [SKILL.md](SKILL.md): full execution rules.
- [Session handling and legacy choices](references/sessions.md): natural-language continuation, compact records, and recovery.
- [Model identity and recovery](references/models.md): availability and fallback authorization.
- [Review and closure guide](references/review.md): phase-specific prompts, incremental observation, bounded closure, and handling unknown failure causes.
- CLI adapters: [agy](references/agy.md), [CMDc](references/cmdc.md), [OpenCode](references/opencode.md), and [Pi](references/pi.md).
