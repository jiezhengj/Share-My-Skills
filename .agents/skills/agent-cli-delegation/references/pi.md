# Pi

- 宿主已选择可控单次/逐轮路径时，首次调用按任务类型选择输出模式：短小、可预期且无需读取项目材料或调用工具的任务可用 `pi --print "任务目标和交付要求"`；项目文件调查、多份材料核对、多轮工具调用或并行评审，从第一次调用就用 `pi --mode json --print "任务目标和交付要求"`。如果同一任务的普通模式已长时间无输出，改用 JSON 模式。
- `--mode json` 输出 JSONL 事件，只改变过程可见性，不改变权限，也不是单个 JSON 文档。
- JSON 诊断时，检查 `tool_execution_start` 和对应的 `tool_execution_end`，读取错误或工具结果；等待 `agent_settled` 作为本次自动工作结束标记，不能只看 `agent_end`。
- 普通评审不要默认传 `--tools`、`--exclude-tools`、`--no-extensions` 或其他限制参数。`--tools` 会替换工具集合；若用户明确要求工具排除，先按当前安装版本的帮助确认效果。
- 多文件评审可从目标项目根目录启动，让 Pi 使用文件读取和搜索工具。不要预先要求逐个读取；只有运行事件显示具体批量调用失败时，才针对那项失败调整调用。

多文件评审按[阶段评审与收束](review.md)明确必查项与结案。观察 tool_execution_start/end 中的参数、路径/区间及结果，区分继续覆盖与重复确认；同一工具/文件名不证明停滞。缺参数时记未知，不摘录推理当成果。无新增证据时按本轮预算最多一次收束；没有实时输入通道就核对终态后用精确 session 逐轮续接，不反复发送相同问题。中间 PASS 倾向不能替代 agent_settled 后的正式报告。

# 会话与模型

首轮用 `pi --print --mode json --provider 已有provider --model 完整模型ID "任务"`，捕获原生 session 头与会话文件完整路径。续接用 `pi --print --mode json --session 完整路径或ID --provider 已有provider --model 完整模型ID "补充问题"`；运行前确认文件存在、头部 cwd/project 相符。`--session-id` 在不存在时可能新建，不能用于保证续接。无参 `--resume` 会进入历史选择器，不能用作自动化路径。历史可从已确认的项目 session 目录读取头部和简短摘要；`--session-dir` 改变存储位置，保持原有设置，不擅自迁移历史。

`pi --list-models` 给出 provider/model、context、max-out、thinking 与 images，不给价格，也不证明实际可用。请求模型与原生 assistant 消息或 session 的 model/provider 分别核对，实际字段缺失记录 null。未指定时沿用默认或原会话有效模型，显式模型失败须按共同规则处理。

# 宿主控制

JSON print 单轮与 session 逐轮是最低路径。`--mode rpc` 仅在宿主能持续发送 JSON 命令、读取响应事件、关联请求与控制 abort 并已真实验证时使用。只有启动/输出/中止能力时降级逐轮，不宣称 RPC 已支持。取消后保留会话并核对已完成动作。

官方参考：[CLI Integration](https://pi.dev/docs/latest/cli-integration)。参数以当前安装版本的 `pi --help` 为准。

最近实测版本：Pi 1.0.3（2026-10-07，明确模型两轮同 session，上下文续接通过；原生历史核对排除了重复提示引起的误判）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `pi --help` 并按其支持方式调整，不要机械照搬本文参数。
