# AI Knowledge Box 🧠

A production-ready RAG (Retrieval-Augmented Generation) system that lets you save notes/URLs and search through them using AI.

Built for **Turium AI** interview task.

## 🎯 What It Does

- **Save Knowledge**: Add text notes or paste URLs (auto-extracts content)
- **Smart Search**: Ask questions in natural language
- **AI Answers**: Get answers powered by Groq's Llama 3.3 with source citations
- **Beautiful UI**: Modern, responsive interface matching Turium's design language

## 🏗️ Architecture

```
Frontend (React + Vite)
    ↓
Backend (FastAPI)
    ↓
┌──────────────────┐
│ 1. Jina Reader   │ → Extract clean text from URLs
│ 2. Chunker       │ → Split into 800-char chunks (100 overlap)
│ 3. Embeddings    │ → sentence-transformers/all-MiniLM-L6-v2
│ 4. Vector Store  │ → SQLite with JSON embeddings
│ 5. Retrieval     │ → Cosine similarity (top-5)
│ 6. LLM           │ → Groq Llama 3.3 70B
└──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API key ([get one free](https://console.groq.com))

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend/vite-project
npm install
npm run dev
```

App runs at: `http://localhost:5173`

## 📦 Deployment

### Option 1: Vercel + Railway (Recommended - Free)

**Frontend (Vercel):**
```bash
cd frontend/vite-project
npm run build
# Deploy to Vercel (one command)
npx vercel --prod
```

**Backend (Railway):**
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. "New Project" → Import from GitHub
4. Add `GROQ_API_KEY` in environment variables
5. Deploy!

**Update frontend API URL** in `App.jsx`:
```javascript
const API = "https://your-railway-app.railway.app";
```

### Option 2: Docker (Production-Ready)

```bash
docker-compose up --build
```

Access at `http://localhost:3000`

## 🎨 Design Decisions

### Chunking Strategy
- **800 chars per chunk** - Balance between context and precision
- **100 char overlap** - Prevents losing key phrases at boundaries
- **Tradeoff**: Simple but effective. Would use LangChain's RecursiveTextSplitter for production.

### Why Jina AI Reader?
- Free, no API key needed
- Converts any URL to clean markdown
- Removes ads, navigation automatically
- Better than BeautifulSoup for RAG

### Vector Store Choice
- **SQLite with JSON** - Simple, no extra dependencies
- **Tradeoff**: Not optimized for >10k chunks. Would use Pinecone/Weaviate at scale.

### Embedding Model
- **all-MiniLM-L6-v2** - Fast, accurate, runs locally
- **384 dimensions** - Good balance of speed/quality
- **Tradeoff**: Smaller model than OpenAI's but free and fast

## 🔧 API Endpoints

### POST `/ingest`
Stores a note or URL
```json
{
  "content": "Your text here",
  "url": "https://example.com"  // Optional
}
```

### GET `/items`
Lists all saved items
```json
[
  [id, content, source_type, timestamp]
]
```

### POST `/query`
Searches and answers
```json
{
  "question": "What is...?"
}
```

**Response:**
```json
{
  "answer": "Based on context...",
  "sources": [
    ["chunk text", 0.85],  // [text, similarity_score]
    ...
  ]
}
```

## 📊 What Scales & What Breaks

**Currently Handles:**
- ✅ ~1000 notes/URLs
- ✅ Single user
- ✅ Concurrent requests (FastAPI async)

**Breaks At Scale:**
- ❌ >10k chunks (linear scan for cosine similarity)
- ❌ Large files (no streaming)
- ❌ Multi-user (no auth/isolation)

**Production Changes:**
1. **Vector DB**: Pinecone/Weaviate with HNSW indexing
2. **Chunking**: LangChain RecursiveTextSplitter
3. **Auth**: JWT tokens, user isolation
4. **Caching**: Redis for embeddings
5. **Monitoring**: Sentry, DataDog
6. **Rate limiting**: Prevent abuse
7. **Database**: PostgreSQL with pgvector

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- CSS (no framework, custom design)
- Fetch API

**Backend:**
- FastAPI (async Python)
- SQLite
- sentence-transformers
- Groq API
- Jina AI Reader

## 📝 Project Structure

```
ai-knowledge-box/
├── backend/
│   ├── main.py           # FastAPI app & routes
│   ├── db.py            # Database setup
│   ├── chunker.py       # Text splitting logic
│   ├── embeddings.py    # Vector generation
│   ├── vector.py        # Similarity calculation
│   ├── llm.py           # Groq integration
│   ├── html_parser.py   # URL content extraction
│   └── requirements.txt
└── frontend/
    └── vite-project/
        └── src/
            ├── App.jsx      # Main component
            ├── App.css      # Turium-branded styles
            └── main.jsx     # Entry point
```

## 🎥 Demo

**Live Demo**: [Add your deployment URL here]

**Screenshots**: See `/screenshots` folder

## 🧪 Testing

```bash
# Test ingestion
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Artificial_intelligence"}'

# Test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is AI?"}'
```

## 🐛 Debugging

**Check logs:**
```bash
# Backend logs show:
# - INFO: Processing URL: ...
# - INFO: Query: What is...
# - ERROR: Failed to fetch URL: ...
```

**Common issues:**
- CORS error → Check API URL in frontend
- Empty results → Check if content was ingested
- Slow queries → Database might be large

## 📄 License

MIT - Built as an interview task for Turium AI

---

**Time spent**: ~8 hours
**Lines of code**: ~800 (backend + frontend)
**External APIs**: Groq (LLM), Jina (URL parsing)
