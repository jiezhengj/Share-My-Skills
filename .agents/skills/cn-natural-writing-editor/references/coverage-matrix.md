# 原最佳实践覆盖矩阵

用途：规定 Skill 对原最佳实践的功能覆盖。每次任务先读取本文件，再决定需要哪些检查和 reference。

状态：`FOUND` 表示发现问题；`CLEAR` 表示在当前输入范围内检查后未发现问题；`UNKNOWN` 表示证据不足；`NOT_APPLICABLE` 表示当前输入不包含该上下文。`UNKNOWN` 和 `NOT_APPLICABLE` 都不能当作通过。

## 目录

- [覆盖矩阵](#覆盖矩阵)
- [实现门槛](#实现门槛)

## 覆盖矩阵

| 原最佳实践维度 | 优先级 | Skill 执行位置 | 参考文件 | 脚本/测试 | 必需输入 |
| --- | --- | --- | --- | --- | --- |
| 提示词残留、占位符、模型客套话 | 高 | 硬证据检查 | `ai-flavor-signals.md` | `scan_cn_article.py` | 文章文本 |
| 虚构引用、无来源数字、时间线和因果冲突 | 高 | 内容与事实核查 | `content-and-claim-audit.md` | 仅提示候选 | 原文、来源或作者材料 |
| 引用—论点一致性、术语和统计口径 | 高 | 内容与事实核查 | `content-and-claim-audit.md` | 不自动证明 | 引用原文、定义、口径 |
| 信息密度、机制、案例、反例、取舍 | 高 | 内容审查、作者提问 | `content-and-claim-audit.md` | 不自动证明 | 文章和素材 |
| 判断轨迹、局部成功、假成功、成本和过程收口（按文章形态启用） | 条件高 | `trajectory_mode = ENABLE` 后：source-map、判断轨迹、结构诊断、冷读 | `process-and-stop.md`、`reader-facing-narrative.md` | `test_skill_contract.py` | 文章核心需要呈现认识和行动的变化，并有时间线、行动、结果、成本或停止依据 |
| 项目经历履历化、阶段同构与作者判断被压平 | 条件高 | 过程型文章的结构诊断、source-map、冷读 | `ai-flavor-signals.md`、`process-and-stop.md`、`author-voice.md` | `test_skill_contract.py` | 项目复盘或个人经历中存在多个阶段、工具或成果归纳 |
| 人类叙事形态：命名/升华/否定对仗密度、情绪缺席、氛围性细节 | 条件高 | 具体性诊断、结构诊断、冷读 | `human-narrative-shape.md`、`human-narrative-samples.md` | `test_skill_contract.py` | 个人文章或复盘类成稿 |
| 原创观察、作者判断和适用边界 | 高 | 素材地图、claim ledger、冷读 | `author-voice.md` | 不自动证明 | 作者补充材料 |
| 素材来源权限与跨材料推断边界 | 高 | source-map、素材关系图、事实回归 | `reader-facing-narrative.md`、`content-and-claim-audit.md` | `test_skill_contract.py` | 原始素材、外部资料、作者确认 |
| 读者路径、理解推进和认知转折 | 中高 | 文章类型路由、写前提纲、结构诊断、冷读 | `genre-routing.md`、`reader-facing-narrative.md`、`cold-read-rubric.md` | 人工冷读回归 | 文章类型、读者契约、原始材料 |
| 段落同构、三点清单、重复总结、强行开结尾、低信息量叙述过渡 | 中高 | 结构检查和 L2 改写 | `ai-flavor-signals.md`、`rewrite-patterns.md` | 段首和基础指标、过渡句候选扫描 | Markdown 文章 |
| 抽象套话、机械连接词、对称句、泛比喻 | 中 | 语言检查和 L4 改写 | `ai-flavor-signals.md`、`rewrite-patterns.md` | 正则信号扫描 | Markdown 文章 |
| 对向检查：表演人味 / 工整论文感 / 浓淡错位（含上价值机制、元话语、空转支架/限定词、悬空指示词、无出处比喻、廉价强度词、防御性自证、回顾渲染、标题失真） | 高 | 成稿诊断流程“对向检查”块 + `ai-flavor-signals.md`“对向检查”章节 | `ai-flavor-signals.md` | 无（人工判断，不建黑名单） | 文章文本 |
| 情绪失真、过度积极或过度中性 | 中 | 语气和具体性检查 | `content-and-claim-audit.md`、`author-voice.md` | 仅候选统计 | 文章和事件背景 |
| 文化、地域和生活细节表面化 | 中 | 具体性与文体检查 | `content-and-claim-audit.md`、`genre-routing.md` | 不自动证明 | 文章、地点和读者背景 |
| 可读性、同义复述、句段波动 | 中低 | 冷读和统计辅助 | `quantitative-and-publishing-signals.md` | 句段、重复指标 | Markdown 文章 |
| 术语边界漂移和风格局部突变 | 中高 | 术语、证据强度和冷读 | `content-and-claim-audit.md`、`false-positive-boundaries.md` | 仅候选统计 | 术语定义、原文 |
| 跨文章重复、批量发布、主题跨度和署名异常 | 中 | 发布上下文检查 | `quantitative-and-publishing-signals.md` | 不扫描单篇外部行为 | 发布记录或多篇文章 |
| 检测器分数和文体统计的可靠性限制 | 高 | 误判边界和交付说明 | `false-positive-boundaries.md` | 输出限制声明 | 工具结果和文体信息 |
| 脱敏 | 另行触发 | `privacy_opt_in = true` 时执行 | `optional-privacy-module.md` | 不默认扫描 | 用户明确请求 |

## 实现门槛

以下条件全部满足，才允许把一次完整实现标记为 `EQUIVALENT`：

1. 所有高优先级行都有可执行规则、输出状态和验证方式。
2. 中低优先级行都有规则和误判边界；没有输入时明确写 `UNKNOWN` 或 `NOT_APPLICABLE`。
3. 自动化脚本只报告可解释信号，不生成作者身份结论。
4. 正式报告、技术文章、自然文章、模板稿、人机混合稿和合法展示模型输出的反向测试通过。
5. 用户未明确要求脱敏时，隐私模块没有被读取、询问或触发。
6. 交付说明列出已检查、未知、未适用、已修改和剩余风险。

任意高优先级空缺、反向测试失败或默认脱敏触发，都只能标记为 `PARTIAL`。
