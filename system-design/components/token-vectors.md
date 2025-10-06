# Token-Based Vector Search

## 📖 Definition
**Token-based vector search** (also known as **semantic vector search**) is a technique where text is first tokenized into smaller linguistic units (words, subwords, or sentences) and then converted into high-dimensional numerical vectors called **embeddings**. These embeddings capture semantic meaning, allowing the system to retrieve and rank results based on conceptual similarity rather than exact keyword matches.

---

## 💡 Example

**Input:**  
> “Find restaurants near me that serve sushi.”

1. **Tokenization:** → ["Find", "restaurants", "near", "me", "that", "serve", "sushi"]
2. **Embedding:** → Each token (or sentence) is converted to a vector representation, e.g.:  
   - “sushi” → [0.14, -0.22, 0.88, …]
   - “restaurant” → [0.31, 0.19, 0.47, …]
3. **Vector Search:** → The system computes **cosine similarity** between the query vector and vectors in the index to find semantically similar documents.

---

## 🔍 Vector Search (Similarity Search)

Vector search retrieves items based on **semantic proximity** rather than literal text match.  
Each text, image, or multimodal item is represented by a dense embedding vector.  
The search engine uses **similarity metrics** (e.g., cosine similarity, dot product, Euclidean distance) to rank results.

### Common Similarity Metrics:
- **Cosine Similarity**: Measures angle between vectors (scale-invariant).
- **Dot Product**: Measures projection magnitude (common in neural models).
- **Euclidean Distance**: Measures straight-line distance (less common in high dimensions).

---

## 🧠 Common Technical Terms

| Term | Definition |
|------|-------------|
| **Tokenization** | Breaking text into words, subwords, or sentences. |
| **Embedding (Vectorization)** | Converting tokens or documents into numerical vectors capturing semantic meaning. |
| **Embedding Space** | The high-dimensional space where embeddings live; semantically similar texts cluster together. |
| **Vector Index** | A specialized index (e.g., FAISS, HNSW, ScaNN) optimized for fast similarity search. |
| **Semantic Search** | Retrieval method that ranks results by meaning, not literal keywords. |
| **Dense Retrieval** | Uses neural embeddings for high-dimensional representation (as opposed to sparse bag-of-words). |
| **Vector Database** | Storage engine for embeddings (e.g., Pinecone, Weaviate, Chroma, Milvus). |

---

## 🧭 Flow Diagram

```mermaid
flowchart LR
    A["Text Input"] --> B["Tokenization"]
    B --> C["Embedding Generation (Vectorization)"]
    C --> D["Vector Index (FAISS / Milvus / Pinecone)"]
    D --> E["Similarity Search"]
    E --> F["Ranked Semantic Results"]

    style A fill:#f0f8ff,stroke:#4682b4,stroke-width:1px
    style B fill:#e6f7ff,stroke:#4682b4,stroke-width:1px
    style C fill:#d9f2e6,stroke:#2e8b57,stroke-width:1px
    style D fill:#fff8dc,stroke:#daa520,stroke-width:1px
    style E fill:#ffe4e1,stroke:#cd5c5c,stroke-width:1px
    style F fill:#faf0e6,stroke:#8b4513,stroke-width:1px
```

---

## 🧩 Summary
Token-based vector search bridges **language understanding** and **information retrieval**.  
By representing text as embeddings, it enables systems to:
- Find semantically related documents even if wording differs.
- Support multilingual and context-aware retrieval.
- Power modern **RAG (Retrieval-Augmented Generation)** systems in LLM pipelines.

---