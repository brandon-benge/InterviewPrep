#!/usr/bin/env python3
import sys, re, pathlib

ALLOWED_PREFIXES = ('#', '-', '*', '|', '>', '`')  # headers, bullets, tables, blockquotes, code fences

ROOT = pathlib.Path('.').resolve()
md_files = [p for p in ROOT.rglob('*.md') if '.venv' not in p.parts and 'README.md' not in str(p)]

problem_files = {}
for path in md_files:
    text = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    saw_section = False
    in_code_fence = False
    for idx, line in enumerate(text, start=1):
        stripped = line.lstrip()

        # Detect code fence start/end (``` or ```lang)
        if stripped.startswith('```'):
            # toggle fence state then allow line (fence marker itself is allowed)
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            # ignore everything inside code blocks
            continue

        if not stripped:  # skip blank lines
            continue
        # mark when we pass first secondary heading (## ) which indicates structured region begins
        if stripped.startswith('## '):
            saw_section = True
        if not saw_section:
            continue  # allow free-form intro paragraph before first section
        if stripped.startswith(ALLOWED_PREFIXES):
            continue
        # treat HTML comments as allowed
        if stripped.startswith('<!--'):
            continue
        # treat ordered list lines (e.g., 1. Something)
        if re.match(r'^\d+\.\s', stripped):
            continue
        # likely offending structural line
        problem_files.setdefault(path, []).append((idx, line))

if not problem_files:
    print('No structural issues found.')
    sys.exit(0)

print('Structural issues detected:')
for p, issues in problem_files.items():
    print(f'\n{p}:')
    for ln, content in issues:
        print(f'  L{ln}: {content}')

sys.exit(1)
