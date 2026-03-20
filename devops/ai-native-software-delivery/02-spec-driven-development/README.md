# Spec-Driven Development Method

This folder contains the method details behind the broader operating model.

Read this folder when you want to understand how the specification is structured, how validation works, and how production feedback closes the loop.

## Recommended Order

1. [How Agents Read SpecRepo](./how-agents-read-spec-repo.md)
2. [Spec Repo](./spec-repo.md)
3. [Test Generation](./test-generation.md)
4. [Deployment Health Checks](./deployment-health-checks.md)
5. [Templates](./templates/README.md)

## Canonical Concepts in This Folder

- Agent-readable repository guidance: [how-agents-read-spec-repo.md](./how-agents-read-spec-repo.md)
- Spec artifact structure: [spec-repo.md](./spec-repo.md)
- Validation strategy: [test-generation.md](./test-generation.md)
- Runtime evaluation: [deployment-health-checks.md](./deployment-health-checks.md)
- Reusable template set: [templates/README.md](./templates/README.md)

## Folder Purpose

This folder should answer four practical questions:

- What files define the system?
- What order should they be written in?
- How are they validated?
- How do runtime signals change the next version of the spec?
