这是一个保真的文章结构整理技能。它改善标题层级、段落边界和内容定位，但严格保留正文文字、顺序、链接、引用、代码、图片和表格内容。

**发给 Agent 的指令**

需要 Node.js 20+ 和 npm；目标技能目录已存在时，请先处理冲突，不要覆盖。在要安装技能的目标项目中发送：

> 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/article-structure .agents/skills/article-structure`

# 适用场景

- 梳理本地 Markdown 的标题层级和段落结构。
- 在不改写正文的情况下补充必要标题、拆分段落或整理已有并列内容。
- 处理飞书 Docx/Wiki 文档或项目 `source-ref.json` 来源快照。
- 让文章更容易理解和定位，但不把所有文本改造成同一种说明文模板。

# 输入与输出

| 来源 | 默认输出 |
| --- | --- |
| 本地 `.md` / `.markdown` | 原地更新同一文件 |
| 飞书 Docx/Wiki | 写回原飞书文档 |
| 项目 `source-ref.json` | 使用只读 `source.md`，在运行目录生成 `structured.md`，默认写回原文档 |

用户明确指定另存路径或创建副本时，以用户指定为准。飞书 URL、token 或来源快照在没有本地输出路径时，不擅自创建副本。

# 允许的结构动作

- 根据原文新增有证据支持的 Markdown 标题。
- 调整现有正文标题的层级，不修改标题文字。
- 在完整句子或明确语义边界处拆分段落。
- 谨慎添加基于原文的加粗、列表或表格。

不得改写、删减、扩写、调换或合并正文内容。标题数量、段落数量、平均长度和视觉整齐度都不是完成标准；应采用能改善理解且最少改变阅读体验的方案。

# 工作流程

1. 识别来源和输出方式，确定文档标题与正文标题的区别。
2. 通读全文，建立当前文本的阅读模型和结构地图。
3. 先整体判断关系组，再处理标题、段落、空行和强调。
4. 本地 Markdown 使用原文快照、临时修订稿和新增结构行清单。
5. 运行 `scripts/verify_preservation.py`，确认正文内容和顺序未被破坏。
6. 有文档标题元数据时运行 `scripts/verify_heading_structure.py`，确认第一个正文章节为 H1。
7. 校验通过后写回原文件，回读最终结果并再次验证。

脚本只检查确定性不变量；文本类型、作者意图、阅读节奏和标题是否破坏语气，必须结合全文判断。

# 文件说明

- `SKILL.md`：完整执行规则和飞书工作流。
- `scripts/verify_preservation.py`：正文保真校验。
- `scripts/verify_heading_structure.py`：标题层级校验。
- `scripts/validate_skill_portable.py`：便携性自检。

更完整的约束以 [`SKILL.md`](SKILL.md) 为准。
