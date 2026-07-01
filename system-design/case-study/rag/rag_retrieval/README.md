# RAG Retrieval Design

This folder separates RAG retrieval into three views that connect through explicit handoff contracts:

| Document | Owns | Boundary With The Other Docs |
|---|---|---|
| [AI Gateway Internal Design](./ai-gateway-internal-design.md) | AuthN/AuthZ, policy lookup, prompt decision, response validation, repair/block/return decisions, model routing, observability | Receives application or RAG prompt packages; returns policy decisions, sanitized requests, validated responses, and audit metadata. It does not execute retrieval. |
| [End-to-End RAG System Design](./end-to-end-rag-system-design.md) | RAG Orchestrator, retrieval tools, Retrieval Coordinator, Reranker, Context Assembly, Prompt Builder, validation context | Receives safe query, identity, authorization filters, allowed tools, and citation requirements from the gateway. Returns a final prompt package and citation map to the gateway. |
| [Advanced Multi-Agent Retrieval Design](./advanced-multi-agent-retrieval-design.md) | Router Agent, Planner Agent, Query Rewrite Agent, Document Agent, Structured Data Agent, Web Agent, Citation Agent | Enters after gateway prompt approval and exits as normalized retrieval candidates or a standard prompt package that the end-to-end RAG path can consume. |

## Ownership Model

| Component | Owns | Does Not Own |
|---|---|---|
| Application / Agent Client | Product workflow, user intent, requested action, UI behavior | Model provider selection, final safety decision, global AI policy, retrieval internals |
| AI Gateway / LLM Gateway | AuthN/AuthZ boundary, policy lookup, guardrails, budget, model/tool routing, response validation, audit | Retrieval ranking, chunking strategy, domain-specific query planning, vector/BM25/graph execution |
| Policy Engine | Tenant/app/user/model/tool/data constraints | Runtime risk scoring or final allow/block decisions by itself |
| Deterministic Rules / Decision Engine | Final prompt and response decisions using policy plus rule/classifier/validator signals | Semantic retrieval, model generation |
| RAG Orchestrator | Retrieval plan, retrieval tool selection, query rewriting, retry strategy, retrieval fallback | Enterprise AI policy enforcement, final model invocation |
| Retrieval Tools | Authorized data access for vector, keyword, graph, SQL, and approved web sources | Final prompt assembly, policy override, response approval |
| Retrieval Coordinator | Merge, dedupe, normalize, and select authorized candidates from retrieval tools | AuthN/AuthZ, model routing |
| Reranker | Relevance ordering of candidate evidence | Security authorization or policy override |
| Context Assembly | Token budgeting, evidence packaging, citation metadata preservation | Deciding if a user is allowed to see data |
| Prompt Builder | Prompt template, context insertion, citation map, model instructions | Direct LLM calls, policy enforcement after generation |
| Multi-Agent Retrieval Layer | Routing, planning, query decomposition, specialized source retrieval, provenance collection | Global policy, direct model bypass, final response approval |
| LLM | Draft answer generation | Data access, authorization, source-of-truth validation |
| Validation Pipeline | Output schema, safety, grounding, citation validity, policy-compliance signals | Retrieval query execution or final ownership of gateway policy |
| Observability / Audit | Logs, traces, metrics, costs, policy decisions, validation outcomes | Business workflow ownership |

## Edge Contracts

These are the seams where the documents meet:

1. **Application -> AI Gateway:** product request, user identity material, requested action, requested tools, tenant/app metadata.
2. **AI Gateway -> RAG Orchestrator:** safe query, principal claims, authorization filters, policy constraints, allowed retrieval tools, citation requirement.
3. **RAG Orchestrator -> Retrieval Tools:** tool-specific query, row/document/graph authorization filters, cost and timeout limits.
4. **Retrieval Tools -> Retrieval Coordinator:** authorized candidates with source metadata, scores, provenance, and policy-check metadata.
5. **RAG / Multi-Agent Layer -> Prompt Builder:** ranked evidence, source IDs, citation map, and generation constraints.
6. **Prompt Builder -> AI Gateway:** final prompt package, citation map, allowed model/tools, token budget, and validation inputs.
7. **AI Gateway -> LLM Runtime:** controlled model invocation after policy, schema, budget, and routing decisions.
8. **LLM Runtime -> AI Gateway:** raw output, tool-call proposals, token usage, and provider status.
9. **AI Gateway -> Validation Pipeline:** raw output plus original request context, policy constraints, context blocks, and citation map.
10. **AI Gateway -> Application:** validated response, citations, usage metadata, refusal, repair result, or async review status.

## Core Invariants

- All model calls go through the AI Gateway, including planner or rewrite calls made by agents.
- Retrieval tools enforce authorization before content becomes a candidate for reranking or prompt construction.
- The RAG layer may produce validation evidence, but the gateway owns the final return, repair, block, or redaction decision.
- Agents can choose retrieval workflows only within the allowed tools and policies returned by the gateway.
- The LLM generates from authorized context. It does not authorize access, fetch data, approve actions, or validate itself.

## Pattern Map

- **Naive RAG:** User query -> Embedding Model -> Vector Search with authorization filters -> Generation Pipeline.
- **Query Rewriting / RAG Fusion:** One query becomes multiple retrieval queries -> Retrieval Coordinator merges and dedupes -> Reranker -> Generation Pipeline.
- **Hybrid Retrieval:** Optional ontology/entity normalization plus BM25, Vector Search, and optional Graph Traversal -> Reranker -> Generation Pipeline.
- **Hierarchical Retrieval:** Summary Search -> Section Search -> Chunk Search -> Reranker -> Generation Pipeline.
- **Agentic RAG:** Planner Agent chooses tools and sequence -> Retrieval tools -> Generation Pipeline.
- **Multi-Agent RAG:** Router Agent selects specialized agents -> Aggregation -> Reranker -> Generation Pipeline.
- **Evaluation and Guardrails:** Any retrieval pattern -> AI Gateway -> Validation Pipeline -> gateway decision.

Generation Pipeline means:

```text
Context Assembly -> Prompt Builder -> AI Gateway -> LLM -> AI Gateway response validation -> Response
```
