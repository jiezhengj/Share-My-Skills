# Command Code (CMDc)

- 普通单次调用：`cmdc -p "评审目标和交付要求"`。在 Windows 中，产品文档或帮助若把命令称为 `cmd`，要注意 `cmd` 通常解析为系统命令提示符；使用安装包实际提供的 Command Code 可执行文件或 shim（例如 `cmdc`），并用当前环境的命令解析和 `--help` 确认。
- 默认 headless 工具可读文件、搜索和列目录；shell、编辑和写入默认被阻止。普通代码评审使用默认能力即可；不要为了评审加 `--yolo` 或 `--tools-all`。`--tools-enable` 是增加被 headless 隐藏的工具，不是只读白名单。
- Windows 下，如果 `read_file.file_path` 收到 `Path must be absolute`，用当前工作目录补成绝对路径后重试该读取；不需要为此改权限或打开 shell。
- 需要观察工具和多轮进度时加 `--output-format json`。这是 NDJSON：事件行为 `{"type":"event","event":...}`，最后读取独立的 `{"type":"result",...}` 行，检查 `subtype`、`stopReason` 和 `finalText`。`tool_running`、`tool_completed` 能区分调用请求与执行结果。

# 会话与模型

首轮使用 `cmdc -p "任务" --model 完整模型ID --output-format json`，捕获 `event.type=run_start` 的 `event.sessionId` 及终态 `result.sessionId`，要求两者一致。`model_request_start.model` 只证明请求路由。可访问本机原生项目记录时，先核对已捕获 ID 对应的项目目录与元数据；没有可靠入口时明确项目核对限制。本轮确认原生项目存储位于用户目录 `.commandcode/projects/`，只查目标项目映射，不能凭目录名字符串自行等同项目。JSONL 的 `type=session` 头部 `id/cwd` 核对完整身份和原生项目；`type=message` 且 `message.role=assistant` 的顶层 `model` 可记录原生实际模型，不能把仅含 entrypoint/traceIds 的 `.meta.json` 当项目或模型证据。续接使用 `cmdc -p "补充问题" --session 完整路径或ID --model 完整模型ID --output-format json`，保持同一项目 cwd 和既有权限。先确认 session 存在且项目相符；不能用无参 `--resume` 自动进入选择器，也不能把主帮助视为历史列表成功。帮助支持 `--fork-session`，分叉须创建新关联。

`cmdc --list-models` 同时列内置服务与 BYOK provider 模型。先核对既有默认模型/provider；例如内置 `deepseek/...` 与自定义 provider 下的同族模型是不同路由，不能因名字近似把内置服务当作用户订阅。使用准确完整 provider/model 身份，不用短名称代替含多层命名空间的值。目录不能证明认证、额度或计费。保留完整模型身份与请求值，实际模型从原生事件或 session 元数据核对；缺少证据记录 null，不能从 finalText 中的自称推定。默认或原会话模型仅在未指定时沿用，固定模型失败不自动替换。可访问历史接口未确认时只报告已捕获关联范围，禁止猜目录、扫个人全部历史。通用匹配与记录见 [sessions](sessions.md)。

# 宿主控制

`-p` 单轮及 `--session` 精确续接已在准确既有 provider 模型上完成两轮交付验证；请求模型字段仍不能冒充实际后端身份。ACP 只有宿主能持续双向写入、观察与取消且实测通过后可用；仅具进程启动/输出接口时逐轮调用。中止宿主作业只证明进程停止，仍需查看原生事件和最后结果，不能宣称未产生动作。

官方参考：[Headless Mode](https://commandcode.ai/docs/headless)。参数以当前安装版本的 `cmdc --help` 为准。

最近实测版本：CMDc 1.77.0（2026-10-07，准确 BYOK 模型两轮同原生 session；首次误选内置服务的余额错误另留验证记录）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `cmdc --help` 并按其支持方式调整，不要机械照搬本文参数。
