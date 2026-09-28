#!/usr/bin/env python3
"""Dependency-free structural validation for the article-editor skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_REFERENCES = (
    "article-genre-rubric.md",
    "author-style.md",
    "narrative-quality-rubric.md",
    "interview-question-bank.md",
    "reader-validation-rubric.md",
    "human-narrative-shape.md",
    "human-narrative-samples.md",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args()
    skill_dir = args.skill_dir.resolve()
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        errors.append("缺少 SKILL.md。")
    else:
        text = skill_file.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
        if not frontmatter:
            errors.append("SKILL.md 缺少闭合的 YAML frontmatter。")
        else:
            header = frontmatter.group(1)
            if not re.search(r"^name:\s*article-editor\s*$", header, flags=re.MULTILINE):
                errors.append("frontmatter 的 name 必须是 article-editor。")
            if not re.search(r'^description:\s*".+"\s*$', header, flags=re.MULTILINE):
                errors.append("frontmatter 缺少非空 description。")
        if "../" + "cn-natural-writing-editor/" in text:
            errors.append("SKILL.md 仍引用未声明的跨技能路径。")

    for name in REQUIRED_REFERENCES:
        if not (skill_dir / "references" / name).is_file():
            errors.append(f"缺少必需参考文件：references/{name}。")

    for path in (skill_dir / "scripts").glob("*.py"):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as error:
            errors.append(f"{path.name} 语法错误：{error.msg}（第 {error.lineno} 行）。")

    result = {"ok": not errors, "skill_dir": str(skill_dir), "errors": errors}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
