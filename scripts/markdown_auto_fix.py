#!/usr/bin/env python3
"""Auto-fix structural markdown issues to satisfy markdown_structure_lint.py rules.

Rules:
 - After the first secondary heading (## ), every non-blank, non-code-fence line must start with
   one of allowed prefixes (# - * | > `), an ordered list (\d+. ), or be an HTML comment.
Strategy:
 - Convert unicode horizontal rule '⸻' to '---'
 - For any offending line, prefix with '> ' (blockquote) unless already acceptable.
 - Skip inside code fences.
"""
from __future__ import annotations
import pathlib, re, sys

ALLOWED_PREFIXES = ('#', '-', '*', '|', '>', '`')

def needs_fix(line: str) -> bool:
    s = line.lstrip()
    if not s:
        return False
    if s.startswith(ALLOWED_PREFIXES):
        return False
    if s.startswith('<!--'):
        return False
    if re.match(r'^\d+\.\s', s):
        return False
    return True

def process(path: pathlib.Path) -> int:
    text = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    changed = 0
    out = []
    saw_section = False
    in_code = False
    for line in text:
        stripped = line.lstrip()
        if stripped.startswith('```'):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if stripped.startswith('## '):
            saw_section = True
        if not saw_section:
            out.append(line)
            continue
        # transform unicode separators
        if stripped == '⸻':
            out.append('---')
            changed += 1
            continue
        if needs_fix(line):
            out.append('> ' + stripped)
            changed += 1
        else:
            out.append(line)
    if changed:
        path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    return changed

def main():
    ROOT = pathlib.Path('.').resolve()
    md_files = [p for p in ROOT.rglob('*.md') if '.venv' not in p.parts and 'README.md' not in str(p)]
    total = 0
    for p in md_files:
        c = process(p)
        if c:
            print(f'Fixed {c:3} lines in {p}')
            total += c
    if total == 0:
        print('No fixes applied; all markdown already conforms.')
    else:
        print(f'Total fixed lines: {total}')

if __name__ == '__main__':
    main()
