# Spec-Driven Development Method

This folder contains the method details behind the broader operating model.

Read this folder when you want to understand how the specification is structured, how validation works, and how production feedback closes the loop.

## Recommended Order

1. [How Agents Read SpecRepo](./how-agents-read-spec-repo.md)
2. [Spec Repo](./spec-repo.md)
3. [Canonical Service Catalog](./canonical-service-catalog.md)
4. [Test Generation](./test-generation.md)
5. [Deployment Health Checks](./deployment-health-checks.md)
6. [Templates](./templates/README.md)

## Canonical Concepts in This Folder

- Agent-readable repository guidance: [how-agents-read-spec-repo.md](./how-agents-read-spec-repo.md)
- Spec artifact structure: [spec-repo.md](./spec-repo.md)
- Cross-repo component and dependency mapping: [canonical-service-catalog.md](./canonical-service-catalog.md)
- Validation strategy: [test-generation.md](./test-generation.md)
- Runtime evaluation: [deployment-health-checks.md](./deployment-health-checks.md)
- Reusable template set: [templates/README.md](./templates/README.md)

## Folder Purpose

This folder should answer five practical questions:

- What files define the system?
- What order should they be written in?
- How are repositories, components, owners, and dependencies mapped?
- How are they validated?
- How do runtime signals change the next version of the spec?
