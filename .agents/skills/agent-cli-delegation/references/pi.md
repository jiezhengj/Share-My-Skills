# 无输出与终态识别

`pi --print "任务"` 是文本单次示例；项目材料/工具调用需要观察时可用 `pi --mode json --print "任务"`。普通模式长时间没有输出时，后续改为 JSON 观察工具进展。`--mode json` 输出 JSONL，不是单个 JSON 文档，也不改变权限。

检查 tool_execution_start 与对应 tool_execution_end 的参数和结果；agent_settled 是本次自动工作结束标记，agent_end 不能单独代替它。中间 PASS 倾向不等于最终报告。

重复文件/工具名可能是继续读取区间或交叉核对，结合参数和新增证据判断。批量读取失败时针对具体错误调整，无须预先要求逐文件读取；收束经验见[评审参考](review.md)。

# 工具选项与会话

`--tools` 替换工具集合；--exclude-tools 和 --no-extensions 也改变能力，按需要和当前帮助选择，不因为评审自动叠加限制。

首轮示例：`pi --print --mode json --provider 已有provider --model 完整模型ID "任务"`，未指定时可省略 provider/model 沿用配置。捕获原生 session 头与文件路径。续接：`pi --print --mode json --session 完整路径或ID "补充问题"`，需要明确模型时添加对应参数。核对头部 cwd/project 和会话身份。

`--session-id` 不存在时可能新建，不能保证续接；无参 --resume 进入历史选择器，只有能控制该交互时适用。原生项目目录可读头部和摘要定位；--session-dir 改变存储位置，不是续接必需参数。

`pi --list-models` 提供 provider/model、context、max-out、thinking/images，不给价格或可调用证明。实际模型取原生 assistant 消息或 session 字段；缺失为 null。

认证、provider 或其他首次失败按[共享重试规则](models.md#重试与认证诊断)判断；有限诊断重试和重复已执行问题分别处理，不单凭错误类别禁止重试。

# RPC 与取消

`--mode rpc` 需要宿主能持续写 JSON 命令、读响应、关联请求并控制 abort；具备接口可尝试并核实，不因参数存在就称已支持。只有启动/输出接口时可用 print 加精确 session 逐轮调用。取消后核对已执行动作，避免重复发送相同问题；已有原生记录中重复发问导致 Pi 报告重复，不能只看后次输出认定续接失败。

官方参考：[CLI Integration](https://pi.dev/docs/latest/cli-integration)。遇到差异查看当前 pi --help。

最近实测版本：Pi 1.0.3（2026-10-07，明确模型两轮同 session，原生记录确认续接和重复提示）。最近测试记录不构成版本门禁。
