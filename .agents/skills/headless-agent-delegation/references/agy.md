# agy

- 普通单次调用：`agy -p "评审目标和交付要求"`。文本输出是默认模式；需要观察工具和进度时使用 `--output-format stream-json`。
- 用户要一个或多个独立意见时，由 Codex 启动一个或多个彼此独立的 `agy -p` 进程。不要因为“子代理”一词就让 AGY 再调用内部 `invoke_subagent`；只有用户明确要求测试 AGY 的内部子代理机制时才调用它。
- `stream-json` 中，检查 `step_update.step_type == "tool"` 的 `tool_name`、`state` 和 `tool_info`，以及结束时 `result.status`、`result.response` 和 `result.denied_actions`。工具被拒绝后，不能只看终态 `status`。
- 判断评审是否完成时，以 `result.response` 是否包含可交付答复为准；`status` 只是 CLI 状态。答复缺失时，检查 `denied_actions` 和工具事件定位原因。
- `-p` headless 调用需要交互批准的工具时，CLI 无法弹出审批界面，未获准的 `run_command` 会自动拒绝。诊断时查看 `init.permission_mode`、工具步骤的 `state`/错误、`result.denied_actions` 和 `result.response`。当前 CLI 的 `--dangerously-skip-permissions` 会把权限模式切换为 `always-proceed` 并自动批准所有工具；是否使用由调用方按任务和当前环境判断，不作为普通评审默认参数。
- 不要为普通评审指定 `--agent`；如用户指定某个 Agent，先用当前安装版本支持的 `agy agents` 检查它是否存在。`--sandbox`、`--mode=plan` 和权限参数会改变执行行为，不作为评审默认项。

官方参考：[Headless mode](https://antigravity.google/docs/cli/headless/)。参数以当前安装版本的 `agy --help` 为准。

最近实测版本：agy 1.2.12（2026-09-29）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `agy --help` 并按其支持方式调整，不要机械照搬本文参数。
