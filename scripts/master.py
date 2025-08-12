#!/usr/bin/env python3
"""Master utility script for quiz workflow.

Subcommands:
  prepare  -> generate quiz.json + answer_key.json + quiz.txt (unless --no-text)
  parse    -> parse marked quiz.txt into my_answers.json
  export   -> export quiz.json to quiz.txt only

Users should invoke this script instead of calling subordinate scripts directly.
"""
from __future__ import annotations
import argparse, subprocess, sys, shutil, os
from pathlib import Path

THIS_DIR = Path(__file__).parent
GEN = THIS_DIR / 'generate_quiz.py'
EXPORT = THIS_DIR / 'export_quiz_text.py'
PARSE = THIS_DIR / 'parse_marked_quiz.py'

def run(cmd):
    r = subprocess.run(cmd, text=True)
    if r.returncode != 0:
        raise SystemExit(r.returncode)

def parse_args(argv):
    p = argparse.ArgumentParser(description='Quiz master utility')
    sub = p.add_subparsers(dest='command', required=True)

    # prepare
    sp = sub.add_parser('prepare', help='Generate quiz + answer key (+ text)')
    provider = sp.add_mutually_exclusive_group(required=True)
    provider.add_argument('--ollama', action='store_true', help='Use local Ollama model')
    provider.add_argument('--ai', action='store_true', help='Use OpenAI API (needs OPENAI_API_KEY)')
    provider.add_argument('--template', action='store_true', help='Deterministic template mode (no LLM)')
    sp.add_argument('--ollama-model', default='mistral')
    sp.add_argument('--model', default='gpt-4o-mini')
    sp.add_argument('--count', type=int, default=5, help='Requested question count (Ollama<=5, OpenAI<=20)')
    sp.add_argument('--quiz', default='quiz.json')
    sp.add_argument('--answers', default='answer_key.json')
    sp.add_argument('--no-text', action='store_true', help='Skip creating quiz.txt')
    sp.add_argument('--sources', nargs='+', default=['system-design/designs/**/*.md', 'devops/**/*.md'])
    sp.add_argument('--fresh', action='store_true', help='Reduce repetition by tracking historical questions')

    # parse
    spp = sub.add_parser('parse', help='Parse marked quiz.txt -> my_answers.json')
    spp.add_argument('--in', dest='inp', default='quiz.txt')
    spp.add_argument('--out', dest='out', default='my_answers.json')
    spp.add_argument('--force', action='store_true')

    # export only
    spe = sub.add_parser('export', help='Export quiz.json -> quiz.txt')
    spe.add_argument('--quiz', default='quiz.json')
    spe.add_argument('--out', default='quiz.txt')
    spe.add_argument('--force', action='store_true')

    return p.parse_args(argv)

def cmd_prepare(a):
    if a.ollama and shutil.which('ollama') is None:
        print('[warn] ollama binary not found on PATH.')
    # Pre-clean old artifacts
    for path in [a.quiz, a.answers, 'quiz.txt']:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f'[info] Removed old {path}')
            except Exception as e:
                print(f'[warn] Could not remove {path}: {e}')
    gen_cmd = [sys.executable, str(GEN), '--count', str(a.count), '--quiz', a.quiz, '--answers', a.answers]
    if a.template:
        gen_cmd += ['--template']
    elif a.ollama:
        gen_cmd += ['--ollama', '--ollama-model', a.ollama_model]
    else:
        gen_cmd += ['--ai', '--model', a.model]
    if a.sources:
        gen_cmd += ['--sources', *a.sources]
    if a.fresh:
        gen_cmd.append('--fresh')
    print('[info] Generating quiz and answer key...')
    run(gen_cmd)
    if not a.no_text:
        print('[info] Exporting quiz.txt...')
        run([sys.executable, str(EXPORT), '--quiz', a.quiz, '--out', 'quiz.txt', '--force'])
    print('[ok] Prepared {quiz.json, answer_key.json, quiz.txt}')

def cmd_parse(a):
    print('[info] Parsing marked quiz file...')
    run([sys.executable, str(PARSE), '--in', a.inp, '--out', a.out] + (['--force'] if a.force else []))

def cmd_export(a):
    print('[info] Exporting text quiz...')
    run([sys.executable, str(EXPORT), '--quiz', a.quiz, '--out', a.out] + (['--force'] if a.force else []))
    print('[ok] Wrote quiz text template.')

def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.command == 'prepare':
        cmd_prepare(args)
    elif args.command == 'parse':
        cmd_parse(args)
    elif args.command == 'export':
        cmd_export(args)
    else:
        print('[error] Unknown command')
        return 2
    return 0

if __name__ == '__main__':  # pragma: no cover
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nInterrupted.')
        raise SystemExit(130)
