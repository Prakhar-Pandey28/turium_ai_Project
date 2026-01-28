from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Optional
import json
import requests
import logging

from db import conn, curr
from chunker import chunk_text
from embeddings import embed
from vector import cosine_similarity
from llm import ask_llm
from html_parser import extract_text_from_url

from fastapi.middleware.cors import CORSMiddleware

# setup logging so we can debug issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS setup - needed for frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestReq(BaseModel):
    content: Optional[str] = None
    url: Optional[str] = None
    
    @validator('*')
    def check_at_least_one(cls, v, values):
        # make sure they provide either content or url
        if 'content' in values and not values.get('content') and not v:
            raise ValueError('Must provide either content or url')
        return v

class QueryReq(BaseModel):
    question: str
    
    @validator('question')
    def question_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')
        return v

# API endpoints
@app.post("/ingest")
def ingest(data: IngestReq):
    """
    Takes either a text note or URL and stores it in the database
    Uses Jina AI to extract clean text from URLs
    """
    
    try:
        # figure out what kind of content we're dealing with
        if data.url:
            logger.info(f"Processing URL: {data.url}")
            try:
                content = extract_text_from_url(data.url)
            except Exception as e:
                logger.error(f"Failed to fetch URL: {e}")
                raise HTTPException(status_code=400, detail=f"Could not fetch URL: {str(e)}")
            source = "url"
        else:
            content = data.content
            source = "note"
        
        if not content or len(content.strip()) < 10:
            raise HTTPException(status_code=400, detail="Content too short or empty")
        
        # break it into chunks so we can search through it later
        chunks = chunk_text(content)
        
        # save the original item first
        curr.execute(
            "INSERT INTO items (content, source, created_at) VALUES (?, ?, datetime('now'))",
            (content, source)
        )
        item_id = curr.lastrowid
        conn.commit()
        
        # now process each chunk
        for chunk in chunks:
            embedding = embed(chunk)
            
            # store chunk with embedding
            curr.execute(
                "INSERT INTO chunks (item_id, chunk_text, embedding) VALUES (?, ?, ?)",
                (item_id, chunk, json.dumps(embedding))
            )
        
        conn.commit()
        logger.info(f"Ingested {len(chunks)} chunks for item {item_id}")
        
        return {"message": "Content ingested successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}") 

@app.get("/items")
def items():
    """return all stored items with newest first"""
    curr.execute("SELECT * FROM items ORDER BY created_at DESC")
    return curr.fetchall()

@app.post("/query")
def query(data: QueryReq):
    """
    Main search endpoint - finds relevant chunks and asks LLM
    """
    try:
        question = data.question
        logger.info(f"Query: {question[:50]}...")
        
        # get embedding for the question
        query_embedding = embed(question)
        
        # grab all chunks from DB
        curr.execute("SELECT id, chunk_text, embedding FROM chunks")
        all_chunks = curr.fetchall()
        
        if not all_chunks:
            logger.warning("No chunks in database")
            return {
                "answer": "I don't have any knowledge stored yet. Please add some content first.",
                "sources": []
            }
        
        # calculate similarity scores for each chunk
        scored = []
        for chunk_id, text, embedding_json in all_chunks:
            embedding = json.loads(embedding_json)
            score = cosine_similarity(query_embedding, embedding)
            scored.append((text, score))
        
        # get top 5 most similar chunks
        top = sorted(scored, key=lambda x: x[1], reverse=True)[:5]
        
        # combine them into context
        context = "\n".join(t[0] for t in top)
        
        # ask the LLM
        answer = ask_llm(context, question)
        
        logger.info(f"Returned answer ({len(answer)} chars)")
        
        # return answer with source chunks
        return {
            "answer": answer,
            "sources": top  # helpful to see what it used
        }
    
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")