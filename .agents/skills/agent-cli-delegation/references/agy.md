# 调用与过程观察

`agy -p "任务目标和交付要求"` 是单次非交互示例；`--prompt-interactive` 提供交互入口，选择取决于宿主能否实际输入、观察和停止。`--input-format stream-json` 要求 `--output-format stream-json`，stdin 按 NDJSON 消息逐轮处理；有对应接口时可尝试，没有持续写入接口时可用单次加 conversation 续接。

工具密集或需要观察进度时建议 `--output-format stream-json`。检查 `step_update.step_type == "tool"` 的 `tool_name/state/tool_info`、`init.permission_mode` 和终态 `result.status/response/denied_actions`。事件输出只增加可见性，不改变权限。

`--agent` 需要当前可用 Agent；如需使用可用 `agy agents` 查询。`--sandbox` 和 `--mode=plan` 会改变执行行为，根据任务选择，不因评审自动添加。

# headless 自动拒绝与空 SUCCESS

print 不能弹出交互审批。已有原始记录中 `run_command` 返回 “user denied permission” 和禁止绕行的模板，但随后 CLI 诊断明确说明 headless 无法提示审批，因此 auto-denied；终态为 SUCCESS，response 为空，denied_actions 含 command。这是未完成任务，模板本身不证明用户拒绝。

结合实际用户指令、有效权限规则、工具错误和 CLI 诊断判断拒绝来源。可信工作区或 tools 列表可见不证明操作获准；命令自动拒绝也不证明文件工具不可用。若确为自动拒绝，可在任务范围内调整调用级审批方式、使用其他可用工具或选择可控交互路径；用户明确拒绝或有效禁止规则继续遵守。

当前 `--dangerously-skip-permissions` 自动批准所有工具请求，无需提示；它不是只读或按任务范围强制限制的选项。调用方按已授权任务和明确限制选择，不仅因参数名另请用户授权，也不因审批不可用认定所有操作都获授权。调用级参数与新增 settings.json 持久 allow-rule 分开处理。

已验证的恢复：保持任务、项目、模型和完整 conversation，增加上述调用级参数后，permission_mode 从 request-review 变为 always-proceed，view_file 实际读取材料并返回结论。这证明该路径在所测条件下可恢复，不保证所有拒绝都适用。只需材料核查时也可用已可用的文件工具精确续接；必需命令实测仍须真实执行，不能以阅读替代。调整后检查实际工具结果与最终交付，避免无恢复迹象的持续重复；有限诊断重试见[共享规则](models.md#重试与认证诊断)。401 不直接证明不可重试；未取得原生日志时不声称 AGY 返回了非重试标记。

# 会话与模型

首轮示例：`agy -p "任务" --model 完整模型ID --output-format stream-json`，未指定模型省略 --model；按当前任务选择所需权限参数。捕获顶层和 result 的 conversation_id、init.cwd；init.model 是原生运行模型字段。

续接示例：`agy -p "补充问题" --conversation 完整ID --model 完整模型ID --output-format stream-json`。核对身份和项目，需要 project 参数时使用已核对值；保留项目配置，不把权限参数冻结为原值。`--continue` 指最近会话，不能代替精确匹配。尚无可靠原生历史入口时说明发现范围，使用已捕获关联，不凭主题猜 ID 或要求用户给内部 ID。

`agy models` 列模型；请求值与实际原生字段分别核对，无可信字段记 null。目录不证明可调用或价格；具体选型和替代见[模型参考](models.md)。

官方参考：[Headless mode](https://antigravity.google/docs/cli/headless/)、[Permissions](https://antigravity.google/docs/permissions?tab=cli)。参数差异以当前 `agy --help`、有效配置和运行结果确认；文档可能描述当前版本没有的入口。

最近实测版本：agy 1.3.1（2026-10-07，明确模型两轮续接；首轮自动拒绝后同 conversation 调用级权限恢复通过）。这是最近测试记录，不是版本门禁；本次原始日志回放未新增模型实测。
