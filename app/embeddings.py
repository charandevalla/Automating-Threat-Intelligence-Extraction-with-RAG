from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode_documents(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=8,
            show_progress_bar=True
        ).tolist()

    def encode_query(self, text):
        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()