#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_cn_article import scan_text  # noqa: E402


class ScanArticleTests(unittest.TestCase):
    def test_excludes_frontmatter_and_fenced_examples(self) -> None:
        fenced = chr(96) * 3
        text = (
            "---\n"
            "title: Sample\n"
            "---\n\n"
            "以下是根据您的要求生成的文章。\n\n"
            f"{fenced}text\n"
            "TODO: this example is intentionally hidden from the prose scan\n"
            f"{fenced}\n"
        )
        result = scan_text(text)
        ids = {item["id"] for item in result["signals"]}
        self.assertIn("prompt_residue", ids)
        self.assertNotIn("placeholder", ids)

    def test_counts_style_signals_without_verdict(self) -> None:
        result = scan_text("首先说明问题。其次说明原因。不是结束，而是开始。")
        by_id = {item["id"]: item for item in result["signals"]}
        self.assertEqual(by_id["mechanical_connectors"]["count"], 2)
        self.assertEqual(by_id["parallel_constructions"]["count"], 1)
        self.assertIn("not an authorship detector", result["notice"])
        self.assertNotIn("ai_score", result)

    def test_detects_low_information_narrative_transition_buffer(self) -> None:
        text = "但我没有马上开始执行，而是多问了一句：这份方案什么时候算完成？"
        result = scan_text(text)
        by_id = {item["id"]: item for item in result["signals"]}
        self.assertEqual(by_id["narrative_transition_buffer"]["count"], 1)
        self.assertEqual(by_id["narrative_transition_buffer"]["severity"], "low")

    def test_does_not_flag_informative_contrast_as_transition_buffer(self) -> None:
        text = "但我没有接受这个方案，而是保留了原来的设计。"
        ids = {item["id"] for item in scan_text(text)["signals"]}
        self.assertNotIn("narrative_transition_buffer", ids)

    def test_detects_first_person_scaffolding_without_treating_it_as_authorship_verdict(self) -> None:
        result = scan_text("我先想到的是范围问题。我觉得最容易忽略的是未知状态。")
        by_id = {item["id"]: item for item in result["signals"]}
        self.assertEqual(by_id["first_person_scaffolding"]["count"], 2)
        self.assertEqual(result["metrics"]["first_person_mentions"], 2)
        self.assertIn("not an authorship detector", result["notice"])

    def test_keeps_first_person_action_out_of_scaffolding_signal(self) -> None:
        result = scan_text("我打开日志，看到 activeDisplayID 已经变成 A。")
        ids = {item["id"] for item in result["signals"]}
        self.assertNotIn("first_person_scaffolding", ids)

    def test_reports_metrics_and_markdown_structure(self) -> None:
        text = "# 标题\n\n第一段。\n\n- 列表项\n- 列表项\n\n第二段。第二段。"
        result = scan_text(text)
        metrics = result["metrics"]
        self.assertEqual(metrics["headings"], 1)
        self.assertEqual(metrics["paragraphs"], 3)
        self.assertEqual(metrics["sentences"], 3)
        self.assertEqual(metrics["lists"], 2)
        self.assertIn("sentence_length_cv", metrics)
        self.assertIn("review_limits", result)

    def test_repeated_content_is_a_candidate_not_a_verdict(self) -> None:
        result = scan_text("这是一段重复内容。\n\n这是一段重复内容。")
        self.assertTrue(result["metrics"]["repeated_ngrams"])
        self.assertEqual(result["review_limits"][0]["status"], "not_checked")


if __name__ == "__main__":
    unittest.main()
