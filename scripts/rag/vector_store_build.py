#!/usr/bin/env python3
"""Build a local Chroma vector store from all repository Markdown files.

Usage:
  ./scripts/bin/run_venv.sh scripts/rag/vector_store_build.py \
      --persist ./chroma_store \
      --chunk-size 800 --chunk-overlap 120 --force

Options:
  --persist PATH       Directory to persist Chroma DB (default: ./.chroma)
  --chunk-size N       Characters per chunk (default: 1000)
  --chunk-overlap N    Overlap between chunks (default: 150)
  --glob PATTERN       Additional glob (repeatable) to include (default: **/*.md)
  --exclude PATTERN    Glob to exclude (repeatable) (e.g. .venv/**)
  --force              Rebuild even if target directory exists

Environment:
  OPENAI_API_KEY required for OpenAI embeddings OR set --local to use sentence-transformers all-MiniLM model.

Examples:
  OPENAI_API_KEY=sk-... ./scripts/bin/run_venv.sh scripts/rag/vector_store_build.py
  ./scripts/bin/run_venv.sh scripts/rag/vector_store_build.py --local --model all-MiniLM-L6-v2
"""
from __future__ import annotations
import argparse, sys, shutil, re
from pathlib import Path
from typing import List

def lazy_import():
    """Import vector store + splitter using new package names with fallback."""
    try:
        from langchain_chroma import Chroma  # type: ignore
    except Exception:
        from langchain_community.vectorstores import Chroma  # type: ignore
    from langchain.docstore.document import Document  # type: ignore
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore
    return Chroma, Document, RecursiveCharacterTextSplitter

def embedding_fn(local: bool, model: str):
    if local:
        try:
            from langchain_huggingface import HuggingFaceEmbeddings  # type: ignore
        except Exception:
            from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
        return HuggingFaceEmbeddings(model_name=model or 'sentence-transformers/all-MiniLM-L6-v2')
    else:
        from langchain_openai import OpenAIEmbeddings  # type: ignore
        return OpenAIEmbeddings(model=model or 'text-embedding-3-small')

def collect_files(globs: List[str], excludes: List[str]) -> List[Path]:
    root = Path('.')
    candidates = set()
    import fnmatch
    for g in globs:
        for p in root.rglob('*.md') if g == '**/*.md' else root.rglob(g):
            if p.is_file():
                candidates.add(p)
    results = []
    for p in candidates:
        rel = p.relative_to(root)
        skip = False
        for ex in excludes:
            if fnmatch.fnmatch(str(rel), ex):
                skip = True
                break
        if skip:
            continue
        if p.suffix.lower() == '.md':
            results.append(p)
    return sorted(results)

TAG_TOKEN_RE = re.compile(r'[^a-z0-9]+')
H1_RE = re.compile(r'^#\s+(.+)', re.MULTILINE)

def slugify(text: str) -> str:
    return TAG_TOKEN_RE.sub('-', text.lower()).strip('-')

def derive_tags(path: Path, h1: str | None) -> list[str]:
    """Lightweight tag derivation including optional H1 heading.
    Strategy:
      - Optional H1 slug first (if present)
      - Up to first 3 directory names
      - File stem tokens (split on non-alphanumerics)
    """
    parts = list(path.parts)
    dir_tags = [p.lower() for p in parts[:-1][:3]]
    stem_tokens = [t for t in TAG_TOKEN_RE.split(path.stem.lower()) if t]
    ordered: list[str] = []
    seen: set[str] = set()
    if h1:
        h1_slug = slugify(h1)[:60]
        if h1_slug and h1_slug not in seen:
            seen.add(h1_slug); ordered.append(h1_slug)
    for t in (*dir_tags, *stem_tokens):
        if t and t not in seen:
            seen.add(t); ordered.append(t)
    return ordered

PREFERRED_SECTION_LEVELS = [3, 2]  # Cascade order: try H3, then H2

def _split_by_heading_level(text: str, level: int):
    pattern = re.compile(rf'^({"#"*level})\s+(.*)', re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return []
    sections = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx+1].start() if idx+1 < len(matches) else len(text)
        heading = m.group(2).strip()
        section_text = text[start:end].strip()
        sections.append((section_text, heading, idx, level))
    return sections

def _cascade_sections(text: str):
    for lvl in PREFERRED_SECTION_LEVELS:
        secs = _split_by_heading_level(text, lvl)
        if secs:
            return secs
    return []  # none found

def build(args):
    Chroma, Document, TextSplitter = lazy_import()
    # Only apply default exclusions if user does not specify any --exclude flags
    default_excludes = ['.venv/**', 'scripts/**', '[A-Z]*.md']
    excludes = args.exclude if args.exclude is not None else default_excludes
    paths = collect_files(
        args.glob or ['**/*.md'],
        excludes
    )
    if not paths:
        print('No markdown files found.')
        return 1
    if args.force and Path(args.persist).exists():
        shutil.rmtree(args.persist)
    print(f'Collecting {len(paths)} markdown files...')
    docs = []  # list of Documents
    for p in paths:
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            print(f'WARN: skip {p}: {e}')
            continue
        # Extract first H1 heading if present
        m = H1_RE.search(text)
        h1 = m.group(1).strip() if m else ''
        tags_list = derive_tags(p, h1 if h1 else None)
        cascaded = _cascade_sections(text)
        if cascaded:
            for section_text, heading, idx, lvl in cascaded:
                sec_meta = {
                    "source": str(p),
                    "tags": ",".join(tags_list),
                    "h1": h1,
                    "section_level": lvl,
                    "section_heading": heading,
                    "section_index": idx
                }
                docs.append(Document(page_content=section_text, metadata=sec_meta))
        else:
            # Fall back to size-based splitting later
            meta = {"source": str(p), "tags": ",".join(tags_list), "h1": h1}
            docs.append(Document(page_content=text, metadata=meta))
    # Decide splitting: if any section_heading metadata exists, keep as-is; else apply size splitter
    if any('section_heading' in d.metadata for d in docs):
        splits = docs
        levels = {d.metadata.get('section_level') for d in docs if 'section_level' in d.metadata}
        print(f'Cascade section mode (levels used: {sorted(levels)}) -> {len(splits)} sections.')
    else:
        splitter = TextSplitter(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
        print('No H3/H2 headings found; using size-based splitting...')
        splits = splitter.split_documents(docs)
        avg = sum(len(s.page_content) for s in splits)//max(len(splits),1)
        print(f'Generated {len(splits)} chunks (avg ~{avg} chars).')
    emb = embedding_fn(args.local, args.model)
    print('Embedding & persisting to Chroma...')
    vs = Chroma.from_documents(splits, embedding=emb, persist_directory=args.persist)
    try:
        vs.persist()
    except Exception:
        pass
    print(f'Done. Persist dir: {args.persist}')
    return 0

def parse(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--persist', default='.chroma', help='Persistence directory')
    ap.add_argument('--chunk-size', type=int, default=1000)
    ap.add_argument('--chunk-overlap', type=int, default=150)
    ap.add_argument('--glob', action='append', help='Glob pattern(s) to include (repeat)')
    ap.add_argument('--exclude', action='append', help='Glob pattern(s) to exclude (repeat)')
    ap.add_argument('--force', action='store_true', help='Rebuild even if directory exists')
    ap.add_argument('--local', action='store_true', help='Use local HuggingFace embedding model')
    ap.add_argument('--model', default='', help='Embedding model (OpenAI embedding or local HF)')
    return ap.parse_args(argv)

if __name__ == '__main__':
    args = parse(sys.argv[1:])
    sys.exit(build(args))
