# Agentic Software Development & Evaluation / Observability Landscape

_Last updated: 2026-03-19_

## Purpose

This document focuses on the two most important implementation layers for the workflow described in [AI-Native Software Delivery System](../01-core-model/ai-native-software-delivery.md):

1. **Agentic Software Development** — projects that help engineers plan, code, review, and iterate on changes.
2. **Evaluation / Observability** — projects that help engineers trace, evaluate, debug, and gate deployments.

It also includes short summaries of:
- **Protocols / Standards** (critical emerging layer)
- **Core Agent Frameworks** (foundation layer)

## How to read the data

- **Public adoption proxy** = GitHub stars, forks, notable public usage/download signals, and release cadence.
- **Projected adoption (12–18 mo)** = directional score from **1–5** where **5** means “very likely to become a standard part of modern agentic SDLC stacks.”
- **Contributors** = contributor count visible on public GitHub pages when reliably exposed.
- **Branches** = GitHub’s public HTML did **not reliably expose total branch counts** during collection. This doc records **active branch visibility** instead (for most repos: default branch + at least 5 active branches were visible, often with a “View more branches” link).
- **PR trend proxy** = open PR count plus release cadence / public activity; this is a proxy, not a perfect trend line.

---

## 1) Summary: Protocols / Standards (critical emerging layer)

### Model Context Protocol (MCP)
- **What it is:** an open standard for connecting AI apps to external tools, data sources, and workflows.
- **Why it matters to `ai-native-software-delivery.md`:** this is the cleanest way to standardize your `ToolExecutor`, `Retriever`, and external context/tool integrations.
- **Role mapping:**
  - `PlannerAgent` / `CoderAgent` → tool access
  - `Retriever` → docs, repos, search, datasets
  - `EvaluationEngine` → structured access to observability/eval systems
- **Why it matters for free/local stacks:** MCP makes it easier to combine local LLMs with local tools and self-hosted services.

### Agent2Agent (A2A)
- **What it is:** an open protocol for agent-to-agent communication and collaboration.
- **Why it matters to `ai-native-software-delivery.md`:** if your system truly uses multiple agents (Planner, Coder, Test, Evaluator), A2A is one of the clearest standards for inter-agent collaboration.
- **Role mapping:**
  - `PlannerAgent` ↔ `CoderAgent`
  - `TestAgent` ↔ `EvaluationEngine`
  - `SecurityAgent` ↔ `Guardrails`

### OpenTelemetry (OTel)
- **What it is:** the de facto open observability standard for traces, metrics, and logs.
- **Why it matters to `ai-native-software-delivery.md`:** Step 9 needs structured telemetry; OTel is the best common substrate for traces, metrics, logs, and deployment metadata.
- **Role mapping:**
  - `EvaluationEngine` → consumes normalized telemetry
  - `Guardrails` → gates releases on health signals
  - `Human Review` / `Release` → audit trail and deployment health checks

---

## 2) Summary: Core Agent Frameworks (foundation layer)

### LangChain / LangGraph
- Strong for tool use, orchestration, retrieval, memory, and graph/stateful workflows.
- Best fit when you want to model `PlannerAgent`, `Retriever`, `ToolExecutor`, and looped execution explicitly.
- LangGraph is especially relevant when you want deterministic state transitions, retries, persistence, and human-in-the-loop review.

### AutoGen
- Strong multi-agent programming model with mature mindshare and broad community recognition.
- Best fit when you want explicit agent roles and multi-agent collaboration patterns.
- Useful for prototyping the orchestration logic in `ai-native-software-delivery.md`, especially Step 3 and Step 4.

### CrewAI
- Good for role-based multi-agent teams and tool-driven workflows.
- Best fit for a straightforward PM / Architect / Engineer / Reviewer mental model.
- Easier to explain to teams that want explicit agent personas.

### LlamaIndex / Haystack
- Not software-delivery agents by themselves, but important for repo search, docs search, knowledge retrieval, and RAG.
- Best fit when your `Retriever` needs access to specifications, internal docs, code examples, or web-acquired context.

---

## 3) Projects to watch: Agentic Software Development (very important layer)

## Evaluation criteria used here
- Can it help with spec-driven delivery?
- Can it run with free / local models?
- Can it fit the agent roles in `ai-native-software-delivery.md`?
- Does it show strong public engagement / contributor energy?

### Agentic SD projects comparison

| Project | License | Primary role in your workflow | Public adoption proxy | Projected adoption (1–5) | Contributors | Branch visibility | PR trend proxy | Free / local LLMs? | Web / RAG / crawling fit | Best-fit agents from `ai-native-software-delivery.md` |
|---|---|---|---:|---:|---:|---|---|---|---|---|
| **OpenHands** | MIT (core); enterprise features source-available | End-to-end software agent platform for coding, issue work, and repo automation | 69.4k stars / 8.7k forks | 5 | Not reliably exposed in public HTML at capture time | Default + 5 active visible, “View more branches” present | 174 open PRs, 100 releases | **Yes** — supports local LLMs and provider guides including local LLMs with SGLang/vLLM | Partial in core; strongest when paired with MCP/search/retrieval tooling | Planner, Coder, PR Artifact, part of Human Review automation |
| **Continue** | Apache 2.0 | Source-controlled AI checks and repo-native agents on pull requests | 32k stars / 4.3k forks | 5 | 457 | Default + 5 active visible, “View more branches” present | 63 open PRs, 806 releases | **Yes** — strong Ollama and self-hosted model support | Strong repo/context fit; pair with external RAG/crawlers for broader retrieval | Guardrails, Test, PR review automation, AI checks |
| **Cline** | Apache 2.0 | IDE-native autonomous coding agent with browser/command execution | 59.2k stars / 6k forks / used by 3.3k | 5 | 305 | Default + 5 active visible, “View more branches” present | 293 open PRs, 243 releases | **Yes** — supports Ollama / LM Studio and many providers | **Yes (browser + MCP ecosystem)** for web-assisted workflows | Coder, Refactor, Security-adjacent checks, human-in-the-loop coding |
| **Aider** | Apache 2.0 | Git-centric terminal coding assistant / pair programmer | 42.1k stars / 4.1k forks | 5 | Not reliably exposed in public HTML at capture time | Branch total not exposed; repo shows Branches tab | 266 open PRs, active commit history, many releases | **Yes** — works with local models including Ollama and OpenAI-compatible local APIs | Partial — supports web pages and repo maps; pair with separate crawler/RAG for more | Coder, Refactor, PR preparation, local coding loop |
| **SWE-agent** | MIT | Issue-to-fix research-grade software engineering agent | 18.8k stars / 2k forks | 4 | Not reliably exposed in public HTML at capture time | Branch total not exposed publicly at capture time | 1 open PR, 10 releases; project itself recommends mini-SWE-agent going forward | **Yes/partial** — works with model of choice, but strongest in research/benchmark setups | Limited in core; pair with external retrieval if needed | Planner + Coder in issue-driven workflows |

### Notes on the Agentic SD layer

#### OpenHands
- OpenHands is the closest open-source project to a full “AI-driven development” operating model: SDK, CLI, local GUI, cloud, and enterprise variants in one ecosystem.
- It already maps well to `Plan → Build Loop → PR Artifact`, and its docs explicitly cover local LLMs.
- Best suited when you want a central software agent runtime rather than only an IDE assistant.

#### Continue
- Continue is especially interesting because it moves checks and agent behavior **closer to the repo**; the repo itself can define checks in markdown under `.continue/checks/`.
- That aligns strongly with your desire to move away from ticket-first delivery and closer to repo-native specs / policies.
- Continue is one of the best fits for turning `SpecRepo` and `Guardrails` into enforceable repo policy.

#### Cline
- Cline is one of the strongest IDE-native agents for engineers who still want explicit human control while getting browser use, terminal use, and file edits.
- It pairs well with `Human Review` because it keeps a clear permissioned interaction loop.
- Cline also has strong practical local-model support through Ollama / LM Studio.

#### Aider
- Aider is one of the cleanest “agentic coding loop” tools for people who want local / terminal / git-first workflows.
- It is especially good if your engineers want lightweight AI-native development without adopting a full agent platform.
- Strong fit for surgical code changes, refactors, test addition, and local model experimentation.

#### SWE-agent
- SWE-agent remains important because it set the pattern for issue-driven software engineering agents, and it is tied directly to SWE-bench research.
- That said, the project itself now recommends mini-SWE-agent for forward use, which is an important maturity signal.
- Best viewed as a research / benchmark-influential project rather than the most operationally mature day-to-day engineering platform.

---

## 4) Projects to watch: Evaluation / Observability (very important layer)

### Evaluation / observability projects comparison

| Project | License | Primary role in your workflow | Public adoption proxy | Projected adoption (1–5) | Contributors | Branch visibility | PR trend proxy | Free / local / self-hosted? | Best-fit steps from `ai-native-software-delivery.md` |
|---|---|---|---:|---:|---:|---|---|---|---|
| **Langfuse** | MIT | Tracing, evals, prompt/version management, datasets, debugging | 23.4k stars / 2.4k forks | 5 | 158 | Branch total not exposed in public HTML at capture time | 273 open PRs, 541 releases | **Yes** — self-host in minutes; local Docker / VM / K8s | Step 6 review bundle, Step 9 evaluation, artifact traceability |
| **Arize Phoenix** | Apache 2.0 | Open-source AI observability + evaluation + OTel-native tracing | 8.9k stars / 768 forks + 2.5M+ monthly downloads on website | 5 | Not reliably exposed in scraped GitHub HTML at capture time | Branch total not exposed publicly at capture time | 52 open PRs, rapid release cadence | **Yes** — runs locally, in notebooks, containers, or cloud; fully open-source and self-hostable | Step 9 evaluation, deployment health checks, tracing |
| **Promptfoo** | Apache 2.0 | Evals, red teaming, vulnerability scanning, CI/CD checks for prompts/agents/RAG | 17.6k stars / 1.5k forks | 5 | Not reliably exposed in scraped GitHub HTML at capture time | Default + 5 active visible, “View more branches” present | 194 open PRs, 398 releases | **Yes** — open source CLI, supports comparing GPT/Claude/Gemini/Llama and RAGs | Step 4 validation, Step 6 review bundle, Step 9 experiments |
| **DeepEval** | Apache 2.0 | Open-source LLM evaluation framework, pytest-like for LLM apps | 14.2k stars / 1.3k forks | 4 | Not reliably exposed in public HTML at capture time | Branch total not exposed publicly at capture time | 38 open PRs | **Yes** — supports local NLP models / local-machine eval components | Step 4 validation, Step 9 correctness / plan / tool-use evaluation |
| **OpenTelemetry** | Apache 2.0 | Vendor-neutral telemetry substrate for metrics, traces, logs | Industry-standard adoption across 90+ vendors | 5 | N/A (spec/ecosystem rather than one repo here) | N/A | N/A | **Yes** — fully open and vendor-neutral | Step 8 rollout telemetry, Step 9 EvaluationEngine input |

### Notes on Evaluation / Observability layer

### Why licenses matter
- License type directly affects whether teams can run the stack locally, modify it, embed it in CI/CD, and avoid vendor lock-in.
- MIT and Apache 2.0 are generally the best fit for local-first, extensible, automation-heavy software delivery systems.
- Source-available or proprietary layers may still be useful, but they should be evaluated carefully against long-term portability and governance requirements.

#### Langfuse
- Langfuse is one of the closest open-source matches to your `EvaluationEngine + artifacts + traceability` vision.
- It covers observability, evaluations, datasets, prompt/version management, and integrates with many agent frameworks.
- It also fits your “free software / local-first” requirement because it is self-hostable and explicitly supports local deployment.

#### Phoenix
- Phoenix is strongest when you want OTel-aligned tracing plus evaluation in one open-source platform.
- It maps especially well to the deployment health-check model you described: normalize telemetry, derive signals, evaluate, then summarize.
- Phoenix also explicitly supports local and containerized operation, which makes it good for labs and privacy-conscious teams.

#### Promptfoo
- Promptfoo is one of the best practical tools today for making evals and red-teaming part of CI.
- It is especially useful if you want `Guardrails` and `SecurityAgent` to have concrete eval/security artifacts before release.
- It is also one of the best bridges between prompt/app testing and policy-style deployment gating.

#### DeepEval
- DeepEval is particularly interesting because it already thinks in terms engineers understand: pytest-like evaluation for LLM systems.
- Its agentic metrics (task completion, tool correctness, plan adherence, step efficiency) line up well with your Step 9 needs.
- It is a strong fit when you want evaluation to become a first-class engineering discipline rather than a vague post-hoc check.

---

## 5) Free local LLMs, web crawling, and RAG: what is realistic today?

### Local / free model support today

**Strong local-model support**
- OpenHands — local LLM guides exist, including SGLang / vLLM and recommended local coding models.
- Aider — supports Ollama and other OpenAI-compatible local model endpoints.
- Continue — strong Ollama and self-hosted model guides.
- Cline — supports local models via Ollama / LM Studio.
- DeepEval — can use local-machine NLP models for some evaluation flows.
- Langfuse / Phoenix — self-hostable platforms that can sit on top of local or cloud model stacks.

### Web crawling / RAG support today

For your workflow, the cleanest answer is:
- **agent platforms** rarely provide best-in-class crawling by themselves,
- but they pair very well with **MCP servers, retrieval frameworks, and crawler utilities**.

Recommended open-source support layer:
- **Crawl4AI** — turns web content into LLM-ready Markdown for RAG, agents, and pipelines.
- **Firecrawl** — crawls and extracts structured web data for agents and apps; also has an MCP server.
- **LlamaIndex / Haystack** — strong retrieval and RAG orchestration layers that can sit under `Retriever`.

This means a practical free/open stack can be:

```text
Local model (Ollama / vLLM / SGLang)
+ Agent runtime (OpenHands / Continue / Cline / Aider)
+ Retrieval (LlamaIndex / Haystack)
+ Crawling (Crawl4AI / Firecrawl)
+ Evaluation / observability (Langfuse / Phoenix / Promptfoo / DeepEval)
```

---

## 6) Mapping these projects back to `ai-native-software-delivery.md`

| `ai-native-software-delivery.md` role / step | Best-fit open-source projects |
|---|---|
| **Step 3 – Plan / Orchestration** | LangGraph, AutoGen, CrewAI, OpenHands |
| **Step 4 – Build Loop / CoderAgent** | OpenHands, Continue, Cline, Aider, SWE-agent |
| **Step 4 – TestAgent / Guardrails** | Continue, Promptfoo, DeepEval, Promptfoo + CI |
| **Step 4 – SecurityAgent / RefactorAgent** | Continue checks, Promptfoo, SonarQube / CodeQL integrations, Aider lint/test loop |
| **Step 5 – PR Artifact** | OpenHands, Continue, Cline, Aider |
| **Step 6 – Human Review bundle** | Continue, Langfuse, Promptfoo, Phoenix |
| **Step 8 – Release / rollout telemetry** | OpenTelemetry, Phoenix, Langfuse |
| **Step 9 – EvaluationEngine** | Phoenix, Langfuse, DeepEval, Promptfoo |
| **Retriever / ToolExecutor** | MCP, LlamaIndex, Haystack, Crawl4AI, Firecrawl |

---

## 7) Recommended reference stacks

### A. Most practical open-source stack for a software team today
- **Repo/PR checks:** Continue
- **Interactive coding agent:** Cline or Aider
- **Full software agent runtime:** OpenHands
- **Eval / tracing:** Langfuse or Phoenix
- **Policy / red-team / CI evals:** Promptfoo
- **Retrieval / crawling:** LlamaIndex + Crawl4AI (or Firecrawl)
- **Standards:** MCP + OpenTelemetry

### B. Best local-first / privacy-first stack
- **Models:** Ollama / vLLM / SGLang
- **Coding loop:** Aider or Cline
- **Agent platform:** OpenHands (local GUI / SDK)
- **Tracing/evals:** self-hosted Langfuse or Phoenix
- **Crawling / RAG:** Crawl4AI + Haystack or LlamaIndex
- **Standards:** MCP + OTel

### C. Best research-heavy / benchmark-driven stack
- **Issue-to-fix research:** SWE-agent / mini-SWE-agent
- **Orchestration:** LangGraph / AutoGen
- **Evaluation:** DeepEval + Phoenix
- **Tracing:** OTel + Phoenix / Langfuse

---

## 8) Bottom line

### Most important open-source projects for **Agentic Software Development**
1. **OpenHands**
2. **Continue**
3. **Cline**
4. **Aider**
5. **SWE-agent / mini-SWE-agent**

### Most important open-source projects for **Evaluation / Observability**
1. **Langfuse**
2. **Phoenix**
3. **Promptfoo**
4. **DeepEval**
5. **OpenTelemetry** (as the telemetry substrate)

### Most important standards / foundations to keep watching
1. **MCP**
2. **A2A**
3. **LangGraph**
4. **AutoGen**
5. **CrewAI**

---

## Sources used

- LangChain repository / docs
- OpenHands repository and docs
- Continue repository and Ollama / self-host docs
- Cline repository and local-model docs
- Aider repository and local-model docs
- SWE-agent repository
- Langfuse repository and docs
- Phoenix repository and docs
- Promptfoo repository
- DeepEval repository
- MCP spec / docs
- A2A project / protocol pages
- OpenTelemetry docs
- Crawl4AI and Firecrawl repositories
