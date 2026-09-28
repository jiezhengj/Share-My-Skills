#!/usr/bin/env python3
"""
impact_check.py - Millisecond-speed cross-case dependency search across cases.
Part of adaptive-life-consulting skill.
Uses standard library only.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

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

def check_impact(record_id, root_dir=None):
    root = find_root(root_dir)
    cases_dir = root / "cases"
    
    clean_id = record_id.strip()
    # Normalize query (strip M:, E:, H:, X: prefix for broad matching if needed)
    raw_id = re.sub(r"^[MEHX]:", "", clean_id)
    
    pattern = re.compile(re.escape(raw_id), re.IGNORECASE)
    
    affected_cases = []
    
    if cases_dir.exists():
        for case_folder in sorted(cases_dir.iterdir()):
            if not case_folder.is_dir():
                continue
            
            case_id = case_folder.name
            # Check case.md and subfiles
            files_to_check = [
                case_folder / "case.md",
                case_folder / "conclusion.md",
                case_folder / "decision-log.md"
            ]
            
            matches = []
            for f in files_to_check:
                if f.exists():
                    try:
                        lines = f.read_text(encoding="utf-8").splitlines()
                        for line_no, line in enumerate(lines, 1):
                            if pattern.search(line):
                                matches.append({
                                    "file": str(f.name),
                                    "line_number": line_no,
                                    "content": line.strip()
                                })
                    except Exception:
                        pass
                        
            if matches:
                affected_cases.append({
                    "case_id": case_id,
                    "case_dir": str(case_folder),
                    "matches_count": len(matches),
                    "details": matches
                })
                
    return {
        "status": "ok",
        "query_record_id": record_id,
        "affected_cases_count": len(affected_cases),
        "affected_cases": affected_cases
    }

def main():
    parser = argparse.ArgumentParser(description="Cross-case dependency impact checker.")
    parser.add_argument("--record-id", type=str, required=True, help="Record ID or prefix (e.g. schedule-0042 or M:schedule-0042)")
    parser.add_argument("--root", type=str, default=None, help="Consulting root path")
    args = parser.parse_args()
    
    res = check_impact(args.record_id, args.root)
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
