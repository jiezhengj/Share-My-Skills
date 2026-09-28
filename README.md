# 项目简介

这里收录的是我日常自建和积累、并挑选出来公开分享的 Agent 技能。每个技能都是独立包，有自己的适用场景、执行说明和所需资料，可以按需单独使用；不需要一次安装全部技能，也不依赖其他技能。

技能采用 `.agents/skills/<技能名>/` 目录结构。支持该格式的 Agent 可以读取技能目录中的 `SKILL.md`，并在相关任务中使用对应规则。本仓库提供技能文件，不是需要单独启动的应用。

# 技能列表

每行包含技能简介和一条可直接交给 Agent 执行的命令。命令使用第三方工具 [degit](https://www.npmjs.com/package/degit)，只下载指定技能目录，不克隆整个仓库；需要 Node.js 和 npm，当前版本要求 Node.js 20 或更高版本。若目标目录已存在，请先处理冲突，不要覆盖。

| 技能与用途 | 发给 Agent 的指令 |
| --- | --- |
| [adaptive-life-consulting](.agents/skills/adaptive-life-consulting/README.zh.md)<br>梳理生活选择、习惯、职业和日常困惑；根据关键未知选择提问、查证、回顾过往行为、形成暂时判断或设计现实尝试。 | 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/adaptive-life-consulting .agents/skills/adaptive-life-consulting` |
| [article-editor](.agents/skills/article-editor/README.md)<br>以编辑部式流程改进中文文章：诊断和访谈、确认编辑简报、按授权改写，并从读者角度检查成稿。 | 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/article-editor .agents/skills/article-editor` |
| [article-structure](.agents/skills/article-structure/README.md)<br>整理文章标题、段落和内容层级，同时保留正文文字与顺序。 | 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/article-structure .agents/skills/article-structure` |
| [cn-natural-writing-editor](.agents/skills/cn-natural-writing-editor/README.md)<br>支持中文文章的写前规划、写作、诊断、授权改写和冷读，关注证据、作者声音与读者理解。 | 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/cn-natural-writing-editor .agents/skills/cn-natural-writing-editor` |
| [headless-agent-delegation](.agents/skills/headless-agent-delegation/README.zh.md)<br>在用户明确要求时，将边界清楚的任务交给已安装的外部编码 Agent CLI，并约束调用和文件修改范围。 | 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/headless-agent-delegation .agents/skills/headless-agent-delegation` |

Agent 对技能目录的发现和配置方式因产品而异。安装后，技能规则与限制见对应目录中的 `SKILL.md`，简介见该目录中的 `README` 文件。

# 项目结构

```text
.agents/
└── skills/
    ├── adaptive-life-consulting/
    ├── article-editor/
    ├── article-structure/
    ├── cn-natural-writing-editor/
    └── headless-agent-delegation/
```

每个技能目录都是一个独立单元。`SKILL.md` 提供 Agent 执行规则；`README` 面向使用者；`references/`、`scripts/` 和 `agents/` 等目录按技能需要提供补充资料、校验工具或 Agent 元数据。安装时请复制整个技能目录，以免遗漏这些文件。

# 修改与验证

技能的适用条件、流程和限制以对应目录中的 `SKILL.md` 为准。修改技能时，请检查同目录中的 README、参考资料、脚本和相对链接是否仍与规则一致。各技能的校验方式不同；如需验证，请查看该技能的 README 或 `SKILL.md`。
