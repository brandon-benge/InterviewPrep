# Quiz Generation Guide (AI Study Aid)

Generate multiple-choice quizzes from repository content to self-test system design & devops knowledge.

***
## 🚀 One-Command Workflow
> Prepare everything (quiz.json, answer_key.json, quiz.txt):
```bash
# Local model (Ollama, capped at 5 questions)
./scripts/run_venv.sh scripts/master.py prepare --ollama --ollama-model mistral --count 5 --fresh

# OpenAI (remote API, up to 20 questions; will cap if higher)
./scripts/run_venv.sh scripts/master.py prepare --ai --model gpt-4o-mini --count 12 --fresh

# Deterministic (no LLM / template mode)
./scripts/run_venv.sh scripts/master.py prepare --template --count 8
```
> Validate (interactive):
```bash
./scripts/run_venv.sh scripts/validate_quiz_answers.py --quiz quiz.json --answers answer_key.json
```
> Validate using your own answers JSON (e.g. produced by parse tool):
```bash
./scripts/run_venv.sh scripts/validate_quiz_answers.py --quiz quiz.json --answers answer_key.json --user my_answers.json
```

## 🧩 Files Produced
- `quiz.json` – list of question objects (no answers)
- `answer_key.json` – mapping question id -> { answer, explanation }
- `quiz.txt` – markable plain text template (optional, created by prepare script unless --no-text)

## 🛠️ Providers & Limits
| Provider | Flag | Max Questions | Notes |
|----------|------|---------------|-------|
| Ollama   | `--ollama` | 5 | Local inference, faster iteration, no API cost |
| OpenAI   | `--ai`     | 20 | Requires `OPENAI_API_KEY` |

> Accuracy Note (Ollama): Local models may occasionally produce mismatches (e.g. answer letter not conceptually matching best option, weak explanations, or subtly duplicated question stems). Always validate logically, and if a question looks off: (1) re-run with `--fresh`, (2) switch to the OpenAI provider for higher consistency, or (3) manually correct the affected item. The validator only checks structural correctness (count, 4 options, answer in A-D), not semantic quality.

## 🔍 Ollama Setup & Validation
> Install: https://ollama.com
```bash
ollama pull mistral
./scripts/run_venv.sh scripts/check_ollama.py check
```
> Manage via tasks (Install / Start / Stop / Check) or CLI (`brew services start ollama`).

## 📦 Advanced (Manual Marking Workflow)
> Export plain text:
```bash
./scripts/run_venv.sh scripts/export_quiz_text.py            # -> quiz.txt
```
> Mark answers (`[X] A.` exactly one per question) then parse:
```bash
./scripts/run_venv.sh scripts/master.py parse --in quiz.txt --out my_answers.json --force
```
> Validate:
```bash
./scripts/run_venv.sh scripts/validate_quiz_answers.py --quiz quiz.json --answers answer_key.json --user my_answers.json
```

## 🔧 Customizing
- Limit corpus scope: `--sources system-design/designs/video-streaming/*.md`
- Change models: `--ollama-model llama3` or `--model gpt-4o-mini`
- Skip text export: add `--no-text` to `master.py prepare`.
- Improve novelty: add `--fresh` to reduce repetition (stores normalized prior questions in `.quiz_history.json`; increases temperature slightly and retries once if overlap detected).
- Improve local answer accuracy: after generation run `generate_quiz.py` directly with `--verify` (adds a self-check pass per question; slower, Ollama only) or integrate later into master script.
- Disable randomness of component focus: pass `--sources ...` or add `--no-random-component` when directly invoking `generate_quiz.py` (the master script uses default random component selection automatically when sources unchanged).
- Deterministic generation: use `--template` (with optional `--seed <n>` via direct `generate_quiz.py`) for hallucination-free baseline sourced from markdown key-value lines and headings.

## ❓ Troubleshooting
| Symptom | Cause | Resolution |
|---------|-------|------------|
| Ollama request error | Daemon not running | `./scripts/run_venv.sh scripts/check_ollama.py start` (macOS) or launch app |
| 0 questions returned | Model output malformed | Re-run; ensure model supports instruction following |
| Validation failed: count mismatch | Model produced fewer items | Re-run; sometimes temperature / truncation issues |
| OPENAI_API_KEY error | Env var missing | `export OPENAI_API_KEY=sk-...` |
| Question seems wrong / answer dubious (Ollama) | Model hallucination or shallow reasoning | Re-run with `--fresh`; compare with notes; consider OpenAI provider for higher reliability |

## 📜 Example Snippet
```json
[
  {
    "id": "Q1",
    "question": "Which component handles rate limiting?",
    "options": ["API Gateway", "Object Store", "CDN Edge", "Log Indexer"],
    "topic": "Rate Limiter System Design",
    "difficulty": "medium"
  }
]
```

#### 
> Return to main README: [README.md](./README.md)
