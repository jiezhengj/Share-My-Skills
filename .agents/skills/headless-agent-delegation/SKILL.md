---
name: headless-agent-delegation
description: "Use only when the user explicitly asks the calling Agent to delegate a bounded task to an installed external coding agent through its headless CLI, such as agy, cmdc, OpenCode, or pi."
---

# 何时使用与选择 CLI

用户明确要求调用外部 Agent CLI 执行或检查任务时使用本技能；只问安装、版本、参数或故障排查时不启动委派。

用户点名 CLI 时使用指定 CLI。用户一次点名多个 CLI 时，按用户要求分别调用。用户未指定时，读取项目根目录 `.headless-agent-delegation.json` 的 `last_successful_cli`；仅当值是 `agy`、`cmdc`、`opencode` 或 `pi` 且命令已安装时复用，否则询问用户选择。

# 编写和启动评审任务

提示词写清评审目标、项目或文件范围、要回答的问题和交付格式。外部 CLI 不会自动获得当前 Codex 对话中的背景；只补充完成任务所需的背景。

普通评审要求返回评审结论，不默认添加“只读”“禁止命令”“禁止工具”或“不得写入”等额外限制，也不为此切换到 plan/sandbox 模式、工具白名单或预配置 Agent。评审任务用 CLI 默认工具和权限启动；用户明确提出零工具尝试或其他硬限制时，先确认目标 CLI 能在本次调用中真正实施该限制，执行时被拒绝不等于没有尝试。

从目标项目根目录启动，让 CLI 找到正确文件和项目配置。保留该项目及当前终端已有的配置、认证和环境变量；不要为让请求通过而替换配置、账号、provider 或 model。不要假定用户预先配置了自定义 Agent；只有用户明确要求，且当前安装版本的帮助和可用 Agent 列表确认该 Agent 存在时才选用。

先查目标 CLI 当前安装版本的 `--help` 和对应适配参考，不跨 CLI 套用参数。长提示或大量文件按该 CLI 支持的文件、stdin 或目录读取方式提供；不要把整份仓库内容拼进命令行参数。

# 判断任务是否完成

退出码或协议中的成功状态只说明 CLI 结束运行。调用方还要检查最终答复是否包含用户要求的结论、证据和格式；没有最终结论的运行不算完成。

需要定位运行摩擦时，使用对应 CLI 的原生事件或日志，区分工具请求、工具实际执行或拒绝、最终答复。只在需要观察进度或诊断失败时启用该 CLI 的事件输出格式；事件输出只改变观察方式，不代表权限隔离。

provider、认证或额度错误只说明这次请求；不能据此推断账户整体状态，也不能擅自切换账号、provider 或 model。把未完成的调用和未知项如实报告。

# 修改边界

用户要求评审时，交付评审报告，不额外委派修改。用户明确授权修改时，才让外部 CLI 修改文件，并在提示词中写清修改范围和验收条件。若实际运行出现超出任务的文件变化，先检查再报告。

CLI 专属调用和事件字段见 [agy](references/agy.md)、[pi](references/pi.md)、[OpenCode](references/opencode.md) 和 [CMDc](references/cmdc.md)。
