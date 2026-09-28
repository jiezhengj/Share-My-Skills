# 安装

需要 Node.js 20+ 和 npm；目标技能目录已存在时，先处理冲突，不要覆盖。在要安装技能的目标项目中，发给 Agent 的指令：

> 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/headless-agent-delegation .agents/skills/headless-agent-delegation`

# 适用范围

只在用户明确要求调用已安装的外部 Agent CLI 时使用，例如让 `agy`、`cmdc`、OpenCode 或 Pi 评审、检查、执行或修改任务。用户只询问安装、版本、参数或排错时，不启动委派。

# 执行评审

- 用户点名 CLI 时使用指定 CLI；未点名时，检查项目根目录 `.headless-agent-delegation.json` 中的 `last_successful_cli`，记录不存在或命令不可用时询问用户。
- 提示词写清目标、范围、待回答的问题和所需结论。普通评审使用 CLI 默认工具、权限和配置，不因“评审”自动添加只读模式、工具白名单、sandbox 或自定义 Agent。
- 从目标项目根目录启动，保留项目配置与当前运行环境。大量文件让 CLI 在项目中搜索和读取；不要把整份仓库拼进提示参数。
- 用户明确要求禁止尝试某个工具时，先确认 CLI 能否实际排除该工具。运行时拒绝不等于没有发起请求。
- 退出码或协议成功状态不代表评审完成。检查最终答复是否给出用户要求的结论和证据；需要诊断时查看 CLI 原生事件。

各 CLI 的调用与事件字段见 [主技能说明](SKILL.md) 和 `references/`。
