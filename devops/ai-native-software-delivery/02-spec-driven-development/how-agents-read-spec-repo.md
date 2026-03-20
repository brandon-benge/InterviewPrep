# How Agents Read SpecRepo

This document explains the purpose of agent instruction files in a repository that uses a `SpecRepo`-style layout.

It is not itself an active instruction file for this repository.

## Why This Document Exists

When people talk about "how an agent reads a repo," they usually mean three separate things:

1. How the agent discovers that governing documentation exists
2. How the agent knows what each spec file means
3. How the agent resolves ambiguity or conflicting information

Those rules do not appear automatically. They usually need to be written into a repository instruction file.

## What Usually Tells an Agent How To Read a Repo

Different coding agents use different instruction files:

| Agent or system | Common repository instruction file |
|---|---|
| Codex | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude | `CLAUDE.md` |

These files are the place where a team would normally define:

- where the spec files live
- which spec files matter most
- what each spec file means
- what to do if code and spec disagree


The template files are here:

- [AGENTS.md template](./templates/agent-instructions/AGENTS.md)
- [GEMINI.md template](./templates/agent-instructions/GEMINI.md)
- [copilot-instructions.md template](./templates/agent-instructions/copilot-instructions.md)
- [CLAUDE.md template](./templates/agent-instructions/CLAUDE.md)
