本文件只记录 Pi 的 headless 调用差异；不要把这些参数套用到其他 CLI。

# 调用与输入

`--print` 执行单次任务并输出最终文本：

```text
pi --print "提示词"
```

长证据可以通过 stdin 前置到首条提示，或在提示中使用 `@path` 附加文件。把进程工作目录设为目标项目根目录；它会影响项目资源发现和相对路径解析，但不是文件访问边界。

# 工具与项目资源

`--tools <list>` 用给定逗号分隔列表替换默认工具集合；独立只读任务使用：

```text
pi --no-approve --no-extensions --no-session --tools read,grep,find,ls --print "提示词"
```

`--no-approve` 不加载信任门控的项目资源，`--no-extensions` 禁用发现到的扩展，`--no-session` 不持久化会话；配合工具白名单，避免项目设置或扩展绕过只读工具范围。用户明确要求继续已有会话时，不使用 `--no-session`，并确保项目写入仍受实际权限限制。Pi 默认可能启用 `read`、`bash`、`edit`、`write`，具体也受设置影响；工具列表限制不是操作系统沙箱。

`--exclude-tools <list>` 会在其他工具选择处理后禁用指定工具。

`--approve` 只表示信任并加载项目本地配置和资源，不是编辑授权，也不会改变进程的操作系统权限。Pi 及其工具仍以启动它的操作系统账户权限运行。

# 官方资料

- [Pi Command Line](https://pi.dev/docs/latest/cli)
- [Pi CLI Integration](https://pi.dev/docs/latest/cli-integration)
- [Run Pi Safely](https://pi.dev/docs/latest/security)
