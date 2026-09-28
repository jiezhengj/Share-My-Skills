本文件只记录 OpenCode 的 headless 调用差异；不要把这些参数套用到其他 CLI。

# 调用与输入

短提示通过 `run` 的消息参数传入：

```text
opencode run "提示词"
```

长证据可用 `--file <path>` 附加，并在消息参数中说明评审目标：

```text
opencode run --file evidence.md "按要求评审附件"
```

不要假设 stdin 会成为提示词，也不要把 `--file` 当作提示词。把进程工作目录设为目标项目根目录。

# 权限

如果本机 `opencode --help` 列出 `--auto`，该选项会自动批准未被明确拒绝的权限请求，不是仅限文件编辑的窄权限模式。不要默认添加；只有用户明确授权相应自动批准行为时才使用。

OpenCode 默认权限不能视为只读。内置 `explore` 是子 Agent，不能直接作为 `opencode run --agent` 的目标。未获修改授权时，只能使用已配置且有效权限实际阻止项目写入的主 Agent；同时确认 shell、MCP 或可调用子 Agent 不会绕过该限制。没有可验证的只读主 Agent 时不要启动该任务。提示词本身不构成权限限制。

普通委派使用默认文本输出即可；`--format json` 输出 NDJSON。

# 官方资料

- [OpenCode CLI Commands](https://opencode.ai/v2/docs/cli/commands/)
- [OpenCode V2 Permissions](https://opencode.ai/v2/docs/permissions)
