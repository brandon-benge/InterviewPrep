#!/usr/bin/env python3
"""(moved to scripts/pdf/) Convert Markdown files to PDF via pandoc."""
from __future__ import annotations
import argparse, subprocess, sys, shutil
from pathlib import Path

def convert(md: Path, out_dir: Path, force: bool):
    pdf = out_dir / (md.stem + '.pdf')
    if pdf.exists() and not force: return
    cmd = [
        'pandoc', str(md), '-o', str(pdf), '--from=markdown', '--pdf-engine=xelatex',
        '--highlight-style=monochrome'
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"built {pdf}")
    except subprocess.CalledProcessError as e:
        print(f"[error] pandoc failed for {md}: {e}", file=sys.stderr)

def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--glob', default='*.md')
    ap.add_argument('--out', default='.')
    args = ap.parse_args(argv)
    if not shutil.which('pandoc'):
        print('[error] pandoc not found', file=sys.stderr); return 1
    root = Path(args.root); out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for md in root.rglob(args.glob):
        if md.name.startswith('.') or md.suffix.lower() != '.md': continue
        convert(md, out_dir, args.force); count += 1
    print(f"processed {count} markdown files")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
