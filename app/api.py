from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag import ThreatIntelRAG
from app.ingest import ingest_pdf
from app.embeddings import EmbeddingModel
from app.vectordb import VectorDB


app = FastAPI(title="Threat Intelligence RAG API")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class IngestRequest(BaseModel):
    pdf_path: str = "data/sample.pdf"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest(req: IngestRequest):
    pdf_path = req.pdf_path

    try:
        chunks = ingest_pdf(pdf_path)
        if not chunks:
            raise HTTPException(status_code=400, detail="No content found in PDF.")

        texts = [c["text"] for c in chunks]
        payloads = [{"text": c["text"], **c["metadata"]} for c in chunks]

        embedder = EmbeddingModel()
        vectors = embedder.encode_documents(texts)

        vectordb = VectorDB()
        vectordb.create_collection(vector_size=len(vectors[0]))

        ids = list(range(1, len(vectors) + 1))
        vectordb.upsert(ids, vectors, payloads)

        total_cves = set()
        total_ips = set()
        total_domains = set()
        total_hashes = set()
        total_mitre = set()
        total_actors = set()

        for chunk in payloads:
            total_cves.update(chunk.get("cves", []))
            total_ips.update(chunk.get("ips", []))
            total_domains.update(chunk.get("domains", []))
            total_hashes.update(chunk.get("hashes", []))
            total_mitre.update(chunk.get("mitre_techniques", []))
            total_actors.update(chunk.get("threat_actors", []))

        return {
            "message": "Ingestion complete.",
            "pdf_path": pdf_path,
            "chunks_indexed": len(chunks),
            "metadata_summary": {
                "cves": sorted(total_cves),
                "ips": sorted(total_ips),
                "domains": sorted(total_domains),
                "hashes": sorted(total_hashes),
                "mitre_techniques": sorted(total_mitre),
                "threat_actors": sorted(total_actors)
            }
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"PDF file not found at {pdf_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def ask(req: QueryRequest):
    try:
        rag = ThreatIntelRAG()
        answer, context_chunks, sources, metadata_summary = rag.ask(req.query, req.top_k)

        return {
            "query": req.query,
            "answer": answer,
            "context_chunks": context_chunks,
            "sources": sources,
            "metadata_summary": metadata_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/iocs")
def get_iocs(query: str = "List the extracted IOCs", top_k: int = 10):
    try:
        rag = ThreatIntelRAG()
        _, _, _, metadata_summary = rag.ask(query, top_k)

        return {
            "message": "IOC summary from retrieved chunks",
            "metadata_summary": metadata_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))