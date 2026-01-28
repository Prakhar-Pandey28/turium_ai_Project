import math

def cosine_similarity(vec1, vec2):
    """Calculate how similar two vectors are (0-1)"""
    
    # dot product
    dot = sum(a * b for a, b in zip(vec1, vec2))
    
    # magnitudes
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    
    # avoid division by zero
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot / (mag1 * mag2)