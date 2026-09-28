#!/usr/bin/env python3
"""Dependency-free structural validation for the article-structure skill."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

    parser = argparse.ArgumentParser(description="验证 article-structure 技能的基础结构。")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"
    errors: list[str] = []
    if not skill_file.is_file():
        errors.append("缺少 SKILL.md。")
    else:
        text = skill_file.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
        if not frontmatter:
            errors.append("SKILL.md 缺少闭合的 YAML frontmatter。")
        else:
            header = frontmatter.group(1)
            if not re.search(r"^name:\s*article-structure\s*$", header, flags=re.MULTILINE):
                errors.append("frontmatter 的 name 必须是 article-structure。")
            if not re.search(r'^description:\s*".+"\s*$', header, flags=re.MULTILINE):
                errors.append("frontmatter 缺少非空 description。")

    required_scripts = ["verify_preservation.py", "verify_heading_structure.py"]
    parsed_scripts: list[str] = []
    for name in required_scripts:
        path = skill_dir / "scripts" / name
        if not path.is_file():
            errors.append(f"缺少必需脚本：scripts/{name}。")
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            parsed_scripts.append(name)
        except SyntaxError as error:
            errors.append(f"scripts/{name} 语法错误：{error.msg}（第 {error.lineno} 行）。")

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({"ok": True, "skill_dir": str(skill_dir), "parsed_scripts": parsed_scripts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
