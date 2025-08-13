#!/usr/bin/env python3
"""Wrap all level-4 markdown headings (####) text in italics if not already.

Rules:
 - Match lines starting with exactly '#### ' (no more, no less) followed by heading text.
 - If after the space the next non-space char is '*' or '_' (already italic/bold/combined), skip.
 - Preserve trailing colon, punctuation, emojis, and existing inline formatting inside the italics.
 - Avoid double-wrapping if already *...* spanning whole line content (after hashes).
"""
from __future__ import annotations
import pathlib, re

ROOT = pathlib.Path('.').resolve()
md_files = [p for p in ROOT.rglob('*.md') if '.venv' not in p.parts]

H4_RE = re.compile(r'^(#### )(.*?)(\s*)$')

def transform(line: str) -> str:
    m = H4_RE.match(line)
    if not m:
        return line
    prefix, text, ws = m.groups()
    stripped = text.strip()
    # Skip if already fully italicized (starts and ends with * and no unmatched)
    if (stripped.startswith('*') and stripped.endswith('*')) or (stripped.startswith('_') and stripped.endswith('_')):
        return line
    # Skip if first non-space char indicates existing emphasis or code block fences inside
    if stripped.startswith(('*', '_')):
        return line
    return f"{prefix}*{text.strip()}*{ws}"

changed = 0
for path in md_files:
    original = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    new_lines = []
    file_changed = False
    for ln in original:
        nl = transform(ln)
        if nl != ln:
            file_changed = True
            changed += 1
        new_lines.append(nl)
    if file_changed:
        path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
        print(f'Updated H4 headings in {path}')

print(f'Total H4 headings updated: {changed}')
