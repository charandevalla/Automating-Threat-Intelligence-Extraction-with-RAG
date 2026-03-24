from app.llm import LocalLLM
from app.embeddings import EmbeddingModel
from app.vectordb import VectorDB


class ThreatIntelRAG:
    def __init__(self):
        self.llm = LocalLLM()
        self.embedder = EmbeddingModel()
        self.vectordb = VectorDB()

    def ask(self, query, top_k=5):
        query_vector = self.embedder.encode_query(query)
        results = self.vectordb.search(query_vector, limit=top_k)

        context_chunks = []
        sources = []

        for r in results:
            payload = r.payload
            text = payload.get("text", "")
            page = payload.get("page", payload.get("page_number", "unknown"))

            context_chunks.append(text)
            sources.append({
                "page": page,
                "text_preview": text[:300]
            })

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a threat intelligence assistant.

Use only the context below.
If the answer is not in the context, say:
"I could not find relevant threat intelligence information in the indexed documents."

At the end of the answer, include a short citation note like:
Sources: page X, page Y

Context:
{context}

Question:
{query}
"""
        answer = self.llm.generate(prompt)
        return answer, context_chunks, sources