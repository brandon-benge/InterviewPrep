#!/usr/bin/env python3
"""Convert bold-leading pseudo headings to real H4 headings, normalize unicode rules,
enforce blank line after blockquote before list, and fill empty H4 headings."""
from __future__ import annotations
import pathlib

ROOT = pathlib.Path('.').resolve()

def process(path: pathlib.Path) -> int:
	lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
	out = []
	changed = 0
	saw_section = False
	in_code = False
	prev_was_blockquote = False
	for line in lines:
		stripped = line.lstrip()
		if stripped.startswith('```'):
			in_code = not in_code
			out.append(line)
			prev_was_blockquote = False
			continue
		if in_code:
			out.append(line)
			continue
		if stripped.startswith('## '):
			saw_section = True
		if not saw_section:
			out.append(line)
			continue
		if stripped == '⸻':
			out.append('---')
			changed += 1
			prev_was_blockquote = False
			continue
		if stripped.startswith('**'):
			core = stripped.strip('*').rstrip(':')
			out.append(f'#### {core}')
			changed += 1
			prev_was_blockquote = False
			continue
		# Empty H4 headings -> placeholder
		if stripped.startswith('####') and stripped.strip() == '####':
			out.append('#### *Placeholder Heading (Fill Me)*')
			changed += 1
			prev_was_blockquote = False
			continue
		# Enforce blank line after blockquote before list bullet / ordered list
		if prev_was_blockquote and (stripped.startswith('- ') or stripped.startswith('* ') or stripped[:2].isdigit()):
			if out and out[-1].strip().startswith('>'):
				out.append('')
				changed += 1
			out.append(line)
			prev_was_blockquote = False
			continue
		out.append(line)
		prev_was_blockquote = stripped.startswith('>')
	if changed:
		path.write_text('\n'.join(out) + '\n', encoding='utf-8')
	return changed

def main():
	total = 0
	for p in ROOT.rglob('*.md'):
		if '.venv' in p.parts:
			continue
		total += process(p)
	print('Total transformed bold pseudo-headings:', total)

if __name__ == '__main__':
	main()
