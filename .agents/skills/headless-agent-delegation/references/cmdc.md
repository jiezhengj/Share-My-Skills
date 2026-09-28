本文件只记录 `cmdc` 的 headless 调用差异；不要把这些参数套用到其他 CLI。

# 调用与输入

短提示使用 `-p`：

```text
cmdc -p "提示词"
```

长提示不要放入命令行参数。省略查询参数，向 `cmdc -p` 的 stdin 发送提示词；输入结束后关闭 stdin。把进程工作目录设为目标项目根目录。

# 权限

Headless 默认阻止文件编辑和 shell 命令。只有用户明确授权修改后，才考虑 `--permission-mode accept-edits`：它允许常规工作区编辑及一组安全文件命令；它不自动批准任意 shell 命令。不要默认使用 `--yolo`。

普通委派使用默认文本输出即可；`--output-format json` 是 NDJSON 事件流，不是单个 JSON 文档。

# 官方资料

- [Command Code Headless Mode](https://commandcode.ai/docs/headless)
- [Command Code Permissions](https://commandcode.ai/docs/permissions)
