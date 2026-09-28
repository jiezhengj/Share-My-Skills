[README](README.md) · [中文](README.zh.md)

# When to Use It

`headless-agent-delegation` is used only when the user explicitly asks the calling Agent to delegate a bounded task to an installed external coding Agent through a headless CLI, such as `agy`, `cmdc`, `OpenCode`, or `pi`.

- The user explicitly asks an external CLI to review, inspect, execute, or modify a bounded task.
- The prompt can state the target, relevant files, constraints, modification permission, and acceptance criteria.

Do not start an external delegation merely because the user asks about a CLI's installation, version, parameters, documentation, or troubleshooting.

# Selection Rules

- If the user names a CLI, use that CLI and do not silently switch after failure.
- If no CLI is named, read the project-root `.headless-agent-delegation.json` and reuse `last_successful_cli` only when it is exactly `agy`, `cmdc`, `opencode`, or `pi`, and that command still exists; otherwise ask the user.
- If no usable CLI is configured, ask the user to choose; do not select one by PATH order or alphabetic order.
- Read the matching adapter reference before invoking a CLI: [`agy`](references/agy.md), [`cmdc`](references/cmdc.md), [`OpenCode`](references/opencode.md), or [`pi`](references/pi.md).

# Modification Boundary

An external Agent may modify files only when the user explicitly authorizes modification. For an unapproved read-only task, use an effective CLI or OS restriction that prevents project writes; the prompt alone is not a permission boundary. If the user limits writable paths, verify that effective permissions enforce that scope or do not start the CLI. The prompt must state the allowed scope and verification conditions. A successful process exit alone does not prove that the external Agent completed the requested work; inspect its actual response and file changes.

# Scope

This skill provides routing and safety rules. CLI-specific invocation differences belong in adapter references and must not be copied from one CLI to another. See [`SKILL.md`](SKILL.md) for the complete contract.
