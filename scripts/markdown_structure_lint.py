#!/usr/bin/env python3
import sys, re, pathlib

ALLOWED_PREFIXES = ('#', '-', '*', '|', '>', '`')  # structural markers
ROOT = pathlib.Path('.').resolve()
md_files = [p for p in ROOT.rglob('*.md') if '.venv' not in p.parts]

violations = {}
for path in md_files:
    lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    saw_section = False
    in_code = False
    prev_was_blockquote = False
    for i, raw in enumerate(lines, start=1):
        stripped = raw.lstrip()
        if stripped.startswith('```'):
            in_code = not in_code
            prev_was_blockquote = False
            continue
        if in_code or not stripped:
            if not stripped:
                prev_was_blockquote = False
            continue
        if stripped.startswith('## '):
            saw_section = True
        if not saw_section:
            continue
        # Check blockquote -> list spacing
        if (stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.\s', stripped)) and prev_was_blockquote:
            violations.setdefault(path, []).append((i, raw, 'List immediately after blockquote; add blank line'))
        if stripped.startswith('**'):
            violations.setdefault(path, []).append((i, raw, 'Starts with bold; convert to heading'))
            continue
        if re.match(r'^!\[[^\]]*\]\([^)]*\)$', stripped):  # image line
            prev_was_blockquote = False
            continue
        if re.match(r'^\d+\.\s', stripped):  # ordered list
            prev_was_blockquote = False
            continue
        if stripped.startswith(ALLOWED_PREFIXES):  # allowed structure
            prev_was_blockquote = stripped.startswith('>')
            continue
        # paragraphs allowed
        prev_was_blockquote = False
        continue

if not violations:
    print('No structural issues found.')
    sys.exit(0)

print('Structural issues detected (bold-leading lines):')
for p, items in violations.items():
    print(f'\n{p}:')
    for ln, content, reason in items:
        print(f'  L{ln}: {content}  <-- {reason}')
sys.exit(1)
