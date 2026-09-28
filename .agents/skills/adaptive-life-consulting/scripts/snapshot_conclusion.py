#!/usr/bin/env python3
"""
snapshot_conclusion.py - Version conclusion.md into conclusions/vX.md and record decision log.
Part of adaptive-life-consulting skill.
Uses standard library only.
"""

import os
import sys
import json
import re
import shutil
import argparse
from datetime import datetime
from pathlib import Path

def snapshot_conclusion(case_path_or_id, reason, root_dir=None):
    p = Path(case_path_or_id)
    if not p.is_dir():
        # Treat as case_id in root/cases/
        root = Path(root_dir).resolve() if root_dir else Path.cwd().resolve()
        case_dir = root / "cases" / case_path_or_id
    else:
        case_dir = p.resolve()
        
    if not case_dir.exists():
        return {"status": "error", "message": f"Case directory not found: {case_dir}"}
        
    conclusion_file = case_dir / "conclusion.md"
    if not conclusion_file.exists():
        return {"status": "error", "message": f"conclusion.md not found in {case_dir}"}
        
    conclusions_dir = case_dir / "conclusions"
    conclusions_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine next version
    existing_versions = list(conclusions_dir.glob("*_v*.md"))
    v_nums = []
    for f in existing_versions:
        m = re.search(r"_v(\d+)\.md$", f.name)
        if m:
            v_nums.append(int(m.group(1)))
            
    next_v = max(v_nums, default=0) + 1
    today = datetime.now().strftime("%Y-%m-%d")
    archive_name = f"{today}_v{next_v}.md"
    archive_path = conclusions_dir / archive_name
    
    # Copy file
    shutil.copy2(conclusion_file, archive_path)
    
    # Update decision-log.md
    decision_log = case_dir / "decision-log.md"
    log_entry = f"| {today} | v{next_v} | revision | {reason} | Snapshot archived to conclusions/{archive_name} |\n"
    if decision_log.exists():
        content = decision_log.read_text(encoding="utf-8")
        decision_log.write_text(content.rstrip() + "\n" + log_entry, encoding="utf-8")
    else:
        header = "# Decision Log\n\n| Date | Version | Trigger | Decisive Evidence | Action Change |\n|---|---|---|---|---|\n"
        decision_log.write_text(header + log_entry, encoding="utf-8")
        
    return {
        "status": "ok",
        "version": f"v{next_v}",
        "snapshot_path": str(archive_path),
        "reason": reason
    }

def main():
    parser = argparse.ArgumentParser(description="Snapshot conclusion and append to decision log.")
    parser.add_argument("--case", type=str, required=True, help="Case directory path or case ID")
    parser.add_argument("--reason", type=str, required=True, help="Reason for revising/snapshotting conclusion")
    parser.add_argument("--root", type=str, default=None, help="Consulting root path")
    args = parser.parse_args()
    
    res = snapshot_conclusion(args.case, args.reason, args.root)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
