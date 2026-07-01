# RAG Retrieval Patterns

This topic is split into separate design views under [`rag_retrieval/`](./rag_retrieval/):

1. [AI Gateway Internal Design](./rag_retrieval/ai-gateway-internal-design.md)
2. [End-to-End RAG System Design](./rag_retrieval/end-to-end-rag-system-design.md)
3. [Advanced Multi-Agent Retrieval Design](./rag_retrieval/advanced-multi-agent-retrieval-design.md)

Start with the [folder overview](./rag_retrieval/README.md) for the ownership map and the handoff contracts between these views.

## Core Boundary

**The AI Gateway owns policy and model-runtime decisions. The RAG system owns retrieval and evidence preparation. The LLM owns generation only.**

All model calls should go through the AI Gateway. Retrieval execution stays inside the RAG system, and specialized agents only plan or execute retrieval work that is allowed by gateway policy.
