# Spec-Driven Development Landscape

_Last updated: 2026-03-20_

## Purpose

This document explains how the current landscape of Spec-Driven Development is being defined in practice.

The important framing is that Spec-Driven Development is not yet governed by a single formal standards body. There is no universally accepted global technical standard for how artificial intelligence-readable architectural intent must be written, validated, or enforced. Instead, the landscape is emerging through a mix of:

- platform-level conventions
- specialized workflow tools
- open-source experiments
- research on formal verification and machine-checkable correctness

In that sense, Spec-Driven Development is better understood as an **emerging operating model** than a finalized standard.

---

## Core Thesis

The center of gravity is shifting from:

- tickets as the primary unit of intent
- code as the only real artifact
- documentation as secondary explanation

Toward:

- specifications as executable intent
- repositories as the working memory for humans and artificial intelligence
- code as one output of a larger spec-governed delivery loop

This is why the phrase **"intent is the new source code"** resonates in artificial-intelligence-native delivery discussions. It does not mean code stops mattering. It means the controlling artifact increasingly becomes the written definition of constraints, expected behavior, architecture, and correctness.

---

## What Is Actually Being Standardized

When people talk about Spec-Driven Development "standards" today, they usually mean one or more of the following:

### 1. Standard artifact shapes

Common files are starting to recur across teams and tools:

- `PROBLEM.md`
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `INVARIANTS.md`
- `CONSISTENCY.md`
- `API_CONTRACTS.yaml`
- `TEST_PLAN.md`
- `SECURITY.md`

The exact filenames vary, but the pattern is stabilizing: artificial intelligence systems perform better when intent, constraints, interfaces, and correctness rules are separated into explicit documents stored directly in the repository.

### 2. Standard workflow stages

A recognizable lifecycle is also emerging:

1. Define the problem and constraints.
2. Convert that into structured requirements and architecture.
3. Use artificial intelligence to plan against the spec.
4. Generate code and tests against the spec.
5. Validate changes against invariants and contracts.
6. Review diffs with traceability back to the spec.
7. Update the spec when production reality changes.

This is the operational layer of Spec-Driven Development: the spec is not written once and forgotten; it governs the whole loop.

### 3. Standard enforcement mechanisms

The most important shift is not documentation format. It is enforcement.

Modern Spec-Driven Development efforts increasingly assume that specs must be:

- structured enough for software systems and agents to use
- structured enough for traceability
- testable enough for validation
- strict enough to block unsafe changes

That is where invariants, contract-first design, policy checks, evaluation systems, and formal methods start to matter.

---

## Who Is Defining the Landscape

The current landscape is being shaped by three overlapping groups.

## Organizations Actively Shaping the Pattern

The field is still early, so it is more accurate to say these organizations are **shaping** or **popularizing** this style than to say they have all agreed on one exact `SpecRepo` standard. Even so, several public examples are important.

### GitHub

GitHub is one of the clearest public drivers of this space through Spec Kit, its public toolkit for Spec-Driven Development.

What GitHub is clearly standardizing in practice:

- a repository-based workflow
- a persistent project constitution
- stepwise movement from specification to plan to tasks to implementation
- analysis steps that check consistency and coverage before implementation

Why it matters:

- GitHub has made the strongest public case that specifications should become executable working artifacts rather than temporary planning notes.
- Its constitution concept is especially influential because it gives agents standing project rules instead of one-time prompt instructions.
- Its workflow reinforces the idea that requirements and constraints should guide implementation continuously, not just at the beginning.

### Augment Code

Augment Code is shaping the market from a different angle. Its public emphasis is less about publishing one canonical spec folder and more about building high-quality context across large codebases, services, and pull requests.

What Augment is clearly emphasizing:

- whole-codebase understanding
- cross-repository and cross-service context
- retrieval of relationships, contracts, and invariants before analysis
- better code review and implementation quality through stronger contextual grounding

Why it matters:

- This supports the same underlying Spec-Driven Development direction: artificial intelligence systems need durable architectural context, not just local file snippets.
- Augment's public material strongly supports the importance of data relationships, interface assumptions, concurrency behavior, and invariants in cross-file reasoning.
- I am inferring from its product direction that this makes documents like `DATA_MODEL.md`, `CONSISTENCY.md`, and invariant-focused specs more valuable, even though Augment does not publicly present one exact `SpecRepo` template as the only standard.

### Tessl

Tessl is one of the strongest public advocates for treating the spec as a long-lived governing artifact. Its public material explicitly frames Spec-Driven Development as a way to give agents both the "what" and the "how" before coding.

What Tessl is clearly emphasizing:

- long-term specs stored in the codebase
- spec-driven workflows before implementation
- guardrails and tests paired with specs
- reusable usage specs that help agents use libraries and frameworks correctly

Why it matters:

- Tessl is pushing the market toward the idea that the maintained artifact may increasingly be the specification itself, with code generated and regenerated from it.
- Its registry model also extends the idea of specification beyond product requirements into dependency usage, framework behavior, and library correctness.
- This is one of the clearest examples of the shift from "documentation about the system" to "instructions the system is built from."

### Kiro and Similar Structured Spec Tools

Kiro provides a concrete example of how this pattern is becoming operational in tooling. Its public workflow uses a three-step sequence of requirements, design, and tasks.

What Kiro is clearly emphasizing:

- requirements-first or design-first workflows
- structured requirements written in a testable pattern
- design documents that include architecture, data models, and interaction flow
- task generation only after the earlier artifacts are reviewed

Why it matters:

- Kiro shows that the market is converging on repeatable spec artifacts, even when the exact filenames differ from a `SpecRepo` layout.
- It also shows that structured requirements are becoming machine-usable development inputs rather than static documentation.
- In practice, this supports the same broader movement as `PROBLEM.md` through `ARCHITECTURE.md`, even if the file names are different.

Community projects such as SpecMind and other open-source "vibe coding" experiments also matter here, although the public landscape is less stable and less standardized than the better-documented platform examples. Their importance is that they push toward machine-checkable constraints, automatic rejection of unsafe changes, and specifications that behave more like executable logic than passive notes.

### Thoughtworks

Thoughtworks is important less as a seller of one exact file structure and more as a respected engineering voice that is publicly tracking Spec-Driven Development as an emerging practice.

What Thoughtworks is clearly emphasizing:

- structured functional specifications for artificial-intelligence-assisted development
- source-controlled architectural records and decisions
- architecture models that remain useful as systems evolve
- continued human judgment around quality, maintainability, and delivery discipline

Why it matters:

- Thoughtworks helps connect newer Spec-Driven Development practices with older architecture discipline rather than treating them as unrelated trends.
- Its long-standing support for source-controlled architectural records makes it a natural bridge into repository-based specification systems.
- Its recent public writing also confirms that the field is still emerging, which is an important corrective to overly certain vendor narratives.

## 1. Platform Giants: infrastructure and default workflow patterns

Large developer platforms define the environment in which artificial intelligence coding systems operate. Their influence is strong because they control where planning, code generation, pull requests, review, and automation already happen.

### What they contribute

- repository-based workflows
- pull-request-centered review loops
- conventions for agent instructions and persistent context
- the idea that artificial intelligence should work from durable project artifacts, not just a chat prompt

### Why they matter

If a platform becomes the default environment for artificial-intelligence-assisted engineering, its workflow assumptions can become a de facto standard even without formal ratification.

### How to interpret GitHub's role

GitHub-style spec-centered workflows matter less because they are an official standards body and more because they sit at the control point of modern software delivery:

- issue and repo context
- code generation
- pull request review
- continuous integration and continuous delivery integration
- policy and security checks

Concepts like a repository-level "constitution" or standing rule set are influential because they turn vague engineering norms into durable instructions that every agent invocation can inherit.

The broader pattern is more important than any single branded framework:

- persistent project rules
- explicit architectural boundaries
- policy-aware code generation
- review artifacts that trace changes back to intent

---

## 2. Specialized Tool Creators: workflow formalization

Specialized startups and tool builders are defining the middle layer: how a spec is structured closely enough that artificial intelligence can build from it without drifting.

### What they contribute

- opinionated spec folder structures
- contract-first generation workflows
- explicit invariants and machine-verifiable constraints
- traceability from requirement to implementation to test

### Why they matter

These vendors are often more aggressive than the platforms. They are not just saying "put docs in the repo." They are saying:

- define the contract first
- define invariants before implementation
- do not allow code generation to outrun the governing spec

This is a meaningful escalation from ordinary documentation practices.

### Common patterns from this group

- `INVARIANTS.md` as a first-class artifact
- `DATA_MODEL.md` and interface contracts before implementation
- generation gated by policy, tests, or approval
- architectural drift detection
- spec-to-code traceability as part of pull request review

---

## 3. Research and formal methods groups: correctness logic

Academic and research communities are shaping the deepest technical question in Spec-Driven Development:

**How can an artificial intelligence system prove that the code it produced actually satisfies the requested behavior?**

### What they contribute

- postcondition inference
- property checking
- constraint solving
- program verification techniques
- machine-checkable behavioral guarantees

### Why they matter

Without this layer, Spec-Driven Development can collapse into "better prompting plus nicer docs." Research pushes the field toward stronger guarantees:

- not just "the artificial intelligence followed the instructions"
- but "the implementation can be checked against the intended behavior"

In other words, research groups are defining the difference between:

- spec-informed generation
- spec-governed correctness

That distinction will likely matter a great deal as these systems move into regulated, safety-critical, or financially sensitive domains.

---

## Four Layers of the Emerging Standard

The landscape is easiest to understand as four layers rather than one standard.

| Layer | What Is Being Standardized | Primary Drivers | Why It Matters |
|---|---|---|---|
| Intent Layer | Problem statements, requirements, architecture, invariants | Architects, engineering leads, vendor templates | Gives artificial intelligence durable governing context |
| Workflow Layer | Plan-build-validate-review-update loop | Platforms and specialized tools | Makes the spec operational, not decorative |
| Enforcement Layer | Tests, policy checks, contract validation, review gates | Continuous integration and continuous delivery systems, policy engines, evaluation tools | Prevents drift between spec and code |
| Logic Layer | Proof, inference, behavioral validation, formal reasoning | Research and formal methods communities | Makes correctness claims defensible |

Most organizations today are only partially mature across these layers. Many have adopted the intent layer. Fewer have strong enforcement. Very few have formal proof-like validation in day-to-day engineering.

---

## The Most Important Emerging Concepts

### Constitution

A constitution is a persistent ruleset that artificial intelligence must follow on every change. It acts like standing engineering law.

Typical content:

- forbidden changes
- security and compliance requirements
- architectural boundaries
- style and review rules
- escalation conditions for risky modifications

This matters because it prevents every prompt from having to restate critical constraints.

### Invariants

Invariants define what must always remain true regardless of implementation detail.

Examples:

- no duplicate external side effects
- state transitions must be valid
- authorization must be enforced before data access
- ordering guarantees must hold per entity

This matters because invariants are one of the cleanest bridges between architecture, testing, runtime checks, and artificial intelligence guardrails.

### Contract-first generation

Contract-first generation means interfaces, schemas, and behavioral requirements are defined before code generation proceeds.

This matters because it reduces ambiguity and narrows the space in which artificial intelligence is allowed to improvise.

### Traceability

Traceability means every code change can be mapped back to:

- a problem statement
- a requirement
- an invariant
- an architectural decision
- a validation artifact

This matters because review quality drops quickly when artificial intelligence can generate large amounts of code without a clear chain of intent.

### Spec updates from reality

A Spec-Driven Development workflow is incomplete if production lessons never flow back into the spec.

This matters because a stale spec becomes a liability. In practice, the strongest teams treat the spec as a living operational artifact rather than a design-time deliverable.

---

## Where the Landscape Is Still Unsettled

Despite the momentum, several parts of the field are not standardized yet.

### File naming is not standardized

The concepts are converging faster than the filenames. One team may use `RULES.md`; another may use `CONSTITUTION.md`; another may embed those rules in agent config.

### Enforcement depth varies widely

Some teams only use specs for better prompting. Others use them to gate pull requests, generate tests, or block policy violations. These are very different maturity levels.

### Formal verification is not mainstream yet

The industry talks more about correctness than it can currently guarantee. In many cases, "verified" still means:

- tested
- reviewed
- evaluated against scenarios

Not mathematically proven.

### Vendor narratives are ahead of shared standards

Tool vendors often present their preferred structure as if it were the structure. The market is still early enough that multiple shapes are competing:

- markdown-first specs
- schema-first specs
- policy-as-code overlays
- graph-based architecture representations
- hybrid human-readable plus software-readable repositories

---

## What Seems To Be Becoming Consensus

Even though the field is still unsettled, several ideas appear to be converging into practical consensus.

### 1. Repo-native context beats prompt-only context

Teams increasingly want artificial intelligence to read the actual repository, design docs, contracts, and rules instead of relying on one-time chat instructions.

### 2. Written intent must be durable

Specs need to persist across sessions, contributors, and agent runs. If the rules only exist in a prompt, they are too fragile.

### 3. Invariants are more valuable than generic documentation

General prose is helpful, but explicit invariants are disproportionately valuable because they can drive tests, guardrails, and runtime evaluation.

### 4. Human review shifts upward

Humans spend less time typing boilerplate code and more time evaluating:

- correctness
- architecture
- risk
- boundary conditions
- whether the implementation still matches the governing intent

### 5. The spec must participate in the delivery loop

A spec that does not influence planning, generation, testing, and release decisions is still just documentation.

---

## Mapping This Back to SpecRepo

Your `SpecRepo` model fits the direction of the market well because it separates the most important forms of intent:

- `PROBLEM.md` defines scope and success
- `INVARIANTS.md` defines non-negotiable truths
- `REQUIREMENTS.md` defines expected capabilities
- `DATA_MODEL.md` defines state and ownership
- `CONSISTENCY.md` defines concurrency and ordering semantics
- `ARCHITECTURE.md` defines system shape and tradeoffs

This is not only a documentation scheme. It is a governance scheme for artificial-intelligence-assisted delivery.

In practical terms, `SpecRepo` sits at the intersection of all three forces above:

- platform-style execution directly from the repository
- tool-driven structured workflow
- research-driven correctness thinking

That makes it a credible framing for how Spec-Driven Development is likely to solidify in practice.

---

## Suggested Summary Position

If you want a concise way to describe the current state of the field, this is a defensible formulation:

> Spec-Driven Development is not yet a single formal standard. It is an emerging software delivery model shaped by platform conventions, specialized artificial intelligence workflow tools, open-source experiments, and formal methods research. The common direction is clear: repositories are becoming the durable home of architectural intent, invariants, and constraints, and artificial intelligence systems are increasingly expected to generate, validate, and review code against that intent rather than against tickets alone.

---

## Bottom Line

The landscape of Spec-Driven Development is being defined from the bottom up.

- Platforms are defining the infrastructure and default workflows.
- Specialized tools are defining the artifact structure and enforcement model.
- Research groups are defining how correctness can eventually be proven rather than merely suggested.

The likely end state is not a single markdown template. It is a new software delivery discipline where:

- intent is explicit
- constraints are durable
- code is traceable
- validation is automated
- humans remain accountable for correctness and risk

That is the real shape of the emerging Spec-Driven Development standard.
