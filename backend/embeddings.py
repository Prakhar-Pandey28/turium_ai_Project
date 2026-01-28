# import sentence transformer for converting text to embeddings
from sentence_transformers import SentenceTransformer

# lightweight model for semantic search and RAG
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    # convert text to vector embedding
    embedding = model.encode(text)
    
    # convert numpy array to list for database storage
    return embedding.tolist()

    