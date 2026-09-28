这是一个中文文章写前、写中和写后的自然化编辑技能。它检查证据、信息密度、作者判断、结构、语言和误判边界，减少模板腔与 AI 化表达，但不把文章当成“AI 检测”对象，也不靠添加口语词来伪装自然。

**发给 Agent 的指令**

需要 Node.js 20+ 和 npm；目标技能目录已存在时，请先处理冲突，不要覆盖。在要安装技能的目标项目中发送：

> 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/cn-natural-writing-editor .agents/skills/cn-natural-writing-editor`

# 适用场景

- 只有主题、素材或口述，需要建立读者契约和写作提纲。
- 需要边写边组织材料、保留作者声音并记录 checkpoint。
- 需要诊断已有文章的事实、信息密度、叙述、结构、语言和读者路径。
- 需要在明确授权后分层改写，处理模板句、抽象表达、重复和语气失真。
- 需要以陌生读者视角进行冷读，检查文章是否真的完成了自己的承诺。

# 工作模式

| 模式 | 适用情况 | 默认交付 |
| --- | --- | --- |
| `prewrite` | 只有主题、素材、口述或写作计划 | 读者契约、素材地图、中心判断、提纲和风险预警 |
| `drafting` | 用户确认前置简报并要求写作 | 按小节推进的正文和 checkpoint |
| `diagnose` | 用户只要求评估已有文章 | 诊断报告，不修改目标文件 |
| `rewrite` | 用户明确允许改写已有文章 | 按最低必要等级改写并进行事实回归 |
| `cold-read` | 用户要求陌生读者检查或文章已修订 | 冷读报告和剩余问题 |

改写等级从 `L0` 到 `L4` 逐步增加干预：只报告问题、清理硬证据问题、调整读者路径、补充用户提供的过程材料，以及处理抽象词和模板化表达。优先处理事实和内容，再处理结构和语言。

# 核心边界

- 不编造作者经历、案例、数字、引用、来源、失败过程、细节或因果。
- 区分 `FACT`、`EXPERIENCE`、`OBSERVATION`、`INFERENCE`、`RECOMMENDATION` 和 `UNKNOWN`。
- 缺少会改变结构或事实边界的信息时提问；不能用顺滑措辞补齐 `UNKNOWN`。
- 不把正式、清楚或技术性强的文体直接判定为“AI 味儿”。
- 未经用户授权不覆盖目标文章，也不创建第二个最终版本。
- 默认不启用脱敏；只有用户明确要求匿名化、隐藏路径或账号等信息时才读取隐私模块。
- 发现可能是技能缺口时先说明依据并询问用户，不因一次 bad case 自动修改技能。

# 典型工作流程

写前阶段先建立 `reader-contract`、`source-map`、`claim-ledger` 和素材关系图，标记读者、主张、证据、反例、适用边界和未知项；材料不足时输出提纲并等待确认。成稿诊断按硬证据、内容证据、作者感、读者路径、结构信号、语言信号和误判边界检查。改写后执行事实回归和冷读，确认没有新增用户未提供的事实或因果。

每次任务开始先读取 `references/coverage-matrix.md`。主要资源包括：

- `references/content-and-claim-audit.md`：内容、事实、来源和判断。
- `references/author-voice.md`：作者声音和具体性。
- `references/ai-flavor-signals.md`：模板化表达与误判边界。
- `references/reader-facing-narrative.md`：读者路径和叙述推进。
- `references/rewrite-patterns.md`：具体改写动作和禁止动作。
- `references/cold-read-rubric.md`：冷读验收。
- `scripts/scan_cn_article.py`：确定性信号扫描，仅供人工复核。

# 验证

Windows PowerShell 可运行：

```text
python -X utf8 <skill-dir>/scripts/test_skill_contract.py
python -X utf8 <skill-dir>/scripts/validate_coverage.py <skill-dir> --format json
```

两项检查通过且覆盖矩阵没有错误后，后续同类反馈优先报告 `NO_GAP_FOUND`；只有出现新失败类型、规则冲突或回归失败时，才重新评估技能本身。

更完整的规则以 [`SKILL.md`](SKILL.md) 为准。
