---
name: headless-agent-delegation
description: "Use only when the user explicitly asks the calling Agent to delegate a bounded task to an installed external coding agent through its headless CLI, such as agy, cmdc, OpenCode, or pi."
---

# 任务边界与工具选择

在用户明确要求使用外部 Agent CLI 执行或检查任务时使用本技能。用户说“用 agy 评审”“让 pi 检查”“用 opencode 修改”等执行语义时，不要求额外出现 `headless`；仅询问参数、安装、版本、文档或故障排查方法时，不启动外部委派。

提示词应包含目标、相关文件或范围、约束、是否允许修改以及验收条件。外部 Agent 不会自动获得调用方 Agent 的会话内容。

用户明确指定 CLI 时，调用方 Agent 使用该 CLI，不因失败而静默换用其他 CLI。用户未指定时：

1. 读取项目根目录的 `.headless-agent-delegation.json`；仅将 `last_successful_cli` 的精确值 `agy`、`cmdc`、`opencode` 或 `pi` 作为可复用命令名，且该命令仍存在时复用；未知值、路径或带参数的值不执行，改为询问用户；
2. 配置为空、没有记录或记录的 CLI 不存在时，询问用户选择，不按 PATH、安装顺序或字母顺序静默选择；
3. 选定 CLI 因登录、额度或服务连接等外部原因不可用时，如果存在其他本地候选 CLI，先询问用户是否切换。

如果用户明确要求只读、不修改项目文件，或限定的允许修改路径不包括选择记忆文件，不写入选择记忆。单 CLI 委派真正成功且该写入未超出用户授权范围后，才更新 `last_successful_cli`；多个 CLI 独立执行时默认不更新单一默认值，用户明确指定主 CLI 时只有主 CLI 成功才更新。

# CLI 适配

先读取目标 CLI 对应的参考文件；没有参考文件时，依据该 CLI 的官方文档和本机帮助组装调用，不把一个 CLI 的参数套用到另一个 CLI。

- `agy`：读取 [references/agy.md](references/agy.md)。
- `cmdc`：读取 [references/cmdc.md](references/cmdc.md)。
- `opencode`：读取 [references/opencode.md](references/opencode.md)。
- `pi`：读取 [references/pi.md](references/pi.md)。

启动时使用正确的项目根目录或工作目录。需要跨目录时传递明确的绝对路径；不要把 CLI 成功启动误认为它已经看到了正确项目。

长提示或长评审证据不要默认拼进命令行参数；如果目标 CLI 提供 stdin、流式或文件输入，按该 CLI 的文档使用。不要假定 `-p`、`--print`、JSON、stream、权限或模型参数在不同 CLI 中含义相同。

当前版本使用各 CLI 默认模型。用户要求指定模型、provider 或推理强度时，明确说明本技能暂不转发这些选项，不静默传递、替换或切换模型。

# 修改边界

只有用户明确授权时才让外部 Agent 修改文件，并把允许修改的范围和验收条件写入提示词。用户未授权修改时，只有在本次有效 CLI 权限或操作系统隔离实际阻止项目写入后才委派；提示词不是权限限制。若用户限定可写路径，必须确认本次有效权限确实将写入限制在该范围内；无法确认时不启动外部 CLI。用户要求多个 CLI 执行同一任务时，只提醒不要让多个可编辑 CLI 同时修改同一批文件；多 CLI 的数量、并发和结果编排由调用方 Agent 按用户请求决定。

外部 CLI 的具体调用差异属于适配参考。调用方 Agent 根据实际返回结果判断任务是否完成，并如实报告失败。
