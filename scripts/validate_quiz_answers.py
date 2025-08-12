#!/usr/bin/env python3
"""Validate user answers against quiz & answer key (moved to scripts/)."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Dict, Any, List

def parse_args(argv: List[str]):
    p = argparse.ArgumentParser(description="Validate quiz answers")
    p.add_argument("--quiz", default="quiz.json")
    p.add_argument("--answers", default="answer_key.json")
    p.add_argument("--user")
    p.add_argument("--show-correct-first", action="store_true")
    return p.parse_args(argv)

def load_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))

def interactive_collect(quiz: List[Dict[str, Any]]) -> Dict[str, str]:
    answers: Dict[str, str] = {}
    print("Enter your answers (A-D). Press Enter to skip (counts as incorrect).\n")
    for q in quiz:
        print(f"{q['id']}: {q['question']}")
        for idx, opt in enumerate(q['options']):
            letter = chr(ord('A') + idx)
            print(f"  {letter}. {opt}")
        while True:
            val = input("Answer (A-D): ").strip().upper()
            if val == "": print("(skipped)\n"); break
            if val in ["A", "B", "C", "D"]: answers[q['id']] = val; print(); break
            print("Please enter A-D or leave blank to skip.")
    return answers

def score(quiz: List[Dict[str, Any]], key: Dict[str, Any], user_answers: Dict[str, str], show_correct_first: bool) -> None:
    total = len(quiz); correct = 0
    print("\n===== Results =====\n")
    for q in quiz:
        qid = q['id']; user_ans = user_answers.get(qid); key_entry = key.get(qid)
        if not key_entry: print(f"[warn] Missing answer key for {qid}"); continue
        correct_ans = key_entry['answer']; is_correct = user_ans == correct_ans
        if is_correct: correct += 1
        print(f"{'✅' if is_correct else '❌'} {qid} Your: {user_ans or '-'} Correct: {correct_ans}")
        explanation = key_entry.get('explanation','')[:400]
        if show_correct_first: print(f"   Explanation: {explanation}")
        else: print(f"   {explanation}")
    pct = (correct / total) * 100 if total else 0
    print(f"\nScore: {correct}/{total} = {pct:.1f}%")

def main(argv):
    args = parse_args(argv)
    quiz_path = Path(args.quiz); ans_path = Path(args.answers)
    if not quiz_path.exists() or not ans_path.exists(): print("[error] quiz or answer key path does not exist"); return 1
    quiz = load_json(quiz_path); key = load_json(ans_path)
    if not isinstance(quiz, list) or not isinstance(key, dict): print("[error] Invalid JSON structure"); return 1
    user_answers = load_json(Path(args.user)) if args.user else interactive_collect(quiz)
    score(quiz, key, user_answers, args.show_correct_first); return 0

if __name__ == "__main__":  # pragma: no cover
    import sys
    try: raise SystemExit(main(sys.argv[1:]))
    except KeyboardInterrupt: print("\nInterrupted."); raise SystemExit(130)
