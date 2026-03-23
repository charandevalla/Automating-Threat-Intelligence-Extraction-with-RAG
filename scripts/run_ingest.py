from app.ingest import ingest_pdf
from app.embeddings import EmbeddingModel
from app.vectordb import VectorDB


def main():
    pdf_path = "data/sample.pdf"

    chunks = ingest_pdf(pdf_path)
    texts = [c["text"] for c in chunks]
    payloads = [{"text": c["text"], **c["metadata"]} for c in chunks]

    embedder = EmbeddingModel()
    vectors = embedder.encode_documents(texts)

    vectordb = VectorDB()
    vectordb.create_collection(vector_size=len(vectors[0]))

    ids = list(range(1, len(vectors) + 1))
    vectordb.upsert(ids, vectors, payloads)

    print("Ingestion complete.")


if __name__ == "__main__":
    main()