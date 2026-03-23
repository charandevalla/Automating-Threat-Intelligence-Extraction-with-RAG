from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name="BAAI/bge-large-en-v1.5"):
        self.model = SentenceTransformer(model_name)

    def encode_documents(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def encode_query(self, text):
        return self.model.encode(text, normalize_embeddings=True).tolist()