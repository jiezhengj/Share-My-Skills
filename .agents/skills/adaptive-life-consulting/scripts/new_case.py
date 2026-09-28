#!/usr/bin/env python3
"""
new_case.py - Proactively scaffold a new case directory with standard 22-section case.md.
Part of adaptive-life-consulting skill.
Uses standard library only.
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

def sanitize_topic(topic_str):
    s = topic_str.strip().lower()
    s = re.sub(r"[^a-z0-9\-_\u4e00-\u9fa5]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed-topic"

def find_root(start_dir=None):
    cur = Path(start_dir).resolve() if start_dir else Path.cwd().resolve()
    while True:
        if (cur / ".adaptive-life-consulting.yaml").exists():
            return cur
        if (cur / "index.md").exists() and (cur / "cases").is_dir():
            return cur
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return Path.cwd().resolve()

def scaffold_case(topic, problem_form="undefined", parent_case=None, root_dir=None):
    root = find_root(root_dir)
    today = datetime.now().strftime("%Y-%m-%d")
    topic_clean = sanitize_topic(topic)
    case_id = f"{today}_{topic_clean}"
    
    # Handle duplicates by adding suffix
    case_dir = root / "cases" / case_id
    counter = 2
    while case_dir.exists():
        case_id = f"{today}_{topic_clean}-{counter}"
        case_dir = root / "cases" / case_id
        counter += 1
        
    # Create case subdirectories
    for d in ["conclusions", "archive"]:
        (case_dir / d).mkdir(parents=True, exist_ok=True)
        
    # Standard 22-section case.md
    case_md_content = f"""# Case State

## Case Metadata
- Case ID: {case_id}
- Created: {today}
- Last Updated: {today}
- Status: active
- Primary Language: zh-CN
- Parent Case: {parent_case or "null"}
- Related Cases: []
- Reopened From: null
- Reopen Reason: null

## Current Problem
{topic}

## Problem Form
- {problem_form}

## Current Success Criteria
[To be defined during initial reasoning]

## Time Horizon
- Short-term:
- Long-term:
- Primary decision horizon:

## Stakeholders
- Primary User

## Current Best Action
[Pending evidence accumulation]

## Hard Constraints
[]

## Soft Preferences
[]

## Confirmed Facts
[]

## Subjective Experiences
[]

## Goals / Values
[]

## Behavioral Evidence
[]

## External Reality
[]

## Working Hypotheses
[]

## Downgraded / Rejected Hypotheses
[]

## Critical Unknowns
[]

## Non-Introspectable Unknowns
[]

## Experiments Pending
[]

## Evidence Gaps
[]

## Decisive Dependencies
[]

## Confidence Levels
- Problem-understanding confidence: initial
- Option-fit confidence: uncalibrated
- External-feasibility confidence: uncalibrated
- Immediate-action confidence: initial

## Next Information-Gathering Action
[Formulate single most decision-sensitive question]

## Last Checkpoint
- Date: {today}
- Trigger: initial_scaffolding
"""
    (case_dir / "case.md").write_text(case_md_content, encoding="utf-8")
    
    # Supporting files
    (case_dir / "evidence.md").write_text(f"# Evidence Log: {case_id}\n\n## Log\n", encoding="utf-8")
    (case_dir / "experiments.md").write_text(f"# Real-World Experiments: {case_id}\n\n## Active Experiments\n", encoding="utf-8")
    (case_dir / "decision-log.md").write_text(f"# Decision Log: {case_id}\n\n| Date | Version | Trigger | Decisive Evidence | Action Change |\n|---|---|---|---|---|\n| {today} | v0 | initial | Case scaffolded | Initial inquiry |\n", encoding="utf-8")
    (case_dir / "conclusion.md").write_text(f"# Current Working Conclusion: {case_id}\n\nStatus: active inquiry pending.\n", encoding="utf-8")
    
    # Update index.md
    index_file = root / "index.md"
    if index_file.exists():
        row = f"| {case_id} | active | {today} | {topic} | Initial inquiry active |\n"
        idx_text = index_file.read_text(encoding="utf-8")
        if case_id not in idx_text:
            index_file.write_text(idx_text.strip() + "\n" + row, encoding="utf-8")
            
    return {
        "status": "ok",
        "case_id": case_id,
        "case_dir": str(case_dir),
        "case_md": str(case_dir / "case.md"),
        "root": str(root)
    }

def main():
    parser = argparse.ArgumentParser(description="Proactively scaffold a new case.")
    parser.add_argument("--topic", type=str, required=True, help="Topic description or slug")
    parser.add_argument("--form", type=str, default="undefined", help="Problem form (choice, open-search, diagnosis, etc.)")
    parser.add_argument("--parent", type=str, default=None, help="Parent case ID if splitting")
    parser.add_argument("--root", type=str, default=None, help="Target root directory")
    args = parser.parse_args()
    
    res = scaffold_case(args.topic, args.form, args.parent, args.root)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
