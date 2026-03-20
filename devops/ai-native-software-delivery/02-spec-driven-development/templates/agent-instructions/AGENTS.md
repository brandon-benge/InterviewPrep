# AGENTS.md Template

Copy this file to the repository root as `AGENTS.md` when you want Codex or other agent systems that support `AGENTS.md` to understand your specification layout.

Replace the placeholders before use.

## Start Here

When a task involves the governed system, read in this order:

1. `<repo-root>/README.md`
2. `<project-docs>/README.md`
3. `<spec-root>/how-agents-read-spec-repo.md`
4. `<project-docs>/reading-path.md`
5. `<project-docs>/glossary.md`
6. `<project-docs>/<core-model-doc>.md`
7. `<spec-root>/spec-repo.md`

## Spec Interpretation Rules

- `PROBLEM.md` defines mission, scope, and success.
- `INVARIANTS.md` defines hard constraints.
- `REQUIREMENTS.md` defines expected behavior.
- `DATA_MODEL.md` defines entities, ownership, and lifecycle.
- `CONSISTENCY.md` defines ordering and concurrency behavior.
- `ARCHITECTURE.md` defines boundaries and design tradeoffs.

## Conflict Rules

- If code conflicts with the written spec, treat the spec as authoritative unless the task clearly updates the spec.
- If two spec files conflict, prefer the more specific file and call out the conflict.
- Do not silently invent missing requirements.

## Working Rule

For this repository, the canonical explanation of the layout lives in:

- `<spec-root>/how-agents-read-spec-repo.md`
