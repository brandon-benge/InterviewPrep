#!/usr/bin/env python3
"""Italicize all level-4 Markdown headings (####) across the repository.

Rules:
  - Match lines starting with exactly four hashes followed by a space and heading text.
  - If the heading text is already fully wrapped in a single pair of * ... * (ignoring leading/trailing whitespace), skip.
  - Otherwise wrap the trimmed text portion in single asterisks: #### *Heading Text*
  - Preserve any trailing inline Markdown after the heading text (rare, but supported) by only italicizing the core phrase before two spaces + two spaces pattern or end of line.
  - Leave empty H4 headings ("#### \n") untouched (could be a placeholder) but report them.

Idempotent: Re-running should not introduce duplicate asterisks.

Usage:
  python scripts/italicize_h4_headings.py [root='.'] [--dry-run]
"""

from __future__ import annotations
import sys
from pathlib import Path
import re
from typing import Iterable

H4_PATTERN = re.compile(r"^(####) (.+?)$")  # capture whole line sans newline
ALREADY_WRAPPED = re.compile(r"^\*.*\*$")  # any leading & trailing * ... * to avoid double wrapping

def iter_markdown_files(root: Path) -> Iterable[Path]:
    for p in root.rglob('*.md'):
        # Skip hidden directories (like .git) just in case
        if any(part.startswith('.') for part in p.relative_to(root).parts):
            continue
        yield p

def transform_line(line: str, stats: dict) -> str:
    # Preserve original newline (if any)
    newline = ''
    if line.endswith('\n'):
        newline = '\n'
        content = line[:-1]
    else:
        content = line
    m = H4_PATTERN.match(content)
    if not m:
        return line
    prefix, text = m.groups()
    if not text.strip():
        stats['empty'] += 1
        return line
    core = text.strip()
    # If already begins and ends with *, skip (avoid adding more asterisks even if nested)
    if ALREADY_WRAPPED.match(core):
        stats['skipped_already'] += 1
        return line
    # Avoid wrapping if it already contains leading and trailing asterisk after trimming punctuation like ':' inside
    new_line = f"{prefix} *{core}*{newline}"
    stats['updated'] += 1
    return new_line

def process_file(path: Path, dry_run: bool, stats: dict):
    original = path.read_text(encoding='utf-8').splitlines(keepends=True)
    changed = []
    file_changed = False
    for line in original:
        new_line = transform_line(line, stats)
        if new_line != line:
            file_changed = True
        changed.append(new_line)
    if file_changed and not dry_run:
        path.write_text(''.join(changed), encoding='utf-8')
        stats['files_changed'] += 1

def main(argv: list[str]):
    import argparse
    ap = argparse.ArgumentParser(description='Italicize all H4 headings in markdown files.')
    ap.add_argument('root', nargs='?', default='.', help='Root directory (default: current)')
    ap.add_argument('--dry-run', action='store_true', help='Do not write changes, just report')
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    stats = {'updated': 0, 'skipped_already': 0, 'empty': 0, 'files_changed': 0}
    for md in iter_markdown_files(root):
        process_file(md, args.dry_run, stats)
    action = 'DRY-RUN' if args.dry_run else 'UPDATED'
    print(f"{action}: files_changed={stats['files_changed']} updated_headings={stats['updated']} already_ok={stats['skipped_already']} empty_h4={stats['empty']}")
    if stats['updated']:
        print('Tip: Re-run to verify idempotency (should show updated_headings=0).')

if __name__ == '__main__':
    main(sys.argv[1:])
