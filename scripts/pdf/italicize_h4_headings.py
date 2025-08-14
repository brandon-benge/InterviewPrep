#!/usr/bin/env python3
from __future__ import annotations
import sys, re
from pathlib import Path

def process(text: str) -> str:
    def repl(m):
        content = m.group(1).strip()
        if content.startswith('_') and content.endswith('_'): return m.group(0)
        return f"#### _{content}_"
    return re.sub(r'^####\s+(.+)$', repl, text, flags=re.MULTILINE)

def main(argv):
    for fname in argv:
        p = Path(fname)
        if not p.exists():
            print(f"missing {fname}", file=sys.stderr); continue
        new = process(p.read_text(encoding='utf-8'))
        p.write_text(new, encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
