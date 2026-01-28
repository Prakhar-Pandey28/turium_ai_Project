# import sentence transformer for converting text to embeddings
from sentence_transformers import SentenceTransformer

# lightweight model for semantic search and RAG
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text_or_list):
    # convert text (or list of texts) to vector embedding(s)
    # model.encode handles batching automatically which is much faster
    embeddings = model.encode(text_or_list)
    
    # convert numpy array to list for database storage
    return embeddings.tolist()

    