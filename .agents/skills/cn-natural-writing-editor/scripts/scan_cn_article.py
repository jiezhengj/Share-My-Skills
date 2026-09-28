#!/usr/bin/env python3
"""Deterministic signal scanner for Chinese Markdown articles.

The scanner reports explainable text and Markdown signals for human review.
It does not estimate authorship, calculate an AI score, or verify external facts.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


SIGNAL_PATTERNS: tuple[tuple[str, str, str], ...] = (
    (
        "prompt_residue",
        "high",
        r"(?:以下|下面)(?:是|为).{0,24}(?:根据|按照).{0,24}(?:要求|指令)|"
        r"(?:作为一名|根据您的要求|以下内容由模型|希望以上内容对您有所帮助)",
    ),
    (
        "placeholder",
        "high",
        r"\b(?:TODO|TBD)\b|待(?:补充|填写|确认)|"
        r"此处.{0,12}(?:补充|填写)|【[^】]{0,40}(?:补充|填写|待定)[^】]{0,40}】",
    ),
    (
        "mechanical_connectors",
        "medium",
        r"首先|其次|再次|最后|此外|与此同时|值得注意的是|总而言之|由此可见",
    ),
    (
        "parallel_constructions",
        "medium",
        r"不是.{0,36}而是|不仅.{0,36}更是|从.{1,20}到.{1,20}",
    ),
    (
        "narrative_transition_buffer",
        "low",
        r"(?:但|不过|只是)(?:我|我们)(?:没有|没|并没有).{0,12}"
        r"(?:马上|立刻|直接|立即|先).{0,18}(?:而是|转而)",
    ),
    (
        "first_person_scaffolding",
        "low",
        r"我(?:先想到|先停了一下|于是|觉得|现在(?:会|要)|后来|再看|回头)|"
        r"我的(?:感觉|理解|判断)",
    ),
    (
        "abstract_evaluations",
        "low",
        r"真正|深刻|重要|全面|显著|有效|赋能|重塑|生态|范式|抓手|动能",
    ),
    (
        "generic_metaphors",
        "low",
        r"钥匙|桥梁|引擎|浪潮|双刃剑",
    ),
    (
        "generic_ending",
        "medium",
        r"未来.{0,24}(?:值得|充满|必将|期待)|"
        r"相信.{0,24}(?:将|会)|让我们共同努力",
    ),
    (
        "absolute_claims",
        "low",
        r"绝对|必然|必将|完全|无疑|毫无疑问|从不|永远",
    ),
)


REVIEW_LIMITS: tuple[dict[str, str], ...] = (
    {
        "id": "citation_verification",
        "status": "not_checked",
        "reason": "扫描器只能发现引用标记，不能验证来源是否存在或支持正文。",
    },
    {
        "id": "fact_and_timeline_verification",
        "status": "not_checked",
        "reason": "事实、时间线、人物和因果关系需要原始材料或外部来源。",
    },
    {
        "id": "cultural_and_regional_accuracy",
        "status": "not_checked",
        "reason": "地域和文化细节不能由词频或长度指标证明。",
    },
    {
        "id": "publishing_context",
        "status": "not_applicable",
        "reason": "单篇文章输入不包含账号、发布时间或跨文章上下文。",
    },
)


def _strip_frontmatter_and_fences(text: str) -> str:
    """Keep visible prose while excluding metadata and fenced examples."""

    lines = text.splitlines()
    output: list[str] = []
    index = 0
    if lines and lines[0].strip() == "---":
        index = 1
        while index < len(lines) and lines[index].strip() != "---":
            index += 1
        index += 1

    in_fence = False
    fence_marker = chr(96) * 3
    for line in lines[index:]:
        if line.strip().startswith(fence_marker):
            in_fence = not in_fence
            continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)


def _strip_heading_lines(text: str) -> str:
    """Keep prose metrics from treating Markdown headings as sentences."""

    return "\n".join(
        line
        for line in text.splitlines()
        if not re.match(r"^\s*#{1,6}\s+\S+\s*$", line)
    )


def _paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def _sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"[。！？!?；;]+", text)
    return [len(sentence.strip()) for sentence in sentences if sentence.strip()]


def _variation(values: list[int]) -> dict[str, float]:
    if not values:
        return {"average": 0, "stddev": 0, "cv": 0}
    average = statistics.mean(values)
    stddev = statistics.pstdev(values) if len(values) > 1 else 0
    return {
        "average": round(average, 2),
        "stddev": round(stddev, 2),
        "cv": round(stddev / average, 4) if average else 0,
    }


def _examples(text: str, pattern: str, limit: int = 3) -> list[str]:
    results: list[str] = []
    for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
        start = max(0, match.start() - 24)
        end = min(len(text), match.end() + 36)
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        if snippet not in results:
            results.append(snippet)
        if len(results) >= limit:
            break
    return results


def _repeated_ngrams(text: str, n: int = 8, limit: int = 10) -> list[dict[str, Any]]:
    normalized = re.sub(r"\s+", "", text)
    if len(normalized) < n * 2:
        return []
    counts = Counter(normalized[index : index + n] for index in range(len(normalized) - n + 1))
    return [
        {"text": value, "count": count}
        for value, count in counts.most_common()
        if count > 1
    ][:limit]


def _markdown_counts(text: str) -> dict[str, int]:
    lines = text.splitlines()
    return {
        "lists": sum(1 for line in lines if re.match(r"^\s*(?:[-*+] |\d+[.)] )", line)),
        "tables": sum(1 for line in lines if re.match(r"^\s*\|.*\|\s*$", line)),
        "blockquotes": sum(1 for line in lines if re.match(r"^\s*>\s?", line)),
        "code_blocks": sum(1 for line in lines if line.strip().startswith(chr(96) * 3)) // 2,
    }


def scan_text(text: str, path: str | None = None) -> dict[str, Any]:
    visible = _strip_frontmatter_and_fences(text)
    prose = _strip_heading_lines(visible)
    paragraphs = _paragraphs(prose)
    sentence_lengths = _sentence_lengths(prose)
    paragraph_lengths = [len(paragraph) for paragraph in paragraphs]
    headings = re.findall(r"(?m)^\s*#{1,6}\s+\S+", text)
    signals: list[dict[str, Any]] = []

    for signal_id, severity, pattern in SIGNAL_PATTERNS:
        count = len(re.findall(pattern, visible, re.IGNORECASE | re.DOTALL))
        if count:
            signals.append(
                {
                    "id": signal_id,
                    "severity": severity,
                    "count": count,
                    "examples": _examples(visible, pattern),
                }
            )

    paragraph_starts = [
        re.sub(r"^[#>*\-\d.\s]+", "", paragraph).strip()[:18]
        for paragraph in paragraphs
        if paragraph.strip()
    ]
    repeated_starts = [
        {"start": start, "count": count}
        for start, count in Counter(paragraph_starts).most_common()
        if start and count > 1
    ][:10]

    sentence_variation = _variation(sentence_lengths)
    paragraph_variation = _variation(paragraph_lengths)
    markdown_counts = _markdown_counts(text)
    first_person_mentions = len(re.findall(r"我", visible))
    first_person_paragraph_starts = sum(
        1 for paragraph in paragraphs if re.match(r"我", paragraph)
    )
    metrics: dict[str, Any] = {
        "characters": len(visible),
        "paragraphs": len(paragraphs),
        "headings": len(headings),
        "sentences": len(sentence_lengths),
        "average_sentence_length": sentence_variation["average"],
        "sentence_length_stddev": sentence_variation["stddev"],
        "sentence_length_cv": sentence_variation["cv"],
        "average_paragraph_length": paragraph_variation["average"],
        "paragraph_length_stddev": paragraph_variation["stddev"],
        "paragraph_length_cv": paragraph_variation["cv"],
        "numbers": len(re.findall(r"(?<!\w)\d+(?:\.\d+)?%?", visible)),
        "citation_markers": len(
            re.findall(r"https?://|doi\b|来源|引自|参考文献", visible, re.IGNORECASE)
        ),
        "first_person_mentions": first_person_mentions,
        "first_person_paragraph_starts": first_person_paragraph_starts,
        "repeated_paragraph_starts": repeated_starts,
        "repeated_ngrams": _repeated_ngrams(prose),
        **markdown_counts,
    }

    return {
        "path": path,
        "notice": "Signals are for human review only; this is not an authorship detector and has no AI score.",
        "signals": signals,
        "metrics": metrics,
        "review_limits": list(REVIEW_LIMITS),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# 中文文章信号扫描",
        "",
        f"> {result['notice']}",
        "",
        "## 指标",
        "",
        "| 指标 | 数值 |",
        "| --- | ---: |",
    ]
    for key, value in result["metrics"].items():
        if key in {"repeated_paragraph_starts", "repeated_ngrams"}:
            continue
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## 信号", ""])
    if not result["signals"]:
        lines.append("未发现配置中的信号。仍需人工阅读。")
    else:
        lines.extend(
            f"- {item['id']}（{item['severity']}，{item['count']} 次）："
            f"{'；'.join(item['examples'])}"
            for item in result["signals"]
        )

    repeated = result["metrics"]["repeated_paragraph_starts"]
    if repeated:
        lines.extend(["", "## 重复段首", ""])
        lines.extend(f"- {item['start']}：{item['count']} 次" for item in repeated)

    repeated_ngrams = result["metrics"]["repeated_ngrams"]
    if repeated_ngrams:
        lines.extend(["", "## 重复片段候选", ""])
        lines.extend(f"- {item['text']}：{item['count']} 次" for item in repeated_ngrams)

    lines.extend(["", "## 未由脚本核验", ""])
    lines.extend(f"- {item['id']}：{item['reason']}" for item in result["review_limits"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown article to scan")
    parser.add_argument(
        "--format", choices=("json", "markdown"), default="json", dest="output_format"
    )
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    result = scan_text(text, str(args.path))
    if args.output_format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
