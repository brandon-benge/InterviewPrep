# GEMINI.md

Copy this file to the repository root as `GEMINI.md` when you want Gemini CLI to understand your specification layout without repeating it in every prompt.

Replace the placeholders before use.

## Read Order

When a task involves the governed system, read `SpecRepo/` in this order:

1. `SpecRepo/README.md`
2. `SpecRepo/PROBLEM.md`
3. `SpecRepo/INVARIANTS.md`
4. `SpecRepo/REQUIREMENTS.md`
5. `SpecRepo/DATA_MODEL.md`
6. `SpecRepo/CONSISTENCY.md`
7. `SpecRepo/ARCHITECTURE.md`

If present and relevant to the task, then read:

8. `SpecRepo/SECURITY.md`
9. `SpecRepo/OBSERVABILITY.md`
10. `SpecRepo/TEST_PLAN.md`
11. `SpecRepo/FAILURE_MODES.md`
12. `SpecRepo/SCALING.md`
13. `SpecRepo/API_CONTRACTS.yaml`
14. `SpecRepo/CHANGELOG.md`

## Interpretation Rules

- `SpecRepo/PROBLEM.md` defines problem framing, scope, constraints, and success.
- `SpecRepo/INVARIANTS.md` defines non-negotiable constraints.
- `SpecRepo/REQUIREMENTS.md` defines required behavior.
- `SpecRepo/DATA_MODEL.md` defines entities and lifecycle.
- `SpecRepo/CONSISTENCY.md` defines concurrency and ordering rules.
- `SpecRepo/ARCHITECTURE.md` defines boundaries and design constraints.

## Behavior Rules

- Prefer repository documentation over prompt-only assumptions.
- If a task changes system behavior, update the relevant specification file when appropriate.
- If a required decision is missing from `SpecRepo/`, identify the gap instead of guessing.
- If the specification is incomplete, identify the missing decision instead of guessing.
