"""
Embeddings using Jina AI's API instead of local models.
This saves ~500MB of RAM by not loading PyTorch + sentence-transformers.

Jina AI provides embeddings with generous free tier.
Get your free API key at: https://jina.ai/
"""
import requests
import logging
import os

logger = logging.getLogger(__name__)

JINA_EMBEDDINGS_API = "https://api.jina.ai/v1/embeddings"
JINA_API_KEY = os.getenv("JINA_API_KEY", "")  # Optional: set in .env for higher limits

def embed(text_or_list):
    """
    Convert text (or list of texts) to vector embeddings using Jina AI API.
    This is much more memory-efficient than loading a local model.
    """
    # Normalize input to list
    is_single = isinstance(text_or_list, str)
    texts = [text_or_list] if is_single else text_or_list
    
    # Limit batch size to prevent API issues
    MAX_BATCH = 100
    if len(texts) > MAX_BATCH:
        logger.warning(f"Batch size {len(texts)} exceeds max {MAX_BATCH}, processing in chunks")
        all_embeddings = []
        for i in range(0, len(texts), MAX_BATCH):
            batch = texts[i:i + MAX_BATCH]
            batch_embeddings = _call_jina_api(batch)
            all_embeddings.extend(batch_embeddings)
        return all_embeddings[0] if is_single else all_embeddings
    
    embeddings = _call_jina_api(texts)
    return embeddings[0] if is_single else embeddings

def _call_jina_api(texts):
    """Call Jina AI embeddings API"""
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key if available
        if JINA_API_KEY:
            headers["Authorization"] = f"Bearer {JINA_API_KEY}"
        
        response = requests.post(
            JINA_EMBEDDINGS_API,
            json={
                "model": "jina-embeddings-v3",
                "task": "retrieval.passage",  # Optimized for RAG
                "dimensions": 768,  # Standard embedding size
                "input": texts
            },
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"Jina API error: {response.status_code} - {response.text}")
            raise Exception(f"Embedding API failed: {response.status_code}. Please set JINA_API_KEY in your .env file. Get a free key at https://jina.ai/")
        
        data = response.json()
        embeddings = [item["embedding"] for item in data["data"]]
        return embeddings
        
    except requests.Timeout:
        raise Exception("Embedding API timed out. Please try again.")
    except requests.RequestException as e:
        raise Exception(f"Embedding API error: {str(e)}")
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        raise