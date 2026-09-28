#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_cn_article import scan_text  # noqa: E402
from validate_coverage import validate  # noqa: E402


class SkillContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_dir = Path(__file__).resolve().parents[1]
        self.article_editor_dir = self.skill_dir.parent / "article-editor"

    def require_article_editor_integration(self) -> None:
        if not self.article_editor_dir.is_dir():
            self.skipTest("article-editor integration checks require the sibling skill in the full MySkills repository")

    def test_formal_report_is_not_high_risk_by_structure_alone(self) -> None:
        text = (
            "# 测试报告\n\n"
            "## 方法\n\n样本来自公开记录，统计口径和日期已在附录说明。\n\n"
            "## 结果\n\n结果仅适用于本次样本，不推断其他场景。"
        )
        result = scan_text(text)
        self.assertFalse(any(item["severity"] == "high" for item in result["signals"]))

    def test_template_article_exposes_multiple_low_level_signals(self) -> None:
        text = (
            "首先说明背景。其次分析优势。最后展望未来。"
            "这不仅是一次升级，更是一次深刻变革。"
        )
        ids = {item["id"] for item in scan_text(text)["signals"]}
        self.assertTrue({"mechanical_connectors", "parallel_constructions"} <= ids)

    def test_prompt_residue_is_high_priority_but_not_authorship_verdict(self) -> None:
        result = scan_text("以下是根据您的要求生成的文章。")
        self.assertEqual(result["signals"][0]["severity"], "high")
        self.assertIn("not an authorship detector", result["notice"])

    def test_privacy_is_opt_in_in_the_skill_contract(self) -> None:
        skill_text = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("privacy_opt_in = false", skill_text)
        self.assertIn("optional-privacy-module.md", skill_text)
        self.assertIn("不询问、不扫描、不替换身份信息", skill_text)

    def test_writing_quality_feedback_triggers_skill_self_check(self) -> None:
        skill_text = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("写作质量反馈触发技能自检", skill_text)
        self.assertIn("Skill 问题", skill_text)
        self.assertIn("是否要同步优化 Skill？你确认后我再修改 Skill 本身。", skill_text)
        self.assertIn("不修改 `SKILL.md`、`references/`、`scripts/` 或 `agents/openai.yaml`", skill_text)
        self.assertIn("任何与写作质量有关的问题", skill_text)
        self.assertIn("普通措辞、标点或局部表达问题执行轻量自检", skill_text)
        self.assertIn("skill-feedback-loop.md", skill_text)
        self.assertIn("NO_GAP_FOUND", skill_text)

    def test_reader_path_rules_keep_documents_distinct_from_articles(self) -> None:
        skill_text = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        narrative_text = (self.skill_dir / "references/reader-facing-narrative.md").read_text(
            encoding="utf-8"
        )
        cold_read_text = (self.skill_dir / "references/cold-read-rubric.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("读者路径", skill_text)
        self.assertIn("说明书或正式技术文档", narrative_text)
        self.assertIn("原本会怎样理解", narrative_text)
        self.assertIn("不能只把结论、规则和代码示例依次摆出来", narrative_text)
        self.assertIn("不要把人的思考压平", narrative_text)
        self.assertIn("读者视角也不是", narrative_text)
        self.assertIn("理解路径检查", cold_read_text)

    def test_source_authority_and_case_concept_rules_are_present(self) -> None:
        skill_text = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        narrative_text = (self.skill_dir / "references/reader-facing-narrative.md").read_text(
            encoding="utf-8"
        )
        matrix_text = (self.skill_dir / "references/coverage-matrix.md").read_text(encoding="utf-8")
        self.assertIn("素材关系图", skill_text)
        self.assertIn("来源权限", skill_text)
        self.assertIn("第一人称叙述支架", (self.skill_dir / "references/rewrite-patterns.md").read_text(encoding="utf-8"))
        self.assertIn("第一人称的功能", (self.skill_dir / "references/author-voice.md").read_text(encoding="utf-8"))
        process_text = (self.skill_dir / "references/process-and-stop.md").read_text(encoding="utf-8")
        self.assertIn("素材来源与关系权限", narrative_text)
        self.assertIn("案例/观察 → 暴露的问题 → 概念或资料解释", narrative_text)
        self.assertIn("判断轨迹与过程收口", process_text)
        self.assertIn("局部成功", process_text)
        self.assertIn("整体是否推进", process_text)
        self.assertIn("手动中止", process_text)
        self.assertIn("素材来源权限与跨材料推断边界", matrix_text)

    def test_article_editor_has_the_same_narrative_closure_contract(self) -> None:
        self.require_article_editor_integration()
        article_editor_dir = self.article_editor_dir
        skill_text = (article_editor_dir / "SKILL.md").read_text(encoding="utf-8")
        rubric_text = (article_editor_dir / "references/narrative-quality-rubric.md").read_text(
            encoding="utf-8"
        )
        reader_text = (article_editor_dir / "references/reader-validation-rubric.md").read_text(
            encoding="utf-8"
        )
        article_skill_text = skill_text
        self.assertIn("NO_GAP_FOUND", skill_text)
        self.assertIn("技能优化封口", skill_text)
        self.assertIn("素材权限与编织方式", rubric_text)
        self.assertIn("案例或观察 → 暴露出的问题", rubric_text)
        self.assertIn("叙述支架", article_skill_text)
        self.assertIn("第一人称叙述支架", rubric_text)
        self.assertIn("人的判断与模型化表达", rubric_text)
        self.assertIn("多段以第一人称开头", reader_text)
        self.assertIn("案例—方法关系", reader_text)
        self.assertIn("判断轨迹", skill_text)
        self.assertIn("局部成功", skill_text)
        self.assertIn("局部成功冒充整体进展", rubric_text)
        self.assertIn("无限查漏、没有收口依据", rubric_text)
        self.assertIn("收口依据", reader_text)
        self.assertIn("整体进展", reader_text)
        self.assertNotIn("那份看起来完整的方案", rubric_text)
        self.assertNotIn("我问了 Agent", rubric_text)

    def test_process_guidance_is_form_based_not_agent_topic_based(self) -> None:
        self.require_article_editor_integration()
        cn_skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        process_text = (self.skill_dir / "references/process-and-stop.md").read_text(
            encoding="utf-8"
        )
        article_editor_skill = (self.skill_dir.parent / "article-editor/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("判断轨迹", cn_skill)
        self.assertIn("trajectory_mode", cn_skill)
        self.assertIn("`ENABLE`", cn_skill)
        self.assertIn("`SKIP`", cn_skill)
        self.assertIn("`UNKNOWN`", cn_skill)
        self.assertIn("不依据是否出现 Agent、Workflow 等主题词", cn_skill)
        self.assertIn("过程型叙事", article_editor_skill)
        self.assertIn("trajectory_mode", article_editor_skill)
        self.assertIn("不是主题关键词", process_text)
        self.assertIn("纯技术文档、纯观点文", process_text)
        self.assertIn("路由示例", process_text)
        self.assertIn("一个团队在一项长期任务中反复修订", process_text)
        self.assertNotIn("只有当文章的核心主题是 Agent/Goal/Workflow", cn_skill)

    def test_project_recap_guard_and_source_fidelity_are_present(self) -> None:
        self.require_article_editor_integration()
        cn_skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        ai_flavor_text = (self.skill_dir / "references/ai-flavor-signals.md").read_text(
            encoding="utf-8"
        )
        process_text = (self.skill_dir / "references/process-and-stop.md").read_text(
            encoding="utf-8"
        )
        voice_text = (self.skill_dir / "references/author-voice.md").read_text(encoding="utf-8")
        article_editor_skill = (self.skill_dir.parent / "article-editor/SKILL.md").read_text(
            encoding="utf-8"
        )
        article_rubric = (
            self.skill_dir.parent / "article-editor/references/narrative-quality-rubric.md"
        ).read_text(encoding="utf-8")
        article_reader = (
            self.skill_dir.parent / "article-editor/references/reader-validation-rubric.md"
        ).read_text(encoding="utf-8")

        self.assertIn("项目经历履历化/报告化", cn_skill)
        self.assertIn("项目经历的履历化/报告化", ai_flavor_text)
        self.assertIn("阶段标签也不等于判断轨迹", process_text)
        self.assertIn("原话与改写的来源回归", voice_text)
        self.assertIn("作者原话可以凝缩", cn_skill)
        self.assertIn("项目经历的履历化与报告化", article_rubric)
        self.assertIn("作者原话与模型新增概括的区分", article_rubric)
        self.assertIn("项目复盘连续按", article_reader)
        self.assertIn("履历化/报告化", article_editor_skill)

    def test_coverage_and_resources_are_consistent(self) -> None:
        result = validate(self.skill_dir)
        self.assertEqual(result["status"], "PASS", result["errors"])


    def test_human_narrative_shape_contract_is_present(self) -> None:
        self.require_article_editor_integration()
        cn_skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        shape_text = (self.skill_dir / "references/human-narrative-shape.md").read_text(
            encoding="utf-8"
        )
        samples_text = (self.skill_dir / "references/human-narrative-samples.md").read_text(
            encoding="utf-8"
        )
        signals_text = (self.skill_dir / "references/ai-flavor-signals.md").read_text(
            encoding="utf-8"
        )
        matrix_text = (self.skill_dir / "references/coverage-matrix.md").read_text(
            encoding="utf-8"
        )
        boundaries_text = (self.skill_dir / "references/false-positive-boundaries.md").read_text(
            encoding="utf-8"
        )
        article_editor_skill = (self.skill_dir.parent / "article-editor/SKILL.md").read_text(
            encoding="utf-8"
        )
        article_rubric = (
            self.skill_dir.parent / "article-editor/references/narrative-quality-rubric.md"
        ).read_text(encoding="utf-8")

        # 共享形态参考存在并声明边界：对话样本非写作样本
        self.assertIn("对话形态 ≠ 写作形态", shape_text)
        self.assertIn("非写作", samples_text)
        self.assertIn("边界", samples_text)
        # 禁止表演人类：不能靠换词、氛围细节、自报情绪、对话腔去味
        self.assertIn("禁止用换词、加氛围细节、自报情绪或造对话腔来表演人类", cn_skill)
        self.assertIn("氛围性细节", boundaries_text)
        # 形态信号接入 cn 诊断、信号层与覆盖矩阵
        self.assertIn("human-narrative-shape.md", cn_skill)
        self.assertIn("概念命名", signals_text)
        self.assertIn("情绪缺席", signals_text)
        self.assertIn("人类叙事形态", matrix_text)
        # article-editor 引用同一形态参考，并把形态问题路由回访谈
        self.assertIn("human-narrative-shape.md", article_editor_skill)
        self.assertIn("不得靠改写表演人类", article_editor_skill)
        self.assertIn("概念命名过密", article_rubric)


if __name__ == "__main__":
    unittest.main()
