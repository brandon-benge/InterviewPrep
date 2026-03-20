# GEMINI.md Template

Copy this file to the repository root as `CLAUDE.md` when you want Claude CLI to understand your specification layout without repeating it in every prompt.

Replace the placeholders before use.

## Read Order

1. `<repo-root>/README.md`
2. `<project-docs>/README.md`
3. `<spec-root>/how-agents-read-spec-repo.md`
4. `<project-docs>/<core-model-doc>.md`
5. `<spec-root>/spec-repo.md`

## Interpretation Rules

- `PROBLEM.md` defines problem framing, scope, and success.
- `INVARIANTS.md` defines non-negotiable constraints.
- `REQUIREMENTS.md` defines required behavior.
- `DATA_MODEL.md` defines entities and lifecycle.
- `CONSISTENCY.md` defines concurrency and ordering rules.
- `ARCHITECTURE.md` defines boundaries and design constraints.

## Behavior Rules

- Prefer repository documentation over prompt-only assumptions.
- If a task changes system behavior, update the relevant specification file when appropriate.
- If the specification is incomplete, identify the missing decision instead of guessing.
