#from __future__ import annotations
from __future__ import annotations
import sqlite3
#!/usr/bin/env python3
# Moved to scripts/quiz/
import argparse, json, os, random, re, sys, uuid, time
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import List, Dict, Optional
try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore
OPENAI_IMPORT_ERROR=None; _OPENAI_NEW_CLIENT=False
from datetime import datetime as _dt
_orig_print = print
def print(*args, **kwargs):  # type: ignore
    if args:
        head = args[0]
        if isinstance(head, str):
            ts = _dt.now().isoformat(timespec='seconds')
            args = (f"[{ts}] {head}",) + args[1:]
    return _orig_print(*args, **kwargs)
try:
    import openai  # type: ignore
    try:
        from openai import OpenAI  # type: ignore
        _OPENAI_NEW_CLIENT=True; _openai_client=OpenAI()
    except Exception: _OPENAI_NEW_CLIENT=False
except Exception as e: OPENAI_IMPORT_ERROR=e; openai=None  # type: ignore
@dataclass
class Question:
    id: str; question: str; options: List[str]; topic: str; difficulty: str; answer: str; explanation: str
    def public_dict(self): return {"id": self.id, "question": self.question, "options": self.options, "topic": self.topic, "difficulty": self.difficulty}
    def answer_dict(self): return {"answer": self.answer, "explanation": self.explanation}

def read_markdown_files(patterns: List[str]) -> Dict[str,str]:
    files={}
    for pattern in patterns:
        for path in glob(pattern, recursive=True):
            if not path.lower().endswith('.md'): continue
            try: files[path]=Path(path).read_text(encoding='utf-8')
            except Exception as e: print(f"[warn] failed reading {path}: {e}")
    return files
DEFAULT_SOURCES=["system-design/designs/**/*.md","devops/**/*.md"]
HISTORY_FILE=Path('.quiz_history.json')

def parse_args(argv: List[str]):
    p=argparse.ArgumentParser()
    p.add_argument('--count',type=int,default=5); p.add_argument('--quiz',default='quiz.json'); p.add_argument('--answers',default='answer_key.json')
    p.add_argument('--sources',nargs='+',default=DEFAULT_SOURCES); p.add_argument('--no-random-component',action='store_true')
    p.add_argument('--model',default='gpt-4o-mini'); p.add_argument('--ai',action='store_true'); p.add_argument('--ollama',action='store_true'); p.add_argument('--ollama-model',default='mistral')
    # Ollama performance tuning
    p.add_argument('--ollama-temperature',type=float,help='Override default temperature (fresh=0.6 else 0.4)')
    p.add_argument('--ollama-num-predict',type=int,help='Max tokens for Ollama to predict (lower can speed up)')
    p.add_argument('--ollama-top-k',type=int,help='Sampling top_k')
    p.add_argument('--ollama-top-p',type=float,help='Sampling top_p')
    p.add_argument('--ollama-snippet-chars',type=int,default=-1,help='Chars per source file snippet when building prompt (-1 = unlimited)')
    p.add_argument('--ollama-corpus-chars',type=int,default=-1,help='Overall corpus char cap for Ollama prompt (-1 = unlimited)')
    p.add_argument('--ollama-compact-json',action='store_true',help='Ask model for compact JSON (no markdown fences, minimal whitespace)')
    p.add_argument('--debug-ollama-payload',action='store_true',help='Print the Ollama generation request JSON (prompt truncated) before sending.')
    p.add_argument('--dump-ollama-prompt',help='Write the full constructed Ollama prompt to this file for inspection.')
    p.add_argument('--dump-ollama-payload',help='Write the full Ollama request JSON (including complete prompt) to this file before sending.')
    p.add_argument('--dump-llm-payload',help='Alias for --dump-ollama-payload: Write the full LLM request JSON (including complete prompt) to this file before sending.')
    p.add_argument('--template',action='store_true'); p.add_argument('--seed',type=int,default=0); p.add_argument('--fresh',action='store_true'); p.add_argument('--verify',action='store_true'); p.add_argument('--dry-run',action='store_true')
    # RAG integration (now always ON; --no-rag allows override)
    p.add_argument('--rag-persist', default='.chroma', help='Persist directory for Chroma vector store')
    p.add_argument('--rag-k', type=int, default=4, help='Chunks per query to retrieve')
    p.add_argument('--rag-queries', nargs='+', help='Explicit retrieval queries (default: auto)')
    p.add_argument('--rag-max-queries', type=int, help='Hard cap on number of retrieval queries (default: derived from --count)')
    p.add_argument('--rag-local', action='store_true', help='Use local embedding function when loading store (must match build)')
    p.add_argument('--rag-embed-model', default='sentence-transformers/all-MiniLM-L6-v2', help='Embedding model name if using --rag-local')
    p.add_argument('--no-rag', dest='no_rag', action='store_true', help='Disable retrieval (debug)')
    # New filtering flags (operate on vector store metadata)
    p.add_argument('--restrict-sources', nargs='+', help='Limit retrieval to documents whose source path contains ANY of these substrings or matches these simple glob patterns (* and ?).')
    p.add_argument('--include-tags', nargs='+', help='Require at least one of these tag tokens (comma-separated tags stored per chunk).')
    p.add_argument('--include-h1', nargs='+', help='Require first H1 slug (or its tokens) to match one of these (case-insensitive, slugified).')
    # RAG context observability & truncation control
    p.add_argument('--dump-rag-context', help='Write the full (untruncated) synthesized RAG context (RAG_CONTEXT.md) to this file before any truncation.')
    return p.parse_args(argv)

def template_questions(files: Dict[str,str], count:int, seed:int)->List[Question]:
    pairs=[]; name_set=set()
    for path,text in files.items():
        topic=Path(path).stem.replace('-',' ').title()
        for line in text.splitlines():
            line=line.strip().lstrip('-').lstrip('*').strip()
            if not line: continue
            if ':' in line and not line.lower().startswith('http'):
                before,after=line.split(':',1); name=before.strip(); desc=after.strip()
                if 2<=len(name)<=60 and 5<=len(desc)<=200:
                    key=name.lower();
                    if key not in name_set: name_set.add(key); pairs.append((name,desc,topic))
        for line in text.splitlines():
            if line.startswith('##'):
                name=line.lstrip('#').strip();
                if 2<=len(name)<=60:
                    key=name.lower();
                    if key not in name_set: name_set.add(key); pairs.append((name,f"Concept related to {name}",topic))
    if not pairs: raise RuntimeError('No template candidates found.')
    rng=random.Random(seed); names=[p[0] for p in pairs]; questions=[]
    for idx in range(count):
        name,desc,topic=pairs[idx%len(pairs)]; distractor_pool=[n for n in names if n!=name]
        while len(distractor_pool)<3: distractor_pool.append(f'Placeholder {len(distractor_pool)+1}')
        rng.shuffle(distractor_pool); distractors=distractor_pool[:3]; option_names=[name]+distractors; rng.shuffle(option_names)
        correct_index=option_names.index(name); qid=f'Q{idx+1}'; stem=f"Which component is described: '{desc[:140]}'?"; difficulty='easy' if len(desc)<60 else 'medium'
        questions.append(Question(qid,stem,option_names,topic,difficulty,chr(ord('A')+correct_index),f"{name} matches the description."))
    return questions

def openai_questions(files: Dict[str,str], count:int, model:str, uniqueness_token:str, recent_norm:List[str], temperature:float)->List[Question]:
    if not openai or OPENAI_IMPORT_ERROR: raise RuntimeError('openai package not available')
    if not os.getenv('OPENAI_API_KEY') and not _OPENAI_NEW_CLIENT: raise RuntimeError('OPENAI_API_KEY not set')
    if not _OPENAI_NEW_CLIENT: openai.api_key=os.getenv('OPENAI_API_KEY')
    max_chars=28000; pieces=[]; total=0
    for path,text in files.items():
        trimmed=text[:2000]; part=f"\n# FILE: {path}\n{trimmed}\n"; 
        if total+len(part)>max_chars: continue
        pieces.append(part); total+=len(part)
    corpus=''.join(pieces); recent_clause=("Avoid reusing these prior question phrasings: "+'; '.join(recent_norm[:30])) if recent_norm else ''
    system=(
        "You are an assistant that creates high-quality multiple-choice quiz questions for system design and devops. "
        "If the provided source material includes citation lines of the form 'C<number>:' or a citation directory, you MUST: "
        "(1) Ground each question in one or more of those cited sections, (2) Choose a concise topic derived from the PRIMARY cited section heading (e.g. 'Caching', 'Load Balancing', 'Message Queues', 'Consistency'), "
        "(3) NEVER use the placeholder 'RAG_CONTEXT' as a topic, (4) Keep topic 1-4 words, Title Case. "
        "Return STRICT JSON with fields: id, question, options (list of 4), topic, difficulty, answer, explanation."
    )
    user=(f"Uniqueness token: {uniqueness_token}. Generate {count} diverse, novel questions (IDs Q1..Q{count}). {recent_clause} Source material: {corpus[:12000]}")
    start=time.time()
    if _OPENAI_NEW_CLIENT:
        resp=_openai_client.chat.completions.create(model=model,messages=[{"role":"system","content":system},{"role":"user","content":user}],temperature=temperature)
        content=resp.choices[0].message.content
    else:
        resp=openai.ChatCompletion.create(model=model,messages=[{"role":"system","content":system},{"role":"user","content":user}],temperature=temperature)
        content=resp['choices'][0]['message']['content']
    duration=time.time()-start
    print(f"[info] LLM response time (openai {model}): {duration:.2f}s")
    m=re.search(r"```json\n(.*)```",content,re.DOTALL); json_text=m.group(1) if m else content
    return _parse_model_questions(json_text, provider='openai')

def ollama_questions(files: Dict[str,str], count:int, model:str, uniqueness_token:str, recent_norm:List[str], temperature:float, *,
                     snippet_chars:int=1500, corpus_chars:int=12000, num_predict:Optional[int]=None,
                     top_k:Optional[int]=None, top_p:Optional[float]=None, compact_json:bool=False,
                     debug_payload:bool=False, dump_prompt_path:Optional[str]=None,
                     dump_payload_path:Optional[str]=None,
                     rag_no_truncate:bool=False)->List[Question]:
    if requests is None: raise RuntimeError('requests not installed')
    # Build reduced corpus respecting snippet and corpus size limits
    # Unlimited by default if snippet_chars or corpus_chars is -1
    max_chars = None if corpus_chars == -1 else 28000
    pieces = []
    total = 0
    for path, text in files.items():
        if rag_no_truncate and path == 'RAG_CONTEXT.md':
            trimmed = text if corpus_chars == -1 else text[:corpus_chars]
        else:
            trimmed = text if snippet_chars == -1 else text[:snippet_chars]
        part = f"\n# FILE: {path}\n{trimmed}\n"
        if corpus_chars != -1 and total + len(part) > corpus_chars:
            break
        if max_chars is not None and total + len(part) > max_chars:
            break
        pieces.append(part)
        total += len(part)
    corpus = ''.join(pieces)
    recent_clause=("Avoid reusing these prior question phrasings: "+'; '.join(recent_norm[:30])) if recent_norm else ''
    style_clause = 'Return STRICT COMPACT JSON array ONLY.' if compact_json else 'Return STRICT JSON as an array.'
    prompt=(
        f"Uniqueness token: {uniqueness_token}. You will create {count} multiple choice questions (IDs Q1..Q{count}) about system design and devops based ONLY on the provided notes.\n"
        f"{recent_clause}\n"
        "If a citation directory with lines like 'C1:' or blocks starting with '[C1]' is present: (1) Base each question on one or more cited sections, (2) Derive 'topic' from the primary cited section heading (concise 1-4 words, Title Case), (3) NEVER output 'RAG_CONTEXT' as a topic, (4) Avoid hallucinating facts not supported by the cited text.\n"
        f"{style_clause} Keys: id, question, options, topic, difficulty, answer, explanation. Keep explanations concise.\nSource notes:\n"+corpus[:corpus_chars]
    )
    start=time.time()
    ollama_options={'temperature':temperature}
    if num_predict: ollama_options['num_predict']=num_predict
    if top_k: ollama_options['top_k']=top_k
    if top_p: ollama_options['top_p']=top_p
    payload={'model':model,'prompt':prompt,'stream':False,'options':ollama_options}
    if dump_prompt_path:
        try:
            Path(dump_prompt_path).write_text(prompt,encoding='utf-8')
            print(f"[debug] Wrote full Ollama prompt -> {dump_prompt_path} (chars={len(prompt)})")
        except Exception as e:
            print(f"[warn] Could not write dump prompt file {dump_prompt_path}: {e}")
    if dump_payload_path:
        try:
            Path(dump_payload_path).write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
            print(f"[debug] Wrote full Ollama JSON payload -> {dump_payload_path} (chars={len(prompt)})")
        except Exception as e:
            print(f"[warn] Could not write dump payload file {dump_payload_path}: {e}")
    if debug_payload:
        trunc = prompt[:600]
        if len(prompt)>600: trunc += f"... [truncated, total {len(prompt)} chars]"
        debug_view = dict(payload)
        debug_view['prompt']=trunc
        try:
            print('[debug] Ollama request payload (truncated prompt):')
            print(json.dumps(debug_view,indent=2)[:4000])
        except Exception:
            pass
    resp=requests.post('http://localhost:11434/api/generate',json=payload,timeout=240)
    if resp.status_code!=200: raise RuntimeError(f'Ollama HTTP {resp.status_code}: {resp.text[:200]}')
    data=resp.json(); content=data.get('response',''); m=re.search(r"```json\n(.*)```",content,re.DOTALL); json_text=m.group(1) if m else content
    duration=time.time()-start
    print(f"[info] LLM response time (ollama {model}): {duration:.2f}s")
    return _parse_model_questions(json_text, provider='ollama')

def validate_questions(questions: List[Question], expected_count:int)->Optional[str]:
    if len(questions)!=expected_count: return f'Expected {expected_count} questions, got {len(questions)}'
    for q in questions:
        if q.answer.upper() not in ['A','B','C','D']:
            lower=q.answer.strip().lower();
            for idx,opt in enumerate(q.options):
                if lower==opt.lower() or lower.startswith(opt.lower()[:5]): q.answer=chr(ord('A')+idx); break
        if len(q.options)!=4: return f'Question {q.id} does not have 4 options'
    return None

# ---------------- Robust Parsing Helper ---------------- #
def _parse_model_questions(raw_json: str, provider: str) -> List[Question]:
    """Parse model JSON output robustly handling multiple shapes.
    Acceptable top-level forms:
      - list[question_obj]
      - {"questions": [...]} wrapper
      - {"data": [...]} wrapper
      - {"Q1": {...}, "Q2": {...}} mapping
      - single question object (wrapped into list)
    Each question object must provide id, question, options, answer. Missing fields get defaults.
    """
    try:
        data=json.loads(raw_json)
    except Exception as e:
        # Last resort: try to locate first JSON array substring
        m=re.search(r'(\[\s*{.*}\s*\])', raw_json, re.DOTALL)
        if not m:
            raise RuntimeError(f'{provider}: could not parse JSON: {e}')
        data=json.loads(m.group(1))
    # Unwrap common wrappers
    if isinstance(data, dict):
        if 'questions' in data and isinstance(data['questions'], list):
            data=data['questions']
        elif 'data' in data and isinstance(data['data'], list):
            data=data['data']
        else:
            # maybe dict of id->questionObj or a single question object
            if all(isinstance(v, dict) for v in data.values()):
                # add id into each if missing (key)
                mapped=[]
                for k,v in data.items():
                    if 'id' not in v: v['id']=k
                    mapped.append(v)
                data=mapped
            else:
                # assume single question object
                data=[data]
    if not isinstance(data, list):
        raise RuntimeError(f'{provider}: unexpected JSON shape (not a list after normalization)')
    questions: List[Question]=[]
    for idx,obj in enumerate(data, start=1):
        if not isinstance(obj, dict):
            # Skip non-dict entries
            continue
        qid=str(obj.get('id') or f'Q{idx}')
        question=str(obj.get('question','')).strip() or f'Placeholder question {idx}'
        raw_opts=obj.get('options')
        if not isinstance(raw_opts, list):
            # attempt to build options from any keys like optionA, a, b, c, d
            cand=[]
            for key in ['a','b','c','d','A','B','C','D']:
                if key in obj: cand.append(str(obj[key]))
            if not cand:
                cand=['Option A','Option B','Option C','Option D']
            raw_opts=cand
        options=[str(o).strip() for o in raw_opts][:4]
        while len(options)<4:
            options.append(f'Extra {len(options)+1}')
        answer=str(obj.get('answer','A')).strip().upper()
        if answer not in ['A','B','C','D']:
            answer='A'
        topic=str(obj.get('topic','General')).strip() or 'General'
        difficulty=str(obj.get('difficulty','medium')).strip() or 'medium'
        explanation=str(obj.get('explanation','')).strip()
        questions.append(Question(qid,question,options,topic,difficulty,answer,explanation))
    if not questions:
        raise RuntimeError(f'{provider}: no questions parsed from model output')
    return questions

def write_outputs(questions: List[Question], quiz_path: Path, answers_path: Path)->None:
    quiz=[q.public_dict() for q in questions]; key={q.id:q.answer_dict() for q in questions}
    quiz_path.write_text(json.dumps(quiz,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); answers_path.write_text(json.dumps(key,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main(argv: List[str])->int:
    args=parse_args(argv)
    if args.count<1: print('[error] --count must be at least 1'); return 2
    files=read_markdown_files(args.sources)

    def fetch_dynamic_h1_queries(db_path:str)->List[str]:
        queries=[]
        try:
            conn=sqlite3.connect(db_path)
            cur=conn.cursor()
            cur.execute("SELECT string_value FROM embedding_metadata WHERE key='h1' GROUP BY string_value;")
            rows=cur.fetchall()
            queries=[row[0][:80] for row in rows if row[0]]
            conn.close()
        except Exception as e:
            print(f"[warn] Could not fetch dynamic H1 queries: {e}")
        return queries
    # Force RAG usage unless explicitly disabled (master script ensures store readiness)
    rag_enabled = not getattr(args,'no_rag',False)
    if rag_enabled:
        try:
            # Prefer new package names; fallback to community
            try:
                from langchain_chroma import Chroma  # type: ignore
            except Exception:
                from langchain_community.vectorstores import Chroma  # type: ignore
            if args.rag_local:
                try:
                    from langchain_huggingface import HuggingFaceEmbeddings  # type: ignore
                except Exception:
                    from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
                embedding = HuggingFaceEmbeddings(model_name=args.rag_embed_model)
            else:
                from langchain_openai import OpenAIEmbeddings  # type: ignore
                embedding = OpenAIEmbeddings()
            if not os.path.isdir(args.rag_persist):
                print(f"[warn] RAG store '{args.rag_persist}' not found; proceeding without RAG.")
            else:
                vs = Chroma(persist_directory=args.rag_persist, embedding_function=embedding)
                # Dynamically fetch H1 subjects from SQLite
                db_path = os.path.join(args.rag_persist, 'chroma.sqlite3')
                dynamic_queries = fetch_dynamic_h1_queries(db_path)
                # If any filter overrides are set, use normal logic
                filter_override = any([
                    getattr(args, 'restrict_sources', None),
                    getattr(args, 'include_tags', None),
                    getattr(args, 'include_h1', None)
                ])
                if dynamic_queries and not filter_override and not args.rag_queries:
                    # Randomly select args.count queries from dynamic_queries
                    import random
                    rng = random.Random(getattr(args, 'seed', 0))
                    selected = rng.sample(dynamic_queries, min(args.count, len(dynamic_queries)))
                    print(f"[info] Using {len(selected)} random dynamic H1 queries from SQLite.")
                    default_queries = selected
                else:
                    default_queries = dynamic_queries if dynamic_queries else [
                        'caching strategies', 'load balancing', 'rate limiting', 'message queues', 'event driven architecture',
                        'microservices observability', 'database replication', 'consistency tradeoffs', 'api gateway', 'circuit breaker'
                    ]
                # Allow user to cap query count for speed
                if args.rag_max_queries:
                    queries = (args.rag_queries or default_queries)[:args.rag_max_queries]
                else:
                    queries = args.rag_queries or default_queries[:max(args.count, 5)]
                collected = []  # raw snippet blocks
                citations = []  # (label, source, heading)
                seen_snips = set()
                citation_idx = 1
                # Helper utilities for filtering & later cascade relaxation
                import fnmatch as _fnmatch, re as _re
                SLUG_RE = _re.compile(r'[^a-z0-9]+')
                def _slugify(x: str) -> str:
                    return SLUG_RE.sub('-', x.lower()).strip('-') if x else ''
                def _as_list(v):
                    if not v: return []
                    return list(v) if isinstance(v,(list,tuple)) else [v]
                restrict_patterns = [rp.lower() for rp in _as_list(getattr(args,'restrict_sources',None))]
                include_tags = [t.lower() for t in _as_list(getattr(args,'include_tags',None))]
                include_h1 = [_slugify(h) for h in _as_list(getattr(args,'include_h1',None))]
                filtering = bool(restrict_patterns or include_tags or include_h1)
                all_docs = []  # keep original order & allow cascade
                for q in queries:
                    try:
                        over_k = args.rag_k * (3 if filtering else 1)
                        docs = vs.similarity_search(q, k=over_k)
                    except Exception as e:
                        print(f"[warn] retrieval failed for '{q}': {e}"); continue
                    for d in docs:
                        snippet = d.page_content[:1000].strip()
                        if snippet in seen_snips:
                            continue
                        seen_snips.add(snippet)
                        all_docs.append((q,d,snippet))
                def _filter_docs(docs_list, use_sources, use_tags, use_h1):
                    if not filtering:
                        return docs_list
                    filtered_local = []
                    for q,d,snippet in docs_list:
                        md = getattr(d,'metadata',{}) or {}
                        src = md.get('source','').lower()
                        tags_raw = md.get('tags','')
                        tag_tokens = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
                        h1_val = md.get('h1','')
                        h1_slug = _slugify(h1_val)
                        keep = True
                        if use_sources and restrict_patterns:
                            matched=False
                            for pat in restrict_patterns:
                                if ('*' in pat or '?' in pat):
                                    if _fnmatch.fnmatch(src,pat): matched=True; break
                                elif pat in src: matched=True; break
                            if not matched: keep=False
                        if keep and use_tags and include_tags:
                            if not any(t in tag_tokens for t in include_tags): keep=False
                        if keep and use_h1 and include_h1:
                            if not h1_slug or all(ih not in h1_slug for ih in include_h1): keep=False
                        if keep:
                            filtered_local.append((q,d,snippet))
                    return filtered_local
                # Apply filters with cascade relaxation (h1 -> tags -> sources)
                working = all_docs
                if filtering:
                    working = _filter_docs(all_docs, True, True, True)
                    if not working:
                        if include_h1:
                            print('[warn] No chunks after filters; relaxing H1 filter...')
                            working = _filter_docs(all_docs, True, True, False)
                    if not working:
                        if include_tags:
                            print('[warn] Still empty; relaxing tag filter...')
                            working = _filter_docs(all_docs, True, False, False)
                    if not working:
                        if restrict_patterns:
                            print('[warn] Still empty; relaxing source filter...')
                            working = all_docs
                    if not working:
                        print('[warn] Filters produced zero documents; using unfiltered retrieval.')
                        working = all_docs
                # Now create citation blocks from working docs
                for q,d,snippet in working:
                    heading = d.metadata.get('section_heading') or (snippet.split('\n',1)[0][:80])
                    source = (d.metadata.get('source') or d.metadata.get('rel_path') or d.metadata.get('path') or 'unknown')
                    label = f"C{citation_idx}"
                    citation_idx += 1
                    citations.append((label, source, heading))
                    block = f"[{label}] (source: {source}, heading: {heading})\n{snippet}"
                    collected.append(block)
                if collected:
                    # Build structured context with citation directory then bodies
                    header_lines = [
                        "# Retrieved Knowledge (Citations)",
                        "Each question MUST be grounded in one or more cited sections. Do NOT invent facts.",
                        "Guidance: Derive 'topic' from the PRIMARY cited section heading; keep it concise (1-4 words, Title Case). NEVER use 'RAG_CONTEXT'."
                    ]
                    if filtering:
                        header_lines.append("(Requested filters: " + "; ".join([
                            f"sources={','.join(restrict_patterns)}" if restrict_patterns else '',
                            f"tags={','.join(include_tags)}" if include_tags else '',
                            f"h1={','.join(include_h1)}" if include_h1 else ''
                        ]).strip().strip('; ').strip() + ")")
                    # Build topic suggestions (heuristic simplification of heading)
                    def _suggest_topic(h: str) -> str:
                        base = h.split('|')[0].split(':')[0].split(' - ')[0].strip()
                        import re as _re
                        cleaned = _re.sub(r'[^A-Za-z0-9 ]+','', base)
                        words = cleaned.split()
                        return ' '.join(words[:5]).title() if words else 'General'
                    topic_suggestions = []
                    seen_topic_pairs = set()
                    for (label, _src, heading) in citations:
                        sugg = _suggest_topic(heading)
                        pair = (label, sugg)
                        if pair in seen_topic_pairs:
                            continue
                        seen_topic_pairs.add(pair)
                        topic_suggestions.append(f"{label} -> {sugg}")
                    if topic_suggestions:
                        header_lines.append("Suggested Topics (label -> topic):")
                        header_lines.extend(topic_suggestions)
                    for (label, source, heading) in citations:
                        header_lines.append(f"{label}: {source} :: {heading}")
                    header = "\n".join(header_lines)
                    body = "\n\n".join(collected)
                    joined = header + "\n\n---\n\n" + body
                    if getattr(args, 'dump_rag_context', None):
                        try:
                            Path(args.dump_rag_context).write_text(joined, encoding='utf-8')
                            print(f"[debug] Wrote full RAG context -> {args.dump_rag_context} (chars={len(joined)})")
                        except Exception as e:
                            print(f"[warn] Could not write RAG context file: {e}")
                    files = { 'RAG_CONTEXT.md': joined }
                    print(f"[info] RAG: aggregated {len(collected)} retrieved chunks with citations (full chars={len(joined)})")
                else:
                    print('[warn] RAG retrieval produced no context; falling back to source files.')
        except ModuleNotFoundError as e:
            print(f"[warn] RAG modules missing ({e}); continuing without RAG.")
        except Exception as e:
            print(f"[warn] RAG integration error: {e}; continuing without RAG.")
    if not files: print('[error] No markdown files found.'); return 1
    if args.template and (args.ai or args.ollama): print('[warn] --template provided; ignoring --ai/--ollama.')
    elif not args.template and not (args.ollama or args.ai): print('[error] Must supply one of --template, --ollama or --ai.'); return 2
    # No hard caps for Ollama or OpenAI question count
    history=[]
    if args.fresh and HISTORY_FILE.exists():
        try:
            loaded=json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
            if isinstance(loaded,list): history=loaded
        except Exception: history=[]
    recent_norm=[re.sub(r'\s+',' ',q.lower()).strip() for q in history][-80:]
    try:
        if args.template:
            print('[info] Generating deterministic template questions…')
            questions=template_questions(files,args.count,args.seed)
        elif args.ollama:
            if requests is None:
                print('[error] requests not installed'); return 2
            try:
                requests.get('http://localhost:11434/api/tags',timeout=3)
            except Exception:
                print('[error] Ollama daemon not reachable.'); return 2
            print(f'[info] Generating questions via Ollama model {args.ollama_model}…')
            base_temp=0.6 if args.fresh else 0.4
            temperature = args.ollama_temperature if args.ollama_temperature is not None else base_temp
            num_predict = args.ollama_num_predict
            top_k = args.ollama_top_k
            top_p = args.ollama_top_p
            snippet_chars = args.ollama_snippet_chars
            corpus_chars = args.ollama_corpus_chars
            compact_json = args.ollama_compact_json
            dump_payload_path = getattr(args, 'dump_llm_payload', None) or getattr(args, 'dump_ollama_payload', None)
            # Use queries selected for each question
            question_queries = queries[:args.count]
            questions = []
            for idx, q in enumerate(question_queries):
                # ...existing code for context retrieval...
                over_k = args.rag_k * (3 if filtering else 1)
                docs = []
                try:
                    docs = vs.similarity_search(q, k=over_k)
                except Exception as e:
                    print(f"[warn] retrieval failed for '{q}': {e}")
                collected = []
                seen_snips = set()
                for d in docs:
                    snippet = d.page_content[:1000].strip()
                    if snippet in seen_snips:
                        continue
                    seen_snips.add(snippet)
                    heading = d.metadata.get('section_heading') or (snippet.split('\n',1)[0][:80])
                    source = (d.metadata.get('source') or d.metadata.get('rel_path') or d.metadata.get('path') or 'unknown')
                    label = f"C1"
                    block = f"[{label}] (source: {source}, heading: {heading})\n{snippet}"
                    collected.append(block)
                if collected:
                    header_lines = [
                        f"# Retrieved Knowledge (Citations)",
                        f"Query: {q}",
                        "Each question MUST be grounded in one or more cited sections. Do NOT invent facts.",
                        "Guidance: Derive 'topic' from the PRIMARY cited section heading; keep it concise (1-4 words, Title Case). NEVER use 'RAG_CONTEXT'."
                    ]
                    header = "\n".join(header_lines)
                    body = "\n\n".join(collected)
                    joined = header + "\n\n---\n\n" + body
                    files_single = { 'RAG_CONTEXT.md': joined }
                else:
                    files_single = files
                token=str(uuid.uuid4())
                qlist = ollama_questions(
                    files_single, 1, args.ollama_model, token, recent_norm, temperature,
                    snippet_chars=snippet_chars, corpus_chars=corpus_chars, num_predict=num_predict,
                    top_k=top_k, top_p=top_p, compact_json=compact_json,
                    debug_payload=getattr(args,'debug_ollama_payload',False),
                    dump_payload_path=dump_payload_path)
                if qlist:
                    # Assign unique ID to each question
                    qobj = qlist[0]
                    qobj.id = f"Q{idx+1}"
                    questions.append(qobj)
            if args.verify:
                corrected=0
                for q in questions:
                    verify_prompt=("Verify the correctness of the provided answer letter. Return JSON {\"correct\":bool, \"correct_answer\":\"A-D\"}.\n" f"Question: {q.question}\nA. {q.options[0]}\nB. {q.options[1]}\nC. {q.options[2]}\nD. {q.options[3]}\nCurrent answer: {q.answer}\n")
                    try:
                        resp=requests.post('http://localhost:11434/api/generate',json={'model':args.ollama_model,'prompt':verify_prompt,'stream':False,'options':{'temperature':0.0}},timeout=90)
                        if resp.status_code!=200: continue
                        data=resp.json().get('response','')
                        m=re.search(r"```json\n(.*)```",data,re.DOTALL); payload=m.group(1) if m else data
                        js=json.loads(payload)
                        if isinstance(js,dict) and not js.get('correct',True):
                            new_ans=js.get('correct_answer')
                            if new_ans in ['A','B','C','D'] and new_ans!=q.answer:
                                q.answer=new_ans; corrected+=1
                    except Exception:
                        continue
                if corrected: print(f'[info] Verification adjusted {corrected} answer(s).')
        else:
            if not os.getenv('OPENAI_API_KEY') and not _OPENAI_NEW_CLIENT:
                print('[error] OPENAI_API_KEY not set.'); return 2
            if not openai:
                print('[error] openai package not installed.'); return 2
            print(f'[info] Generating questions via OpenAI model {args.model}…')
            temperature=0.6 if args.fresh else 0.4
            question_queries = queries[:args.count]
            questions = []
            for idx, q in enumerate(question_queries):
                over_k = args.rag_k * (3 if filtering else 1)
                docs = []
                try:
                    docs = vs.similarity_search(q, k=over_k)
                except Exception as e:
                    print(f"[warn] retrieval failed for '{q}': {e}")
                collected = []
                seen_snips = set()
                for d in docs:
                    snippet = d.page_content[:1000].strip()
                    if snippet in seen_snips:
                        continue
                    seen_snips.add(snippet)
                    heading = d.metadata.get('section_heading') or (snippet.split('\n',1)[0][:80])
                    source = (d.metadata.get('source') or d.metadata.get('rel_path') or d.metadata.get('path') or 'unknown')
                    label = f"C1"
                    block = f"[{label}] (source: {source}, heading: {heading})\n{snippet}"
                    collected.append(block)
                if collected:
                    header_lines = [
                        f"# Retrieved Knowledge (Citations)",
                        f"Query: {q}",
                        "Each question MUST be grounded in one or more cited sections. Do NOT invent facts.",
                        "Guidance: Derive 'topic' from the PRIMARY cited section heading; keep it concise (1-4 words, Title Case). NEVER use 'RAG_CONTEXT'."
                    ]
                    header = "\n".join(header_lines)
                    body = "\n\n".join(collected)
                    joined = header + "\n\n---\n\n" + body
                    files_single = { 'RAG_CONTEXT.md': joined }
                else:
                    files_single = files
                token=str(uuid.uuid4())
                qlist = openai_questions(files_single, 1, args.model, token, recent_norm, temperature)
                if qlist:
                    qobj = qlist[0]
                    qobj.id = f"Q{idx+1}"
                    questions.append(qobj)
    except Exception as e:
        print(f'[error] Generation failed: {e}'); return 1
    error=validate_questions(questions,args.count)
    if error: print(f'[error] Validation failed: {error}'); return 1
    if args.dry_run: print('[info] Dry run complete.'); return 0
    write_outputs(questions,Path(args.quiz),Path(args.answers))
    if args.fresh:
        try:
            # Retain only the most recent 100 normalized question stems to enforce tighter freshness window.
            norm_new=[re.sub(r'\s+',' ',q.question.lower()).strip() for q in questions]; updated=(history+norm_new)[-100:]; HISTORY_FILE.write_text(json.dumps(updated,indent=2),encoding='utf-8')
        except Exception as e: print(f'[warn] Could not update history: {e}')
    print(f'[ok] Wrote {len(questions)} questions -> {args.quiz} and answer key -> {args.answers}')
    return 0

if __name__=='__main__':
    try: sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt: print('\nInterrupted.'); sys.exit(130)
