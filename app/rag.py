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

        all_cves = set()
        all_ips = set()
        all_domains = set()
        all_hashes = set()
        all_mitre = set()
        all_actors = set()

        for r in results:
            payload = r.payload
            text = payload.get("text", "")
            page = payload.get("page", payload.get("page_number", "unknown"))

            context_chunks.append(text)

            all_cves.update(payload.get("cves", []))
            all_ips.update(payload.get("ips", []))
            all_domains.update(payload.get("domains", []))
            all_hashes.update(payload.get("hashes", []))
            all_mitre.update(payload.get("mitre_techniques", []))
            all_actors.update(payload.get("threat_actors", []))

            sources.append({
                "page": page,
                "text_preview": text[:300],
                "cves": payload.get("cves", []),
                "ips": payload.get("ips", []),
                "domains": payload.get("domains", []),
                "hashes": payload.get("hashes", []),
                "mitre_techniques": payload.get("mitre_techniques", []),
                "threat_actors": payload.get("threat_actors", [])
            })

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a threat intelligence assistant.

Use only the context below.
If the answer is not in the context, say:
"I could not find relevant threat intelligence information in the indexed documents."

At the end of the answer, include a short note with relevant metadata if available.

Context:
{context}

Question:
{query}

Relevant metadata from retrieved chunks:
CVEs: {sorted(all_cves)}
IPs: {sorted(all_ips)}
Domains: {sorted(all_domains)}
Hashes: {sorted(all_hashes)}
MITRE Techniques: {sorted(all_mitre)}
Threat Actors: {sorted(all_actors)}
"""
        answer = self.llm.generate(prompt)

        metadata_summary = {
            "cves": sorted(all_cves),
            "ips": sorted(all_ips),
            "domains": sorted(all_domains),
            "hashes": sorted(all_hashes),
            "mitre_techniques": sorted(all_mitre),
            "threat_actors": sorted(all_actors)
        }

        return answer, context_chunks, sources, metadata_summary