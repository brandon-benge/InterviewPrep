# Glossary

## AI-Native Software Delivery

A software delivery model in which written intent, constraints, and evaluation loops guide planning, implementation, validation, and release, with artificial intelligence handling more of the execution work.

## Spec-Driven Development

A development approach in which specifications do not only describe the system. They actively govern planning, implementation, testing, review, release, and iteration.

## Spec-First

A design approach that defines interfaces, architecture, and data shape before implementation begins. It is narrower than Spec-Driven Development because it mainly addresses the design phase.

## SpecRepo

A repository-based set of files that captures the problem, requirements, invariants, data model, consistency rules, and architecture in a durable format that both humans and artificial intelligence can use.

## Constitution

A persistent project ruleset that applies to every change. It defines standing constraints such as forbidden actions, review rules, security expectations, and architectural boundaries.

## Invariant

A condition that must always remain true. Invariants are useful because they can drive architecture, testing, guardrails, and production evaluation.

## Guardrails

Automated checks or policies that prevent changes from violating scope, safety rules, quality thresholds, or governance requirements.

## Evaluation Engine

The part of the workflow that interprets deployment and runtime signals, applies deterministic checks, and summarizes the results for humans.

## Pull Request as Review Artifact

The idea that the pull request becomes the main human review surface, with traceability back to the spec, tests, risks, and reasoning.

## Continuous Loop

The repeating cycle of intent, specification, planning, implementation, validation, release, evaluation, and spec updates.
