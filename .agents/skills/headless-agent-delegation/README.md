[中文版](README.zh.md) · [English](README.en.md)

# 简介

`headless-agent-delegation` 只在用户明确要求时，把边界清楚的任务委派给已安装的外部编码 Agent CLI。它负责选择规则、CLI 适配和修改边界，不会因为外部命令返回成功就直接假定任务完成。

# Introduction

`headless-agent-delegation` routes a clearly bounded task to an installed external coding Agent CLI only when the user explicitly asks for it. It defines CLI selection, adapter usage, and modification boundaries; a successful process exit alone is not completion evidence.

详细规则见 [主技能说明](SKILL.md)。
