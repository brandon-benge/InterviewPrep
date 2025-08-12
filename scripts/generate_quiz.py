#!/usr/bin/env python3
"""Generate an interview prep multiple‑choice quiz from repository markdown (moved to scripts/).
Adds optional freshness control (--fresh) that tracks prior questions to reduce repetition.
"""
from __future__ import annotations
import argparse, json, os, random, re, sys, uuid
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore

OPENAI_IMPORT_ERROR = None
_OPENAI_NEW_CLIENT = False
try:  # pragma: no cover - optional dependency
    import openai  # type: ignore
    try:
        from openai import OpenAI  # type: ignore
        _OPENAI_NEW_CLIENT = True
        _openai_client = OpenAI()
    except Exception:
        _OPENAI_NEW_CLIENT = False
except Exception as e:  # pragma: no cover
    OPENAI_IMPORT_ERROR = e
    openai = None  # type: ignore

@dataclass
class Question:
    id: str; question: str; options: List[str]; topic: str; difficulty: str; answer: str; explanation: str
    def public_dict(self): return {"id": self.id, "question": self.question, "options": self.options, "topic": self.topic, "difficulty": self.difficulty}
    def answer_dict(self): return {"answer": self.answer, "explanation": self.explanation}

def read_markdown_files(patterns: List[str]) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for pattern in patterns:
        for path in glob(pattern, recursive=True):
            if not path.lower().endswith('.md'): continue
            try: files[path] = Path(path).read_text(encoding='utf-8')
            except Exception as e: print(f"[warn] failed reading {path}: {e}")
    return files

# Heuristic generation removed per user requirement (no local synthesis fallback).

DEFAULT_SOURCES = ["system-design/designs/**/*.md", "devops/**/*.md"]
HISTORY_FILE = Path('.quiz_history.json')  # stores normalized prior question texts

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate system design quiz JSON")
    p.add_argument("--count", type=int, default=5, help="Requested question count (Ollama capped at 5, OpenAI capped at 20)")
    p.add_argument("--quiz", default="quiz.json")
    p.add_argument("--answers", default="answer_key.json")
    p.add_argument("--sources", nargs="+", default=DEFAULT_SOURCES, help="Override source globs (disables random component focus if changed)")
    p.add_argument("--no-random-component", action="store_true", help="Disable random component directory focus even if components/ exists")
    p.add_argument("--model", default="gpt-4o-mini")
    p.add_argument("--ai", action="store_true", help="Use OpenAI API (requires OPENAI_API_KEY)")
    p.add_argument("--ollama", action="store_true", help="Use local Ollama model daemon")
    p.add_argument("--ollama-model", default="mistral")
    p.add_argument("--template", action="store_true", help="Deterministic template mode (no LLM; derives Q&A from markdown headings / key-value lines)")
    p.add_argument("--seed", type=int, default=0, help="Seed for deterministic template or distractor selection")
    p.add_argument("--fresh", action="store_true", help="Attempt to avoid repeating previous questions (persists .quiz_history.json; may retry)")
    p.add_argument("--verify", action="store_true", help="For Ollama: self-check each generated answer and adjust if model changes its mind")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)

def template_questions(files: Dict[str, str], count: int, seed: int) -> List[Question]:
    """Generate deterministic questions from markdown without any LLM.
    Strategy:
      1. Collect candidate (name, description, topic) triples from lines of the form 'Name: description' or list items '- Name: description'.
      2. Fallback: use headings (##, ###) as names with generic descriptions.
      3. Build questions: Show a description, ask which component it refers to.
      4. Options: correct name + 3 other distinct names (deterministic shuffle via seed).
    """
    # Extract candidates
    pairs = []  # (name, desc, topic)
    name_set = set()
    for path, text in files.items():
        topic = Path(path).stem.replace('-', ' ').title()
        for line in text.splitlines():
            line = line.strip().lstrip('-').lstrip('*').strip()
            if not line:
                continue
            # key: value pattern
            if ':' in line and not line.lower().startswith('http'):
                before, after = line.split(':', 1)
                name = before.strip()
                desc = after.strip()
                if 2 <= len(name) <= 60 and 5 <= len(desc) <= 200:
                    key = name.lower()
                    if key not in name_set:
                        name_set.add(key)
                        pairs.append((name, desc, topic))
        # headings fallback
        for line in text.splitlines():
            if line.startswith('##'):
                name = line.lstrip('#').strip()
                if 2 <= len(name) <= 60:
                    key = name.lower()
                    if key not in name_set:
                        name_set.add(key)
                        pairs.append((name, f"Concept related to {name}", topic))
    if not pairs:
        raise RuntimeError("No template candidates found in sources.")
    # Deterministic selection
    rng = random.Random(seed)
    # Guarantee enough distinct names for distractors; if not, duplicate markers
    names = [p[0] for p in pairs]
    # Build questions
    questions: List[Question] = []
    # Cycle through pairs to fulfill count
    for idx in range(count):
        base = pairs[idx % len(pairs)]
        name, desc, topic = base
        # pick 3 other distinct names
        distractor_pool = [n for n in names if n != name]
        if len(distractor_pool) < 3:
            # pad with synthetic distractors
            while len(distractor_pool) < 3:
                distractor_pool.append(f"Placeholder {len(distractor_pool)+1}")
        rng.shuffle(distractor_pool)
        distractors = distractor_pool[:3]
        option_names = [name] + distractors
        rng.shuffle(option_names)
        correct_index = option_names.index(name)
        qid = f"Q{idx+1}"
        stem = f"Which component is described: '{desc[:140]}'?"
        difficulty = 'easy' if len(desc) < 60 else 'medium'
        questions.append(Question(id=qid, question=stem, options=option_names, topic=topic, difficulty=difficulty, answer=chr(ord('A')+correct_index), explanation=f"{name} matches the description."))
    return questions

def openai_questions(files: Dict[str, str], count: int, model: str, uniqueness_token: str, recent_norm: List[str], temperature: float) -> List[Question]:  # pragma: no cover
    if not openai or OPENAI_IMPORT_ERROR: raise RuntimeError("openai package not available")
    if not os.getenv("OPENAI_API_KEY") and not _OPENAI_NEW_CLIENT: raise RuntimeError("OPENAI_API_KEY not set")
    if not _OPENAI_NEW_CLIENT: openai.api_key = os.getenv("OPENAI_API_KEY")
    max_chars = 28_000; pieces: List[str] = []; total = 0
    for path, text in files.items():
        trimmed = text[:2000]; part = f"\n# FILE: {path}\n{trimmed}\n"
        if total + len(part) > max_chars: continue
        pieces.append(part); total += len(part)
    corpus = "".join(pieces)
    recent_clause = ("Avoid reusing these prior question phrasings: " + "; ".join(recent_norm[:30])) if recent_norm else ""
    system = ("You are an assistant that creates high-quality multiple-choice quiz questions for system design and devops. "
              "Return STRICT JSON with fields: id, question, options(list of 4 concise strings), topic, difficulty (easy|medium|hard), answer (A-D), explanation. Do not output anything except JSON.")
    user = (f"Uniqueness token: {uniqueness_token}. Generate {count} diverse, novel questions (IDs Q1..Q{count}). "
            f"{recent_clause} Source material: {corpus[:12000]}")
    try:
        if _OPENAI_NEW_CLIENT:
            resp = _openai_client.chat.completions.create(model=model, messages=[{"role":"system","content":system},{"role":"user","content":user}], temperature=temperature)
            content = resp.choices[0].message.content
        else:
            resp = openai.ChatCompletion.create(model=model, messages=[{"role":"system","content":system},{"role":"user","content":user}], temperature=temperature)
            content = resp["choices"][0]["message"]["content"]
    except Exception as e: raise RuntimeError(f"OpenAI API error: {e}")
    json_text_match = re.search(r"```json\n(.*)```", content, re.DOTALL)
    json_text = json_text_match.group(1) if json_text_match else content
    data = json.loads(json_text)
    items = data["questions"] if isinstance(data, dict) and "questions" in data else data
    questions: List[Question] = []
    for obj in items:
        questions.append(Question(id=obj["id"], question=obj["question"].strip(), options=[o.strip() for o in obj["options"]][:4], topic=obj.get("topic","General"), difficulty=obj.get("difficulty","medium"), answer=obj.get("answer","A").strip(), explanation=obj.get("explanation","")))
    return questions

def ollama_questions(files: Dict[str, str], count: int, model: str, uniqueness_token: str, recent_norm: List[str], temperature: float) -> List[Question]:  # pragma: no cover
    if requests is None: raise RuntimeError("requests not installed")
    max_chars = 28_000; pieces: List[str] = []; total = 0
    for path, text in files.items():
        trimmed = text[:1500]; part = f"\n# FILE: {path}\n{trimmed}\n"
        if total + len(part) > max_chars: continue
        pieces.append(part); total += len(part)
    corpus = "".join(pieces)
    recent_clause = ("Avoid reusing these prior question phrasings: " + "; ".join(recent_norm[:30])) if recent_norm else ""
    prompt = (f"Uniqueness token: {uniqueness_token}. You will create {count} multiple choice questions (IDs Q1..Q{count}) about system design and devops based ONLY on the provided notes.\n"
              f"{recent_clause}\nReturn STRICT JSON (no prose) as an array. Each element must have keys: id, question, options (array of 4 short strings), topic, difficulty (easy|medium|hard), answer (A-D), explanation.\n"
              "Source notes: \n" + corpus[:12000])
    try:
        resp = requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temperature}}, timeout=120)
    except Exception as e: raise RuntimeError(f"Ollama request error: {e}")
    if resp.status_code != 200: raise RuntimeError(f"Ollama HTTP {resp.status_code}: {resp.text[:200]}")
    data = resp.json(); content = data.get("response", "")
    json_match = re.search(r"```json\n(.*)```", content, re.DOTALL)
    json_text = json_match.group(1) if json_match else content
    parsed = json.loads(json_text)
    items = parsed["questions"] if isinstance(parsed, dict) and "questions" in parsed else parsed
    questions: List[Question] = []
    for obj in items:
        questions.append(Question(id=obj["id"], question=obj["question"].strip(), options=[o.strip() for o in obj["options"]][:4], topic=obj.get("topic","General"), difficulty=obj.get("difficulty","medium"), answer=obj.get("answer","A").strip(), explanation=obj.get("explanation","")))
    return questions

def validate_questions(questions: List[Question], expected_count: int) -> Optional[str]:
    if len(questions) != expected_count: return f"Expected {expected_count} questions, got {len(questions)}"
    seen=set()
    for q in questions:
        # Normalize answers that may have been output as full option text or words instead of letter
        if q.answer and q.answer.upper() not in ["A","B","C","D"]:
            lower_ans = q.answer.strip().lower()
            mapped = None
            for idx, opt in enumerate(q.options):
                if lower_ans == opt.lower() or lower_ans.startswith(opt.lower()[:5]):
                    mapped = chr(ord('A')+idx); break
            if mapped:
                q.answer = mapped
            else:
                for idx, opt in enumerate(q.options):
                    if lower_ans in opt.lower():
                        q.answer = chr(ord('A')+idx); break
        if q.id in seen: return f"Duplicate id {q.id}"; seen.add(q.id)
        if len(q.options) != 4: return f"Question {q.id} does not have 4 options"
        if q.answer not in ["A","B","C","D"]: return f"Question {q.id} invalid answer letter {q.answer}"
        if q.answer not in [chr(ord('A')+i) for i in range(len(q.options))]: return f"Question {q.id} answer letter out of range"
    return None

def write_outputs(questions: List[Question], quiz_path: Path, answers_path: Path) -> None:
    quiz = [q.public_dict() for q in questions]
    key = {q.id: q.answer_dict() for q in questions}
    quiz_path.write_text(json.dumps(quiz, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')
    answers_path.write_text(json.dumps(key, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')

def main(argv: List[str]) -> int:
    args = parse_args(argv)
    OLLAMA_MAX = 5
    OPENAI_MAX = 20
    if args.count < 1:
        print("[error] --count must be at least 1")
        return 2
    # Optional random component focus: if system-design/components exists and user did not override sources
    if not args.no_random_component and args.sources == DEFAULT_SOURCES:
        comp_root = Path("system-design/components")
        if comp_root.exists():
            component_dirs = [d for d in comp_root.iterdir() if d.is_dir()]
            if component_dirs:
                chosen = random.choice(component_dirs)
                args.sources = [str(chosen / "**/*.md")]
                print(f"[info] Random component focus: {chosen.name}")
    files = read_markdown_files(args.sources)
    if not files:
        print("[error] No markdown files found for provided patterns.")
        return 1
    if args.template:
        # Template mode ignores AI/Ollama flags (cannot combine)
        if args.ai or args.ollama:
            print("[warn] --template provided; ignoring --ai/--ollama flags.")
    else:
        if not (args.ollama or args.ai):
            print("[error] Must supply one of --template, --ollama or --ai.")
            return 2
        if args.ollama and args.ai:
            print("[warn] Both --ollama and --ai provided; preferring --ollama.")
    if args.ollama and args.count > OLLAMA_MAX:
        print(f"[info] Capping requested count {args.count} to {OLLAMA_MAX} for Ollama (performance & latency)")
        args.count = OLLAMA_MAX
    elif (not args.ollama) and args.ai and args.count > OPENAI_MAX:
        print(f"[info] Capping requested count {args.count} to {OPENAI_MAX} for OpenAI")
        args.count = OPENAI_MAX

    # Load history for freshness
    history: List[str] = []
    if args.fresh and HISTORY_FILE.exists():
        try:
            loaded = json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
            if isinstance(loaded, list):
                history = loaded
        except Exception:
            history = []
    recent_norm = [re.sub(r'\s+', ' ', q.lower()).strip() for q in history][-80:]

    try:
        if args.template:
            print("[info] Generating deterministic template questions (no LLM)…")
            questions = template_questions(files, args.count, args.seed)
        elif args.ollama:
            if requests is None:
                print("[error] 'requests' not installed; required for Ollama. pip install requests")
                return 2
            try:
                requests.get("http://localhost:11434/api/tags", timeout=3)
            except Exception:
                print("[error] Ollama daemon not reachable at http://localhost:11434. Start it (brew services start ollama / launch app).")
                return 2
            print(f"[info] Generating questions via Ollama model {args.ollama_model}…")
            attempts = 2 if args.fresh else 1
            temperature = 0.6 if args.fresh else 0.4
            for attempt in range(1, attempts+1):
                token = str(uuid.uuid4())
                questions = ollama_questions(files, args.count, args.ollama_model, token, recent_norm, temperature)
                if not args.fresh:
                    break
                norm_new = [re.sub(r'\s+', ' ', q.question.lower()).strip() for q in questions]
                overlap = sum(1 for qn in norm_new if qn in recent_norm)
                if overlap == 0:
                    break
                if attempt < attempts:
                    print(f"[warn] {overlap} repeated question(s) detected, retrying for freshness...")
            if args.verify:
                corrected = 0
                for q in questions:
                    verify_prompt = (
                        "Verify the correctness of the provided answer letter for the multiple choice question.\n"
                        "Return STRICT JSON only like: {\"correct\": true/false, \"correct_answer\": \"A|B|C|D\"}. No explanations.\n"
                        f"Question: {q.question}\nOptions:\nA. {q.options[0]}\nB. {q.options[1]}\nC. {q.options[2]}\nD. {q.options[3]}\nCurrent answer: {q.answer}\n"
                    )
                    try:
                        resp = requests.post(
                            "http://localhost:11434/api/generate",
                            json={"model": args.ollama_model, "prompt": verify_prompt, "stream": False, "options": {"temperature": 0.0}},
                            timeout=90,
                        )
                        if resp.status_code != 200:
                            continue
                        data = resp.json().get('response','')
                        m = re.search(r"```json\n(.*)```", data, re.DOTALL)
                        payload = m.group(1) if m else data
                        js = json.loads(payload)
                        if isinstance(js, dict) and not js.get('correct', True):
                            new_ans = js.get('correct_answer')
                            if new_ans in ['A','B','C','D'] and new_ans != q.answer:
                                print(f"[verify] Adjusted {q.id} answer {q.answer} -> {new_ans}")
                                q.answer = new_ans; corrected += 1
                    except Exception:
                        continue
                if corrected:
                    print(f"[info] Verification adjusted {corrected} answer(s).")
        else:  # OpenAI
            if not os.getenv("OPENAI_API_KEY") and not _OPENAI_NEW_CLIENT:
                print("[error] OPENAI_API_KEY not set.")
                return 2
            if not openai:
                print("[error] openai package not installed. pip install openai")
                return 2
            print(f"[info] Generating questions via OpenAI model {args.model}…")
            attempts = 2 if args.fresh else 1
            temperature = 0.6 if args.fresh else 0.4
            for attempt in range(1, attempts+1):
                token = str(uuid.uuid4())
                questions = openai_questions(files, args.count, args.model, token, recent_norm, temperature)
                if not args.fresh:
                    break
                norm_new = [re.sub(r'\s+', ' ', q.question.lower()).strip() for q in questions]
                overlap = sum(1 for qn in norm_new if qn in recent_norm)
                if overlap == 0:
                    break
                if attempt < attempts:
                    print(f"[warn] {overlap} repeated question(s) detected, retrying for freshness...")
    except Exception as e:
        print(f"[error] Generation failed: {e}")
        return 1

    error = validate_questions(questions, args.count)
    if error:
        print(f"[error] Validation failed: {error}")
        return 1
    if args.dry_run:
        print("[info] Dry run complete; no files written.")
        return 0

    write_outputs(questions, Path(args.quiz), Path(args.answers))
    if args.fresh:
        try:
            norm_new = [re.sub(r'\s+', ' ', q.question.lower()).strip() for q in questions]
            updated = (history + norm_new)[-600:]
            HISTORY_FILE.write_text(json.dumps(updated, indent=2), encoding='utf-8')
        except Exception as e:
            print(f"[warn] Could not update history: {e}")
    print(f"[ok] Wrote {len(questions)} questions -> {args.quiz} and answer key -> {args.answers}")
    return 0

if __name__ == "__main__":  # pragma: no cover
    try: sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("\nInterrupted."); sys.exit(130)
