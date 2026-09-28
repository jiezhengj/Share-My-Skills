本文件只记录 `cmdc` 的 headless 调用差异；不要把这些参数套用到其他 CLI。

# 调用与输入

确认目标项目根目录后再启动。用户已明确授权 cmdc 在该项目中执行任务时，使用 `--trust` 跳过初次项目授权提示；它不会打开文件编辑、shell 命令或 `-p` 默认禁用的工具权限。

短提示使用 `-p`，并带上 `--trust`：

```text
cmdc --trust -p "提示词"
```

长提示不要放入命令行参数。省略查询参数，把提示词发送到 `cmdc --trust --output-format json -p` 的 stdin；输入结束后关闭 stdin。把进程工作目录设为已确认的目标项目根目录。

# 权限

Headless 默认阻止文件编辑和 shell 命令。只有用户明确授权修改后，才考虑 `--permission-mode accept-edits`：它允许常规工作区编辑及一组安全文件命令；它不自动批准任意 shell 命令。不要默认使用 `--yolo`。

短任务可以使用默认文本输出。多文件或预计多轮的任务使用 `--output-format json` 观察进度。它输出 NDJSON 事件流，不是单个 JSON 文档；逐行读取，直到收到最终 `type: "result"` 行。

事件用于区分启动、工具工作和模型等待：`run_start` 表示本次运行已启动，`tool_running` / `tool_completed` 表示单个工具的状态，`model_request_start` / `model_request_end` 表示模型请求的状态。工具完成不代表整项任务完成；没有最终 `result` 就不能报告成功。

默认文本模式只在任务结束后输出最终答案。进程仍运行但没有文本，无法证明它停在授权提示。对长任务优先检查 JSON 事件；若在合理等待范围内没有最终结果，结束该次调用、记录最后一个事件，并按未完成状态处理。不要只因沉默就重复启动同一长任务。

# 官方资料

- [Command Code Headless Mode](https://commandcode.ai/docs/headless)
- [Command Code Permissions](https://commandcode.ai/docs/permissions)
