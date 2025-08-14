#!/usr/bin/env python3
"""Master utility script for quiz workflow (moved to scripts/quiz/)."""
from __future__ import annotations
import argparse, subprocess, sys, shutil, os, json, time, shlex
from datetime import datetime as _dt
from pathlib import Path
THIS_DIR = Path(__file__).parent
GEN = THIS_DIR / 'generate_quiz.py'
EXPORT = THIS_DIR / 'export_quiz_text.py'
PARSE = THIS_DIR / 'parse_marked_quiz.py'
VECTOR_BUILD = Path(__file__).parent.parent / 'rag' / 'vector_store_build.py'

_orig_print = print
def print(*args, **kwargs):  # type: ignore
    if args:
        head=args[0]
        if isinstance(head,str):
            ts=_dt.now().isoformat(timespec='seconds')
            args=(f"[{ts}] {head}",)+args[1:]
    return _orig_print(*args, **kwargs)

def run(cmd):
    # Log the exact command being executed (escaped) for transparency
    if isinstance(cmd, (list, tuple)):
        printable = ' '.join(shlex.quote(str(c)) for c in cmd)
    else:
        printable = str(cmd)
    print(f'[exec] {printable}')
    r = subprocess.run(cmd, text=True)
    if r.returncode != 0:
        raise SystemExit(r.returncode)

def parse_args(argv):
    p = argparse.ArgumentParser(description='Quiz master utility')
    sub = p.add_subparsers(dest='command', required=True)
    sp = sub.add_parser('prepare', help='Generate quiz + answer key (+ text)')
    provider = sp.add_mutually_exclusive_group(required=True)
    provider.add_argument('--ollama', action='store_true')
    provider.add_argument('--ai', action='store_true')
    provider.add_argument('--template', action='store_true')
    sp.add_argument('--ollama-model', default='mistral')
    sp.add_argument('--model', default='gpt-4o-mini')
    sp.add_argument('--count', type=int, default=5)
    sp.add_argument('--quiz', default='quiz.json')
    sp.add_argument('--answers', default='answer_key.json')
    sp.add_argument('--no-text', action='store_true')
    sp.add_argument('--sources', nargs='+', default=['system-design/designs/**/*.md', 'devops/**/*.md'])
    sp.add_argument('--fresh', action='store_true')
    sp.add_argument('--persist', default='.chroma', help='Vector store directory (must exist or use --auto-build)')
    sp.add_argument('--auto-build', action='store_true', help='Auto build vector store if missing (may take time)')
    sp.add_argument('--local-embeddings', action='store_true', help='Expect local embeddings were used for the store')
    sp.add_argument('--rag-k', type=int, default=4, help='Chunks per query retrieval (passed through)')
    sp.add_argument('--rag-queries', nargs='+', help='Explicit retrieval queries')
    # Debug / tracing options (pass-through to generate)
    sp.add_argument('--debug-ollama-payload', action='store_true', help='Print truncated Ollama request payload before sending')
    sp.add_argument('--dump-rag-context', help='Write the full (untruncated) synthesized RAG context to this file before any truncation.')
    sp.add_argument('--dump-llm-payload', help='Write the full LLM request JSON (including complete prompt) to this file before sending. Applies to Ollama and OpenAI.')
    # Pass-through filtering flags for retrieval (generate_quiz.py)
    sp.add_argument('--restrict-sources', nargs='+', help='Limit retrieval to chunks whose source path matches any pattern (substring or glob).')
    sp.add_argument('--include-tags', nargs='+', help='Require at least one of these tags be present in chunk metadata.')
    sp.add_argument('--include-h1', nargs='+', help='Require first H1 slug (or contains) to match one of these values.')
    spp = sub.add_parser('parse', help='Parse marked quiz.txt -> my_answers.json')
    spp.add_argument('--in', dest='inp', default='quiz.txt')
    spp.add_argument('--out', dest='out', default='my_answers.json')
    spp.add_argument('--force', action='store_true')
    spe = sub.add_parser('export', help='Export quiz.json -> quiz.txt')
    spe.add_argument('--quiz', default='quiz.json')
    spe.add_argument('--out', default='quiz.txt')
    spe.add_argument('--force', action='store_true')
    return p.parse_args(argv)

def _check_vector_store(persist: str, local: bool) -> bool:
    if not os.path.isdir(persist):
        return False
    try:
        try:
            from langchain_chroma import Chroma  # type: ignore
        except Exception:
            from langchain_community.vectorstores import Chroma  # type: ignore
        if local:
            try:
                from langchain_huggingface import HuggingFaceEmbeddings  # type: ignore
            except Exception:
                from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
            emb = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        else:
            from langchain_openai import OpenAIEmbeddings  # type: ignore
            emb = OpenAIEmbeddings()
        vs = Chroma(persist_directory=persist, embedding_function=emb)
        _ = vs.similarity_search('health check query', k=1)
        return True
    except Exception as e:
        print(f'[warn] Vector store health check failed: {e}')
        return False

def _build_vector_store(persist: str, local: bool):
    print(f'[info] Building vector store -> {persist} (local={local}) ...')
    cmd=[sys.executable, str(VECTOR_BUILD), '--persist', persist]
    if local: cmd.append('--local')
    run(cmd)

def _check_openai():
    if not os.getenv('OPENAI_API_KEY'):
        return '[error] OPENAI_API_KEY not set'
    try:
        import requests  # type: ignore
        r=requests.get('https://api.openai.com/v1/models',headers={'Authorization':f"Bearer {os.getenv('OPENAI_API_KEY')}"},timeout=6)
        if r.status_code>=400:
            return f'[error] OpenAI API unreachable (HTTP {r.status_code})'
    except Exception as e:
        return f'[error] OpenAI connectivity check failed: {e}'
    return ''

def _check_ollama(model: str):
    import shutil as _shutil
    if _shutil.which('ollama') is None:
        return '[error] ollama binary not found'
    try:
        import requests  # type: ignore
        r=requests.get('http://localhost:11434/api/tags',timeout=4)
        if r.status_code!=200:
            return f'[error] Ollama daemon HTTP {r.status_code}'
        data=r.json(); tags=[t.get('name') for t in data.get('models',data if isinstance(data,list) else [])]
        def _matches(name: str) -> bool:
            if not name: return False
            base=name.split(':',1)[0]
            return name==model or base==model
        if not any(_matches(n) for n in tags):
            print(f'[info] Model {model} not present locally (found: {', '.join(tags) or 'none'}); attempting pull...')
            pr=subprocess.run(['ollama','pull',model],text=True)
            if pr.returncode!=0:
                return f'[error] Failed to pull model {model}'
    except Exception as e:
        return f'[error] Ollama connectivity check failed: {e}'
    return ''

def preflight(a):
    print('[info] Preflight validation starting...')
    # Vector store
    if not _check_vector_store(a.persist, a.local_embeddings):
        if a.auto_build:
            _build_vector_store(a.persist, a.local_embeddings)
            if not _check_vector_store(a.persist, a.local_embeddings):
                print('[error] Vector store build failed or unhealthy.'); return False
        else:
            print(f'[error] Vector store missing/unhealthy at {a.persist}. Use --auto-build.'); return False
    # Provider checks
    if a.ai:
        err=_check_openai()
        if err: print(err); return False
    if a.ollama:
        err=_check_ollama(a.ollama_model)
        if err: print(err); return False
    print('[info] Preflight validation passed.')
    return True

def cmd_prepare(a):
    if a.ollama and shutil.which('ollama') is None:
        print('[warn] ollama binary not found on PATH.')
    if not preflight(a):
        print('[error] Aborting due to failed preflight.')
        return
    for path in [a.quiz, a.answers, 'quiz.txt']:
        if os.path.exists(path):
            try: os.remove(path); print(f'[info] Removed old {path}')
            except Exception as e: print(f'[warn] Could not remove {path}: {e}')
    gen_cmd = [sys.executable, str(GEN), '--count', str(a.count), '--quiz', a.quiz, '--answers', a.answers,
               '--rag-persist', a.persist, '--rag-k', str(a.rag_k)]
    if a.rag_queries:
        gen_cmd += ['--rag-queries', *a.rag_queries]
    if a.restrict_sources:
        gen_cmd += ['--restrict-sources', *a.restrict_sources]
    if a.include_tags:
        gen_cmd += ['--include-tags', *a.include_tags]
    if a.include_h1:
        gen_cmd += ['--include-h1', *a.include_h1]
    if a.local_embeddings:
        gen_cmd.append('--rag-local')
    if a.template: gen_cmd += ['--template']
    elif a.ollama: gen_cmd += ['--ollama', '--ollama-model', a.ollama_model]
    else: gen_cmd += ['--ai', '--model', a.model]
    if a.ollama and a.debug_ollama_payload:
        gen_cmd.append('--debug-ollama-payload')
    if a.dump_rag_context:
        gen_cmd += ['--dump-rag-context', a.dump_rag_context]
    if a.dump_llm_payload:
        gen_cmd += ['--dump-llm-payload', a.dump_llm_payload]
    if a.sources: gen_cmd += ['--sources', *a.sources]
    if a.fresh: gen_cmd.append('--fresh')
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
    if args.command == 'prepare': cmd_prepare(args)
    elif args.command == 'parse': cmd_parse(args)
    elif args.command == 'export': cmd_export(args)
    else: print('[error] Unknown command'); return 2
    return 0

if __name__ == '__main__':
    try: raise SystemExit(main())
    except KeyboardInterrupt: print('\nInterrupted.'); raise SystemExit(130)
