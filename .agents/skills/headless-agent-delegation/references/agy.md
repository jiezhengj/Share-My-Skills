# agy

- 首次调用前分别选择权限路径和输出模式。`agy -p` 的 headless 调用无法弹出交互审批；若任务预计需要审批保护的工具，先按当前 `--help`、当前版本支持的权限配置、已有授权和本任务范围确认可用路径，不要默认启动后等待自动拒绝。已有的窄授权可直接使用；不要为了单次调用而擅自新增持久权限规则。
- 多文件、多轮或需要观察进度的任务，从第一次调用就使用 `--output-format stream-json`。它只输出事件，不授予权限；文本模式适用于短小、可预期且无需使用工具的任务。
- 按用户请求和提示词界定本次任务范围。`--dangerously-skip-permissions` 会自动批准所有工具请求；当 headless 无法弹出审批、任务边界清楚且所需操作属于该任务范围时，可在首次调用中直接使用它，继续只执行任务要求的操作。
- 用户要一个或多个独立意见时，由 Codex 启动一个或多个彼此独立的 `agy -p` 进程。不要因为“子代理”一词就让 AGY 再调用内部 `invoke_subagent`；只有用户明确要求测试 AGY 的内部子代理机制时才调用它。
- `stream-json` 中，检查 `step_update.step_type == "tool"` 的 `tool_name`、`state` 和 `tool_info`，以及 `init.permission_mode`、结束时的 `result.status`、`result.response` 和 `result.denied_actions`。遇到拒绝时，用 `result.denied_actions` 确认具体受阻操作，并按[技能中的通用拒绝处理原则](../SKILL.md#工具请求被拒绝时)决定后续；不能只看终态 `status`，是否完成以答复是否包含可交付内容为准。
- 不要为普通评审指定 `--agent`；如用户指定某个 Agent，先用当前安装版本支持的 `agy agents` 检查它是否存在。`--sandbox`、`--mode=plan` 和权限参数会改变执行行为，不作为评审默认项。

官方参考：[Headless mode](https://antigravity.google/docs/cli/headless/)、[Permissions](https://antigravity.google/docs/permissions?tab=cli)。参数和权限配置均以当前安装版本的 `agy --help`、可用设置与运行结果为准；官方文档可能描述了当前版本尚未提供的功能。

最近实测版本：agy 1.2.12（2026-09-29）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `agy --help` 并按其支持方式调整，不要机械照搬本文参数。
