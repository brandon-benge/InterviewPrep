# GitHub Copilot Instructions Template

Copy this file to `.github/copilot-instructions.md` when you want GitHub Copilot to understand your specification layout as part of repository context.

Replace the placeholders before use.

## Read This Material First

When working in this repository, use these files as the primary orientation path:

1. `<repo-root>/README.md`
2. `<project-docs>/README.md`
3. `<spec-root>/how-agents-read-spec-repo.md`
4. `<project-docs>/reading-path.md`
5. `<project-docs>/glossary.md`

## How To Interpret Spec Files

- `PROBLEM.md` defines mission, scope, constraints, and success.
- `INVARIANTS.md` defines hard correctness and safety rules.
- `REQUIREMENTS.md` defines expected behavior.
- `DATA_MODEL.md` defines state, ownership, and lifecycle.
- `CONSISTENCY.md` defines ordering and concurrency semantics.
- `ARCHITECTURE.md` defines system boundaries and tradeoffs.

## Repository Rule

When a concept already has a canonical home in `<project-docs>`, do not re-explain it in full in another file unless the duplication is intentional. Prefer linking to the canonical document.
