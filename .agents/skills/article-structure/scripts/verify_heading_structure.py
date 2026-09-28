#!/usr/bin/env python3
"""Reject a document title being used as the sole body H1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")
TITLE_TAG = re.compile(r"^<title>.*</title>\s*$")
STRUCTURE_SUFFIX = re.compile(r"\s*[｜|]\s*结构梳理\s*$")


def normalized_title(value: str) -> str:
    return STRUCTURE_SUFFIX.sub("", value).strip()


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

    parser = argparse.ArgumentParser(description="校验正文 H1 从实际章节开始。")
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--document-title", required=True)
    args = parser.parse_args()

    headings: list[tuple[int, str, int]] = []
    for line_number, line in enumerate(args.markdown.read_text(encoding="utf-8").splitlines(), start=1):
        if TITLE_TAG.fullmatch(line):
            continue
        matched = HEADING.fullmatch(line)
        if matched:
            headings.append((len(matched.group(1)), matched.group(2), line_number))

    if not headings:
        raise SystemExit("错误：未找到正文标题，无法确认章节从 H1 开始。")

    first_level, first_text, first_line = headings[0]
    errors: list[str] = []
    if first_level != 1:
        errors.append(f"第一个正文章节位于第 {first_line} 行，却是 H{first_level}；必须是 H1。")

    expected_title = normalized_title(args.document_title)
    title_h1s = [
        line_number
        for level, text, line_number in headings
        if level == 1 and normalized_title(text) == expected_title
    ]
    if title_h1s:
        locations = "、".join(f"第 {line_number} 行" for line_number in title_h1s)
        errors.append(f"文档标题被写成正文 H1（{locations}）；请仅写入文档元数据。")

    if errors:
        print("错误：" + " ".join(errors), file=sys.stderr)
        raise SystemExit(2)

    print(json.dumps({"ok": True, "first_body_heading": first_text, "h1_count": sum(level == 1 for level, _, _ in headings)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
