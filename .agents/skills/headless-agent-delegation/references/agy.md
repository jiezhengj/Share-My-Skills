# agy 适配说明

本文件只记录 `agy` 的已验证调用差异；使用其他外部 Agent CLI 时不要套用这些参数。

## 基本调用

短提示优先使用 `-p`：

```text
agy -p "Reply exactly AGY_OK." --output-format json --print-timeout 0
```

当前 CLI 对长格式 `--print` 要求提示词直接绑定到参数；不要把提示词作为未绑定的单独参数传入 `--print`，因为后续的 `--output-format` 等选项可能被误当成提示词。应写成：

```text
agy --print="Reply exactly AGY_OK." --output-format json --print-timeout 0
```

长提示、长评审证据和多轮任务使用：

```text
agy --input-format stream-json --output-format stream-json
```

每行发送一个用户事件：

```json
{"event":"user","message":{"content":"完整提示词"}}
```

`content` 只能是字符串或 `text` 块；单轮任务发送后也必须关闭 stdin，并等待最终 `result`。

## slash 命令

提示词中需要原样处理 `/model`、`/usage` 或其他 slash 文本时，加上 `--disable-slash-commands`；如果任务依赖 slash 命令或技能展开，则不能添加该选项。

## 权限、工作区与模式

不需要 shell 的只读任务，在提示词开头明确要求：

```text
只使用本次会话实际提供的只读文件或搜索工具；不要调用 run_command/RunCommand 或任何写入、编辑、删除工具。若缺少必要的只读能力，说明缺口并停止，不要改用 shell。
```

这是提示词约束，不是权限沙箱：Headless 默认权限模式虽显示为 `request-review`，但官方说明活动工作区内的文件读取和写入仍会自动允许。当前 CLI 帮助没有专用的 `--read-only` 开关；`--mode=plan` 是规划模式，不构成写入隔离，也可能创建计划文档。

官方 CLI 权限配置支持 `permissions.deny` 规则，例如拒绝指定路径的 `write_file`。这不是整体只读模式：shell 命令由独立的 `command` 权限控制，仅限制文件写入工具不足以阻止命令改写工作区。未获修改授权时，只有确认本次会话实际采用的权限规则覆盖评审目录和可能产生写入的命令，或操作系统隔离确实阻止这些写入后，才启动只读评审。不能仅凭提示词、`request-review`、`--mode=plan` 或设置文件中出现规则就认定写入已被阻止。

Headless 下需要确认的 shell 工具可能被软拒绝；JSON 中常见动作名为 `command`，显示名可能是 `RunCommand`。即使退出码为 `0`、状态为 `SUCCESS`，也可能同时得到空 `response` 和 `denied_actions`，这不算完成。

如果任务确实需要命令，用户应在 `~/.gemini/antigravity-cli/settings.json` 的 `permissions.allow` 中按任务配置最窄规则。`command(git)` 会匹配常规 Git 命令，不是只读白名单；Windows 上若需匹配 Git 子命令，官方文档要求使用 `regex:` 规则。不要自动修改该设置，也不要使用全局放行或 `--dangerously-skip-permissions`。

`--sandbox` 为终端命令增加操作系统级文件系统和网络隔离，但项目目录仍可读写；它不会授予普通命令权限，也不保证项目只读。`--mode=plan` 可能创建计划文档并等待批准；普通只读分析不要默认使用它。只有用户明确授权修改文件时才使用 `--mode=accept-edits`，并由调用方 Agent 检查实际变化。

若 Git 工作区探测持续触发无关命令拒绝，可从非 Git 中立目录启动，并使用 `--add-dir <project>` 添加项目；此时提示词必须使用绝对路径。`--add-dir` 只扩展工作区，不限制写入；只读任务只有在另有已验证的权限规则或操作系统隔离阻止项目写入时才能使用，否则不要采用此回避方式。`--project`、`--new-project` 和 `--remote-control` 会改变项目或连接生命周期，只在用户明确要求时使用。

官方参考：[Headless mode](https://antigravity.google/docs/cli/headless/) 和 [Permissions](https://antigravity.google/docs/permissions?tab=cli)。具体参数以当前机器上的 `agy --help` 为准。
