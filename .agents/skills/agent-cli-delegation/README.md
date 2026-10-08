[中文版](README.zh.md) · [English](README.en.md)

`agent-cli-delegation` delegates bounded tasks to an installed external coding agent only when the user explicitly asks. It supports named or explicitly requested random CLI selection after availability checks, precise session continuation, explicit model choices, phase-specific reviews, progress observation with bounded closure, and recovery based on native results. Ordinary reviews use the target CLI's defaults and project context; file changes require the user's authorization.

See [SKILL.md](SKILL.md) for the full rules, [session handling](references/sessions.md) for continuation and legacy records, [model handling](references/models.md) for model identity and recovery, and [review and closure](references/review.md) for phase-specific prompts and incremental observation. CLI-specific references cover [agy](references/agy.md), [CMDc](references/cmdc.md), [OpenCode](references/opencode.md), and [Pi](references/pi.md).
