#!/usr/bin/env python3
"""
validate_memory.py - Validate, inspect, or append to canonical cross-case memory.
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

ALLOWED_TYPES = {"fact", "experience", "goal", "preference", "behavior", "hypothesis"}
ALLOWED_STATUSES = {"active", "superseded", "retracted", "disputed", "expired", "restricted"}

def find_root(start_dir=None):
    cur = Path(start_dir).resolve() if start_dir else Path.cwd().resolve()
    while True:
        if (cur / ".adaptive-life-consulting.yaml").exists():
            return cur
        if (cur / "index.md").exists() and (cur / "memory").is_dir():
            return cur
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return Path.cwd().resolve()

def parse_simple_yaml_records(filepath):
    if not filepath.exists():
        return []
    
    text = filepath.read_text(encoding="utf-8")
    # Simple standard parser for canonical yaml blocks
    raw_blocks = text.split("- id:")
    records = []
    for b in raw_blocks:
        if not b.strip() or b.startswith("#"):
            continue
        full_block = "- id:" + b if not b.startswith("- id:") else b
        # Extract fields
        rec = {}
        for line in full_block.splitlines():
            line_str = line.strip()
            if ":" in line_str and not line_str.startswith("#"):
                k, v = line_str.split(":", 1)
                k = k.strip().lstrip("-").strip()
                v = v.strip().strip("'").strip('"')
                if k:
                    rec[k] = v
        if "id" in rec:
            records.append(rec)
    return records

def validate_entry(entry_dict):
    errors = []
    if "id" not in entry_dict or not entry_dict["id"]:
        errors.append("Missing required field: id")
    if "type" not in entry_dict or entry_dict["type"] not in ALLOWED_TYPES:
        errors.append(f"Invalid or missing type. Must be one of: {sorted(ALLOWED_TYPES)}")
    if "status" in entry_dict and entry_dict["status"] not in ALLOWED_STATUSES:
        errors.append(f"Invalid status. Must be one of: {sorted(ALLOWED_STATUSES)}")
    if "value" not in entry_dict or not entry_dict["value"]:
        errors.append("Missing required field: value")
    return errors

def add_record(entry_dict, root_dir=None):
    root = find_root(root_dir)
    canonical_file = root / "memory" / "canonical.yaml"
    canonical_file.parent.mkdir(parents=True, exist_ok=True)
    
    errors = validate_entry(entry_dict)
    if errors:
        return {"status": "error", "errors": errors}
        
    today = datetime.now().strftime("%Y-%m-%d")
    record_id = entry_dict["id"]
    rec_type = entry_dict["type"]
    val = entry_dict["value"]
    source_case = entry_dict.get("source_case", "manual")
    confidence = entry_dict.get("confidence", "high")
    scope = entry_dict.get("scope", "general")
    status = entry_dict.get("status", "active")
    
    yaml_block = f"""
- id: {record_id}
  type: {rec_type}
  value: "{val}"
  source_cases:
    - {source_case}
  observed_at: {today}
  valid_from: {today}
  valid_to: null
  confidence: {confidence}
  scope:
    - {scope}
  stability: contextual
  status: {status}
  supersedes: []
  conflicts_with: []
"""
    if not canonical_file.exists():
        canonical_file.write_text("# Canonical Cross-Case Memory Records\n" + yaml_block, encoding="utf-8")
    else:
        existing = canonical_file.read_text(encoding="utf-8")
        canonical_file.write_text(existing.rstrip() + "\n" + yaml_block, encoding="utf-8")
        
    return {"status": "ok", "action": "added", "record_id": record_id, "file": str(canonical_file)}

def main():
    parser = argparse.ArgumentParser(description="Canonical memory validator and manager.")
    parser.add_argument("--action", choices=["validate", "add", "list"], default="list")
    parser.add_argument("--entry-json", type=str, default=None, help="JSON string of record to add")
    parser.add_argument("--root", type=str, default=None, help="Consulting root path")
    args = parser.parse_args()
    
    root = find_root(args.root)
    canonical_file = root / "memory" / "canonical.yaml"
    
    if args.action == "list":
        records = parse_simple_yaml_records(canonical_file)
        print(json.dumps({"status": "ok", "total_records": len(records), "records": records}, ensure_ascii=False, indent=2))
    elif args.action == "add":
        if not args.entry_json:
            print(json.dumps({"status": "error", "message": "Missing --entry-json"}, ensure_ascii=False))
            sys.exit(1)
        data = json.loads(args.entry_json)
        res = add_record(data, args.root)
        print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
