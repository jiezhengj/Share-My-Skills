#!/usr/bin/env python3
"""Validate the source-coverage contract for cn-natural-writing-editor."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = ("原最佳实践维度", "优先级", "Skill 执行位置", "参考文件", "脚本/测试", "必需输入")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _reference_names(cell: str) -> list[str]:
    return re.findall(r"`([^`]+\.md)`", cell)


def validate(skill_dir: Path) -> dict[str, Any]:
    matrix_path = skill_dir / "references" / "coverage-matrix.md"
    matrix_text = matrix_path.read_text(encoding="utf-8")
    lines = matrix_text.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if line.startswith("| 原最佳实践维度 |")),
        None,
    )
    errors: list[str] = []
    rows: list[dict[str, str]] = []

    if header_index is None or header_index + 1 >= len(lines):
        errors.append("coverage-matrix.md lacks the required coverage table")
    else:
        headers = _cells(lines[header_index])
        if tuple(headers) != REQUIRED_COLUMNS:
            errors.append(f"coverage table headers differ: {headers}")
        for line in lines[header_index + 2 :]:
            if not line.startswith("|"):
                break
            cells = _cells(line)
            if len(cells) != len(REQUIRED_COLUMNS):
                errors.append(f"coverage row has {len(cells)} columns: {line}")
                continue
            row = dict(zip(REQUIRED_COLUMNS, cells))
            rows.append(row)
            for reference in _reference_names(row["参考文件"]):
                if not (skill_dir / "references" / reference).exists():
                    errors.append(f"missing reference: {reference}")
            if row["优先级"] == "高":
                if (
                    not row["Skill 执行位置"]
                    or not row["参考文件"]
                    or not row["脚本/测试"]
                ):
                    errors.append(f"high-priority row lacks execution detail: {row['原最佳实践维度']}")

    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if "references/coverage-matrix.md" not in skill_text:
        errors.append("SKILL.md does not require coverage-matrix.md")
    if "是否需要脱敏" in skill_text:
        errors.append("SKILL.md still asks about anonymization by default")
    if "optional-privacy-module.md" not in skill_text:
        errors.append("SKILL.md does not route the optional privacy module")
    if (skill_dir / "references" / "author-voice-and-privacy.md").exists():
        errors.append("stale combined author/privacy reference remains")

    return {
        "status": "PASS" if not errors else "FAIL",
        "rows": len(rows),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args()
    result = validate(args.skill_dir)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"coverage: {result['status']} ({result['rows']} rows)")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
