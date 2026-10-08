# 输出遗漏与项目身份

- 宿主选择可控单次/逐轮路径时的 run 示例：`opencode run "评审目标和交付要求"`。需要观察工具过程时加 `--format json`；运行结束后同时检查进程退出状态和最后的答复文本。
- 若捕获到的运行输出被截断或没有带出最终答复，按当前帮助确认 `opencode session export` 用法，并导出该次运行的明确 session ID；从导出记录提取最后一条有正文的 assistant 消息，不要把末尾 `idle` 状态记录当成答复。并行运行时不要用“最新 session”代替对应 ID。
- 从目标项目根目录启动，核对进程实际 cwd 与继承 `PWD` 一致；调用方切目录时同步 PWD，否则原生项目可能仍落在旧目录。若后台服务项目不同，当前帮助支持 `--standalone` 时可使用私有服务；它不能修复错误 PWD。先从精确 `session export` 的 `info.location.directory` 核对项目，再检查实际工具路径。OpenCode 从当前目录向上发现项目 `opencode.json`/`.opencode` 配置，并与全局配置合并；不要从临时目录启动后假定目标项目的配置仍然生效，也不要覆盖已有的 `OPENCODE_CONFIG_CONTENT` 等环境配置。
- `--file` 可附加少量指定文件；大量仓库内容通常由 CLI 在正确目录中通过搜索和读取取得，不必全部塞进消息。`--auto` 会自动批准未明确拒绝的权限请求，按当前任务选择；它不能覆盖明确 deny，也不强制限制任务范围。
- 不要求预先配置特定 Agent 才能做普通评审。若用户指定 Agent，先确认该 Agent 在当前配置中可用；不要把 subagent 名称直接当成主 Agent。

出现 `Unknown tool` 或转而执行调用方启动其他评审的动作时，暂停该可疑运行，保存本轮完整 session 与工具事件。检查请求的工具名/input、state.output/error、可见工具集合及 providerCall/providerResult 的 executed 等字段（当前版本若提供），再用精确 session export 核对项目、消息与实际模型。字段缺失不猜补；这些信号不足以确定 provider 注入或永久会话污染，不猜改工具名、不自动换配置/路由。可疑结果不计有效独立意见；停止进程后仍核对服务端状态，续接或新建遵循共同规则。

# 会话与模型

首轮用 `opencode run --format json --model provider/model "任务"`，从本轮事件取得完整 session ID。续接用 `opencode run --format json --session 完整ID --model provider/model "补充问题"`；务必先 `session list`/`session export` 确认该 ID 存在且属于目标项目，因为 `--session` 对不存在的 ID 可能创建会话。`--continue` 是最近会话，不能代替精确定位；`--fork` 是新关联。并发运行只能导出本轮明确 ID，不能用 latest。

同项目 `opencode session list` 列顶层会话，按项目、主题、时间、最后摘要进一步核对；导出原生记录确认具体内容与模型。`opencode models` 若为空，不据此声明有可用模型，核对既有配置和本轮原生信号。模型格式支持 `provider/model#variant`，保留项目配置及既有 provider；调用级权限按任务选择。请求与实际 model/provider 从原生消息分别记录；未知写 null。目录/配置不能代替调用成功或计费证明。

认证、服务或其他首次失败按[共享重试规则](models.md#重试与认证诊断)判断；单个错误不证明 session 永久不可用，重试前核对原生运行状态及已执行动作。

# 宿主控制

run 的单轮完成与 session 逐轮续接为最低路径。服务、API 或 ACP 需要对应双向操作和取消通道；有接口可尝试并核实，不因帮助有入口就宣称已支持；没有通道时用 run。宿主中止进程并不证明服务端任务被取消，仍核对原生 session/运行状态；不能无依据重发修改任务。

官方参考：[CLI Commands](https://opencode.ai/v2/docs/cli/commands/)、[Config](https://opencode.ai/v2/docs/config/)。参数以当前安装版本的 `opencode run --help` 为准。

最近实测版本：OpenCode v2.0.24（2026-10-07，明确模型两轮精确续接通过；已重放并验证 cwd/PWD 对齐及原生项目核对路径，初次偏移记录保留在验证材料）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `opencode run --help` 并按其支持方式调整，不要机械照搬本文参数。
