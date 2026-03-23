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
        for r in results:
            payload = r.payload
            context_chunks.append(payload.get("text", ""))

        context = "\n\n".join(context_chunks)

        prompt = f"""
Context:
{context}

Question:
{query}

Answer only from the context above. If the answer is not present, say you do not know.
"""
        answer = self.llm.generate(prompt)
        return answer, context_chunks