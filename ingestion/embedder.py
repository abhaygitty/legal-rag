from sentence_transformers import SentenceTransformer
import config

model = SentenceTransformer(config.EMBEDDING_MODEL)

def embed(text):
    return model.encode(text).tolist()