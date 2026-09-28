#!/usr/bin/env python3
"""
init_workspace.py - Discover or initialize the consulting root workspace.
Part of adaptive-life-consulting skill.
Uses standard library only.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

def find_consulting_root(start_dir=None):
    if start_dir:
        cur = Path(start_dir).resolve()
    else:
        cur = Path.cwd().resolve()
    
    check_dir = cur
    while True:
        marker = check_dir / ".adaptive-life-consulting.yaml"
        if marker.exists():
            return check_dir, True
        
        if (check_dir / "index.md").exists() and (check_dir / "cases").is_dir() and (check_dir / "memory").is_dir():
            return check_dir, True
        
        parent = check_dir.parent
        if parent == check_dir:
            break
        check_dir = parent
        
    return cur, False

def init_workspace(target_root, workspace_type="dedicated"):
    target_path = Path(target_root).resolve()
    created = []
    
    for d in ["cases", "memory", "memory/archive"]:
        p = target_path / d
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created.append(str(p))
            
    marker = target_path / ".adaptive-life-consulting.yaml"
    if not marker.exists():
        marker_content = f"""schema_version: 1
protocol_version: 5
workspace_type: {workspace_type}
skill_name: adaptive-life-consulting
created_at: '{datetime.now().strftime("%Y-%m-%d")}'
"""
        marker.write_text(marker_content, encoding="utf-8")
        created.append(str(marker))
        
    idx = target_path / "index.md"
    if not idx.exists():
        idx_content = """# Case Index

| Case ID | Status | Updated | Topic | Current State |
|---|---|---|---|---|
"""
        idx.write_text(idx_content, encoding="utf-8")
        created.append(str(idx))
        
    conflict = target_path / "memory" / "conflict-log.md"
    if not conflict.exists():
        conflict_content = """# Memory Conflict Log

Record of cross-case memory disputes, invalidations, and retractions.
"""
        conflict.write_text(conflict_content, encoding="utf-8")
        created.append(str(conflict))
        
    canonical = target_path / "memory" / "canonical.yaml"
    if not canonical.exists():
        canonical.write_text("# Canonical Cross-Case Memory Records\nrecords: []\n", encoding="utf-8")
        created.append(str(canonical))
        
    return target_path, created

def main():
    parser = argparse.ArgumentParser(description="Discover or initialize consulting root workspace.")
    parser.add_argument("--root", type=str, default=None, help="Target root directory path")
    parser.add_argument("--type", type=str, default="dedicated", choices=["dedicated", "shared"], help="Workspace type")
    args = parser.parse_args()
    
    found_root, exists = find_consulting_root(args.root)
    
    if exists and not args.root:
        res = {
            "status": "ok",
            "action": "discovered",
            "root": str(found_root),
            "created_files": []
        }
    else:
        root_to_use = Path(args.root).resolve() if args.root else found_root
        target_path, created = init_workspace(root_to_use, args.type)
        res = {
            "status": "ok",
            "action": "initialized" if created else "already_initialized",
            "root": str(target_path),
            "created_files": created
        }
        
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
