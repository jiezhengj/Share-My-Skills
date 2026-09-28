# Command Code (CMDc)

- 普通单次调用：`cmdc -p "评审目标和交付要求"`。在 Windows 中，产品文档或帮助若把命令称为 `cmd`，要注意 `cmd` 通常解析为系统命令提示符；使用安装包实际提供的 Command Code 可执行文件或 shim（例如 `cmdc`），并用当前环境的命令解析和 `--help` 确认。
- 默认 headless 工具可读文件、搜索和列目录；shell、编辑和写入默认被阻止。普通代码评审使用默认能力即可；不要为了评审加 `--yolo` 或 `--tools-all`。`--tools-enable` 是增加被 headless 隐藏的工具，不是只读白名单。
- Windows 下，如果 `read_file.file_path` 收到 `Path must be absolute`，用当前工作目录补成绝对路径后重试该读取；不需要为此改权限或打开 shell。
- 需要观察工具和多轮进度时加 `--output-format json`。这是 NDJSON：事件行为 `{"type":"event","event":...}`，最后读取独立的 `{"type":"result",...}` 行，检查 `subtype`、`stopReason` 和 `finalText`。`tool_running`、`tool_completed` 能区分调用请求与执行结果。

官方参考：[Headless Mode](https://commandcode.ai/docs/headless)。参数以当前安装版本的 `cmdc --help` 为准。

最近实测版本：CMDc 1.66.0（2026-09-29）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `cmdc --help` 并按其支持方式调整，不要机械照搬本文参数。
