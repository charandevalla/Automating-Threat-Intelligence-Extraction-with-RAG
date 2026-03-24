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

    print("Extracted metadata summary:")
    print(f"  CVEs: {len(total_cves)}")
    print(f"  IPs: {len(total_ips)}")
    print(f"  Domains: {len(total_domains)}")
    print(f"  Hashes: {len(total_hashes)}")
    print(f"  MITRE Techniques: {len(total_mitre)}")
    print(f"  Threat Actors: {len(total_actors)}")


if __name__ == "__main__":
    main()