# agy

- 先按宿主已验证的控制能力选择模式，再分别核对权限与输出。`--print`/`-p` 是单次非交互路径；当前帮助提供 `--prompt-interactive`，只有宿主已验证持续输入、审批观察、终止及会话核对才可采用。交互入口存在不证明当前宿主可控制；不要为避免拒绝启动不可控交互。
- 选择 print 时，它不能弹出交互审批；预计必需的受保护操作须按当前帮助、既有配置及本任务授权核对可用路径。可信工作区不证明命令获准，工具列表可见不证明执行获准；无权限证据就说明限制，不靠试拒绝完成预检，不擅自新增持久权限。材料评审保留默认工具，命令实测是否必需由验收决定。
- 多文件、多轮或需要观察进度的任务，从第一次调用就使用 `--output-format stream-json`。它只输出事件，不授予权限；文本模式适用于短小、可预期且无需使用工具的任务。
- 按用户请求和提示词界定本次任务范围。`--dangerously-skip-permissions` 会自动批准所有工具请求；只有已有授权或既有有效配置允许这一调用级权限路径，且所需操作属于本任务范围时才能使用它；任务边界清楚或审批不可用本身不足以放宽权限，继续只执行任务要求的操作。
- 用户要一个或多个独立意见时，由调用方启动一个或多个独立 AGY 进程；独立性不决定 print 或交互模式，仍按宿主控制选择。不要因为“子代理”一词就让 AGY 再调用内部 `invoke_subagent`；只有用户明确要求测试 AGY 的内部子代理机制时才调用它。
- `stream-json` 中，检查 `step_update.step_type == "tool"` 的 `tool_name`、`state` 和 `tool_info`，以及 `init.permission_mode`、结束时的 `result.status`、`result.response` 和 `result.denied_actions`。遇到拒绝时，用 `result.denied_actions` 确认具体受阻操作，并按[技能中的通用拒绝处理原则](../SKILL.md#工具请求被拒绝时)决定后续；不能只看终态 `status`，是否完成以答复是否包含可交付内容为准。
- 不要为普通评审指定 `--agent`；如用户指定某个 Agent，先用当前安装版本支持的 `agy agents` 检查它是否存在。`--sandbox`、`--mode=plan` 和权限参数会改变执行行为，不作为评审默认项。

命令拒绝且最终空答复时，不能因 `SUCCESS` 判完成，也不整体淘汰 AGY。若验收是材料核查，原生事件显示现有 `view_file`/`list_dir`/`grep_search` 可工作，可用精确 conversation 续接：指出已拒绝的操作、补齐尚缺材料并交结论，标注未实测项；不重复已知拒绝或全局禁命令。若必需构建/环境验证受阻，保留未完成，不用阅读替代。恢复不得改模型、配置或权限；其他模式仅在已验证宿主控制且原会话/权限可保持时考虑。

# 会话与模型

宿主只支持可控单次/逐轮时，以下为 print 路径示例（未指定模型就省略 --model，不添加其他限制）。首轮用 `agy -p "任务" --model 完整模型ID --output-format stream-json`，捕获顶层 `conversation_id`、`result.conversation_id` 与 `init.cwd`；`init.model` 是原生运行模型证据。续接要求本轮与已捕获完整身份及项目一致。尚无可访问原生存在核对入口时不能凭记录保证存在，应明确限制并避免使用可能新建的参数路径。续接用 `agy -p "补充问题" --conversation 完整ID --model 完整模型ID --output-format stream-json`，需要项目参数时使用已核对 `--project`，保留 cwd、配置与权限。`--continue` 只指最近会话，不能替代已匹配会话的精确身份。运行前检查原生存在及项目，不凭主题猜 ID。历史列表入口若未公开或记录不可访问，就说明仅能续接已捕获关联；不要求人类提供内部 ID。

`agy models` 查询当前目录，`--model` 接受模型身份。核对原生事件实际模型字段与请求值；若事件无可信字段，实际模型记 null。目录不是调用或价格证明，仅偏好不代选，替代只执行用户具体候选顺序，见共同模型规则；不能凭 Flash/Pro 名称比较成本或能力。

# 宿主控制

`--input-format stream-json` 要求 `--output-format stream-json`，帮助说明 stdin 按 NDJSON 消息逐轮处理；只有宿主具备持续写入、观察和取消并经过真实验证才使用。否则采用单轮加 conversation 续接。宿主中止后仍核对已执行操作与原生 session，不把进程退出当作动作回滚。

官方参考：[Headless mode](https://antigravity.google/docs/cli/headless/)、[Permissions](https://antigravity.google/docs/permissions?tab=cli)。参数和权限配置均以当前安装版本的 `agy --help`、可用设置与运行结果为准；官方文档可能描述了当前版本尚未提供的功能。

最近实测版本：agy 1.3.1（2026-10-07，明确模型两轮续接；首轮工具拒绝后的调用级权限重试另有验证记录）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `agy --help` 并按其支持方式调整，不要机械照搬本文参数。
