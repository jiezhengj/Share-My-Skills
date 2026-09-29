# OpenCode

- 普通单次调用：`opencode run "评审目标和交付要求"`。需要观察工具过程时加 `--format json`；运行结束后同时检查进程退出状态和最后的答复文本。
- 若捕获到的运行输出被截断或没有带出最终答复，按当前帮助确认 `opencode session export` 用法，并导出该次运行的明确 session ID；从导出记录提取最后一条有正文的 assistant 消息，不要把末尾 `idle` 状态记录当成答复。并行运行时不要用“最新 session”代替对应 ID。
- 从目标项目根目录启动。OpenCode 从当前目录向上发现项目 `opencode.json`/`.opencode` 配置，并与全局配置合并；不要从临时目录启动后假定目标项目的配置仍然生效，也不要覆盖已有的 `OPENCODE_CONFIG_CONTENT` 等环境配置。
- `--file` 可附加少量指定文件；大量仓库内容通常由 CLI 在正确目录中通过搜索和读取取得，不必全部塞进消息。`--auto` 会自动批准未明确拒绝的权限请求，不要作为普通评审的默认参数。
- 不要求预先配置特定 Agent 才能做普通评审。若用户指定 Agent，先确认该 Agent 在当前配置中可用；不要把 subagent 名称直接当成主 Agent。

官方参考：[CLI Commands](https://opencode.ai/v2/docs/cli/commands/)、[Config](https://opencode.ai/v2/docs/config/)。参数以当前安装版本的 `opencode run --help` 为准。

最近实测版本：OpenCode v2.0.18（2026-09-29）。该记录不表示本技能与此版本强绑定；遇到差异时查看当前 `opencode run --help` 并按其支持方式调整，不要机械照搬本文参数。
