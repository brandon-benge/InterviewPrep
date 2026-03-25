# GitHub Copilot Instructions

Copy this file to `.github/copilot-instructions.md` when you want GitHub Copilot to understand your specification layout as part of repository context.

Replace the placeholders before use.

## Read This Material First

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

## How To Interpret Spec Files

- `SpecRepo/PROBLEM.md` defines mission, scope, constraints, and success.
- `SpecRepo/INVARIANTS.md` defines hard correctness and safety rules.
- `SpecRepo/REQUIREMENTS.md` defines expected behavior.
- `SpecRepo/DATA_MODEL.md` defines state, ownership, and lifecycle.
- `SpecRepo/CONSISTENCY.md` defines ordering and concurrency semantics.
- `SpecRepo/ARCHITECTURE.md` defines system boundaries and tradeoffs.

## Repository Rule

Treat `SpecRepo/` as the governing source of truth for system behavior. If required information is missing, identify the gap instead of guessing.
