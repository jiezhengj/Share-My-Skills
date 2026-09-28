# Pi

- 普通单次调用：`pi --print "评审目标和交付要求"`。需要中间工具事件时加 `--mode json`；它输出 JSONL 事件，不是权限限制，也不是单个 JSON 文档。
- JSON 诊断时，检查 `tool_execution_start` 和对应的 `tool_execution_end`，读取错误或工具结果；等待 `agent_settled` 作为本次自动工作结束标记，不能只看 `agent_end`。
- 普通评审不要默认传 `--tools`、`--exclude-tools`、`--no-extensions` 或其他限制参数。`--tools` 会替换工具集合；若用户明确要求工具排除，先按当前安装版本的帮助确认效果。
- 多文件评审可从目标项目根目录启动，让 Pi 使用文件读取和搜索工具。不要预先要求逐个读取；只有运行事件显示具体批量调用失败时，才针对那项失败调整调用。

官方参考：[CLI Integration](https://pi.dev/docs/latest/cli-integration)。参数以当前安装版本的 `pi --help` 为准。

最近实测版本：Pi 0.87.1（2026-09-29）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `pi --help` 并按其支持方式调整，不要机械照搬本文参数。
