import sys
from app.ingest import ingest_pdf
from app.embeddings import EmbeddingModel
from app.vectordb import VectorDB


def main():
    if len(sys.argv) < 2:
        pdf_path = "data/sample.pdf"
    else:
        pdf_path = sys.argv[1]

    chunks = ingest_pdf(pdf_path)
    texts = [c["text"] for c in chunks]
    payloads = [{"text": c["text"], **c["metadata"]} for c in chunks]

    embedder = EmbeddingModel()
    vectors = embedder.encode_documents(texts)

    vectordb = VectorDB()
    vectordb.create_collection(vector_size=len(vectors[0]))

    ids = list(range(1, len(vectors) + 1))
    vectordb.upsert(ids, vectors, payloads)

    print(f"Ingestion complete. Indexed {len(chunks)} chunks from {pdf_path}")


if __name__ == "__main__":
    main()