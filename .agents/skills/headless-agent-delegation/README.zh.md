[README](README.md) · [English](README.en.md)

# 安装指南

需要 Node.js 20+ 和 npm；目标技能目录已存在时，请先处理冲突，不要覆盖。在要安装技能的目标项目中，发给 Agent 的指令：

> 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/headless-agent-delegation .agents/skills/headless-agent-delegation`

# 适用条件

`headless-agent-delegation` 只在用户明确要求调用已安装的外部编码 Agent CLI 时使用，例如让 `agy`、`cmdc`、`OpenCode` 或 `pi` 评审、检查、执行或修改一个边界清楚的任务。

- 用户明确指定使用外部 CLI。
- 委派提示词能够写清目标、相关文件或范围、约束、是否允许修改以及验收条件。

用户只询问 CLI 的安装、版本、参数、文档或故障排查时，不启动外部委派。

# 选择规则

- 用户指定 CLI 时必须使用指定 CLI，失败后不能静默切换。
- 用户未指定时，先读取项目根目录的 `.headless-agent-delegation.json`。
- 只有 `last_successful_cli` 精确等于 `agy`、`cmdc`、`opencode` 或 `pi` 且该命令仍存在时才复用；否则询问用户选择。
- 不按 PATH 顺序、安装顺序或字母顺序自动选择。
- 调用前读取对应的适配说明：[`agy`](references/agy.md)、[`cmdc`](references/cmdc.md)、[`OpenCode`](references/opencode.md) 或 [`pi`](references/pi.md)。

# 修改边界

只有用户明确授权时，外部 Agent 才可以修改文件。未授权修改的只读任务必须使用实际生效的 CLI 或操作系统限制阻止项目写入；提示词本身不是权限边界。用户限定可写路径时，必须确认有效权限会执行该范围，否则不启动 CLI。提示词必须写明允许修改的范围和验收条件。外部命令返回成功不等于任务已经完成，调用方 Agent 仍需检查实际响应和文件变化。

# 技能范围

本技能只负责委派路由和安全边界。不同 CLI 的调用差异必须放在各自的适配说明中，不能把一个 CLI 的参数直接套用到另一个 CLI。完整契约见 [`SKILL.md`](SKILL.md)。
