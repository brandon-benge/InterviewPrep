#!/usr/bin/env python3
"""Convert bold-leading pseudo headings to real H4 headings and normalize unicode rules."""
from __future__ import annotations
import pathlib

ROOT = pathlib.Path('.').resolve()

def process(path: pathlib.Path) -> int:
	lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
	out = []
	changed = 0
	saw_section = False
	in_code = False
	for line in lines:
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
		if stripped == '⸻':
			out.append('---')
			changed += 1
			continue
		if stripped.startswith('**'):
			core = stripped.strip('*').rstrip(':')
			out.append(f'#### {core}')
			changed += 1
			continue
		out.append(line)
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
