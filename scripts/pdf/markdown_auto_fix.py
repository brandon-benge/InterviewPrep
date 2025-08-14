#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

def fix(text: str) -> str:
    out_lines = []
    for line in text.splitlines():
        m = re.fullmatch(r"\*\*(.+)\*\*", line.strip())
        if m:
            out_lines.append(f"#### _{m.group(1).strip()}_")
        else:
            out_lines.append(line)
    return "\n".join(out_lines) + "\n"

def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument('paths', nargs='+'); ap.add_argument('--check', action='store_true'); args = ap.parse_args(argv)
    changed = False
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(f"[warn] missing {p}", file=sys.stderr); continue
        orig = path.read_text(encoding='utf-8')
        new = fix(orig)
        if new != orig:
            if args.check:
                print(f"{p} would change"); changed = True
            else:
                path.write_text(new, encoding='utf-8'); print(f"fixed {p}")
    return 1 if args.check and changed else 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
