#!/usr/bin/env python3
"""Verify a Markdown structure edit preserves source text and its original order."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^#{1,6}[ \t]+.+$")
HEADING_PREFIX = re.compile(r"^#{1,6}[ \t]+")
LIST_PREFIX = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]+")
TABLE_DIVIDER = re.compile(r"^[ \t]*\|?[ \t:|-]+\|?[ \t]*$")
TITLE_H1 = re.compile(r"^#\s+(.+?)\s*$")
TITLE_TAG = re.compile(r"^<title>(.+)</title>\s*$")
STRUCTURE_SUFFIX = re.compile(r"\s*[｜|]\s*结构梳理\s*$")


def split_frontmatter(text: str) -> tuple[str, str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        return "", text
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("检测到未闭合的 YAML frontmatter。")
    end = closing + len("\n---\n")
    return text[:end], text[end:]


def normalized_title(value: str) -> str:
    return STRUCTURE_SUFFIX.sub("", value).strip()


def strip_document_title_metadata(body: str, document_title: str) -> tuple[str, bool]:
    """Remove a source/revised document-title line from the body comparison."""
    expected = normalized_title(document_title)
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        h1 = TITLE_H1.fullmatch(line.strip())
        title_tag = TITLE_TAG.fullmatch(line.strip())
        candidate = h1.group(1) if h1 else title_tag.group(1) if title_tag else None
        if candidate is None or normalized_title(candidate) != expected:
            return body, False
        return "\n".join(lines[:index] + lines[index + 1 :]), True
    return body, False


def load_generated_lines(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    lines = payload.get("generated_lines") if isinstance(payload, dict) else payload
    if not isinstance(lines, list) or not all(isinstance(item, str) and "\n" not in item for item in lines):
        raise ValueError("新增结构行清单必须是单行字符串数组，或包含 generated_lines 数组的对象。")
    return lines


def remove_generated_lines(body: str, lines: list[str], source_body: str) -> str:
    source_counts = collections.Counter(source_body.splitlines())
    generated_counts = collections.Counter(lines)
    output: list[str] = []
    for line in body.splitlines():
        if generated_counts[line] > 0 and source_counts[line] == 0:
            generated_counts[line] -= 1
            continue
        if source_counts[line] > 0:
            source_counts[line] -= 1
        output.append(line)
    missing = list(generated_counts.elements())
    if missing:
        raise ValueError("修订稿中未找到清单所列的新增结构行：" + "、".join(missing))
    return "\n".join(output)


def canonical_body(body: str) -> str:
    output: list[str] = []
    in_code_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            output.append(line)
            continue
        if in_code_fence:
            output.append(line)
            continue
        if HEADING.fullmatch(line):
            line = HEADING_PREFIX.sub("", line)
        line = LIST_PREFIX.sub("", line)
        if TABLE_DIVIDER.fullmatch(line):
            continue
        # Permitted formatting: bold delimiters and Markdown table cell separators.
        line = line.replace("**", "").replace("|", "")
        output.append(line)
    return re.sub(r"\s+", "", "\n".join(output))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

    parser = argparse.ArgumentParser(description="校验 Markdown 结构整理是否保留原文文字和顺序。")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--revised", type=Path, required=True)
    parser.add_argument("--generated-lines", type=Path, required=True)
    parser.add_argument("--document-title", help="来源开头等同文档标题的 H1，按元数据从正文比较中剥离")
    args = parser.parse_args()
    try:
        source_frontmatter, source_body = split_frontmatter(args.source.read_text(encoding="utf-8"))
        revised_frontmatter, revised_body = split_frontmatter(args.revised.read_text(encoding="utf-8"))
        if source_frontmatter != revised_frontmatter:
            raise ValueError("YAML frontmatter 已被修改。")
        if args.document_title:
            source_body, source_had_title = strip_document_title_metadata(source_body, args.document_title)
            revised_body, revised_had_title = strip_document_title_metadata(revised_body, args.document_title)
            if source_had_title and not revised_had_title:
                raise ValueError("修订稿缺少来源中的文档标题元数据。")
        generated_lines = load_generated_lines(args.generated_lines)
        revised_without_generated = remove_generated_lines(revised_body, generated_lines, source_body)
        source_text = canonical_body(source_body)
        revised_text = canonical_body(revised_without_generated)
        if source_text != revised_text:
            raise ValueError("正文文字或出现顺序发生变化。")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"错误：{error}", file=sys.stderr)
        raise SystemExit(2) from error
    print(json.dumps({"ok": True, "body_sha256": digest(source_text), "generated_line_count": len(generated_lines)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
