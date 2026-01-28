# Simple text chunking
# Splits text into overlapping chunks so we don't lose context at boundaries
#
# Design decisions:
# - 800 char chunks: Big enough for context, small enough to be specific
# - 100 char overlap: Prevents losing info when a key phrase falls on boundary
# 
# Tradeoffs:
# - Larger chunks = more context but less precision
# - Smaller chunks = more precision but may lose context
# - More overlap = better continuity but more storage
#
# This breaks at scale because:
# - No smart sentence/paragraph boundary detection
# - Doesn't handle tables or code well
# - Would need better chunking for production (langchain, etc)

def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        # grab a chunk
        chunk = text[start:start + size]
        chunks.append(chunk)
        
        # move forward but keep some overlap
        start = start + size - overlap

    return chunks
