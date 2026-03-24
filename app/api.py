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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest():
    pdf_path = "data/sample.pdf"

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

        return {
            "message": "Ingestion complete.",
            "chunks_indexed": len(chunks)
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF file not found at data/sample.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def ask(req: QueryRequest):
    try:
        rag = ThreatIntelRAG()
        answer, context_chunks = rag.ask(req.query, req.top_k)

        return {
            "query": req.query,
            "answer": answer,
            "context_chunks": context_chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))