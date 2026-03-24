from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorDB:
    def __init__(self, collection_name="threat_intel", host="localhost", port=6333):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)

    def create_collection(self, vector_size):
        existing = [c.name for c in self.client.get_collections().collections]

        if self.collection_name in existing:
            self.client.delete_collection(collection_name=self.collection_name)

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    def upsert(self, ids, vectors, payloads):
        points = [
            PointStruct(id=i, vector=v, payload=p)
            for i, v, p in zip(ids, vectors, payloads)
        ]
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector, limit=5):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )
        return results.points