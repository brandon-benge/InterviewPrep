#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys, json
from pathlib import Path

def lint(text: str) -> list[dict]:
    issues = []
    for i,line in enumerate(text.splitlines(),1):
        if line.startswith('#### ') and '__' in line:
            issues.append({"line": i, "rule": "h4_italics", "msg": "H4 contains bold markup"})
    return issues

def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument('paths', nargs='+'); ap.add_argument('--json', action='store_true'); args = ap.parse_args(argv)
    all_issues = []
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(f"[warn] missing {p}", file=sys.stderr); continue
        issues = lint(path.read_text(encoding='utf-8'))
        for iss in issues: iss['file'] = p
        all_issues.extend(issues)
    if args.json:
        print(json.dumps(all_issues, indent=2))
    else:
        for iss in all_issues:
            print(f"{iss['file']}:{iss['line']} {iss['rule']} {iss['msg']}")
    return 0 if not all_issues else 1

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
