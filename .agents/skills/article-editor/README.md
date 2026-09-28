这是一个面向中文文章的编辑部式编辑技能。它先判断文章要对读者完成什么承诺，再根据材料、证据和作者意图决定干预层级；它不是泛化的顺句或润色工具。

**发给 Agent 的指令**

需要 Node.js 20+ 和 npm；目标技能目录已存在时，请先处理冲突，不要覆盖。在要安装技能的目标项目中发送：

> 请在当前项目执行：`npx degit jiezhengj/Share-My-Skills/.agents/skills/article-editor .agents/skills/article-editor`

# 适用场景

- 文章像个人备忘录，读者不知道从哪里进入。
- 文章缺少背景、例子、证据、限制或清晰的结尾。
- 文章叙述性弱、读者路径断裂，或技术内容与个人经历混在一起。
- 用户提出“可读性不高”“逻辑不清”“不像人在写”等写作质量问题。
- 用户希望在保留事实和作者声音的前提下进行发展性编辑、实质性编辑或改写。

# 工作流程

默认按以下顺序推进：

1. `diagnose`：识别读者、文章类型、中心问题、主张、证据和信息缺口，不修改目标文档。
2. `interview`：只询问会改变文章结构、事实边界或读者承诺的高价值问题。
3. `brief`：形成读者契约、主张、材料权限、结构、边界和结尾的编辑简报，等待作者确认。
4. `rewrite`：确认后只改写用户指定的目标文档，保持目标路径不变。
5. `cold-read`：从陌生读者角度检查理解路径、事实回归和剩余问题。

原始访谈和补充材料保存在目标对应的 `.article-editor/records/<target-id>/` 记录目录中。原始记录只追加，不覆盖；编辑简报和冷读报告属于可重建的派生记录。

# 编辑边界

- 不编造经历、案例、数字、来源、限制或结论。
- 不在作者确认编辑简报前修改目标文档。
- 不移动目标文档，不擅自创建第二个最终版本。
- 区分事实、经历、观察、推断、建议和未解决问题。
- 用户只要求局部校改时，不擅自扩展为全文改写。
- 文章质量反馈会触发技能自检，但不会因为单个 bad case 自动修改技能本身。

# 参考资料与验证

- `references/article-genre-rubric.md`：文章类型判断。
- `references/author-style.md`：作者声音和结构风险。
- `references/narrative-quality-rubric.md`：叙述质量、作者在场感和材料边界。
- `references/interview-question-bank.md`：自适应访谈问题。
- `references/reader-validation-rubric.md`：冷读验证。
- `scripts/validate_skill_portable.py`：技能便携性自检。

Windows PowerShell 可运行：

```text
python -X utf8 <skill-dir>/scripts/validate_skill_portable.py --skill-dir <skill-dir>
```

更完整的执行约束以 [`SKILL.md`](SKILL.md) 为准。
