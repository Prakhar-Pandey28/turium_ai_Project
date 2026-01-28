# 🚀 Deployment Guide

## Easiest: Vercel (Frontend) + Railway (Backend)

### Step 1: Deploy Backend to Railway

1. **Push to GitHub** (if not already):
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repo → select `/backend` folder
   - Add environment variable: `GROQ_API_KEY=your_key`
   - Click "Deploy"
   - Copy your railway URL (e.g., `https://ai-knowledge-box-production.up.railway.app`)

### Step 2: Deploy Frontend to Vercel

1. **Update API URL** in `frontend/vite-project/src/App.jsx`:
```javascript
// Change this line:
const API = "http://localhost:8000";
// To your Railway URL:
const API = "https://your-app.railway.app";
```

2. **Deploy**:
```bash
cd frontend/vite-project
npm run build
npx vercel --prod
```

Done! You'll get a live URL like `https://ai-knowledge-box.vercel.app`

---

## Alternative: Render (All-in-one - Free Tier)

### Backend on Render:

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add `GROQ_API_KEY`
5. Create Web Service

### Frontend on Render:

1. New → Static Site
2. Connect same repo
3. Settings:
   - **Root Directory**: `frontend/vite-project`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Create Static Site

---

## Docker Deployment (Local or Cloud)

```bash
# Build and run
docker-compose up --build
```

Access at `http://localhost:3000`

---

## Fly.io (Fast Global Deploy)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy backend
cd backend
fly launch
fly secrets set GROQ_API_KEY=your_key
fly deploy

# Deploy frontend
cd ../frontend/vite-project
fly launch
fly deploy
```

---

## Demo Video

Record a quick 2-min video showing:
1. Adding a URL (use a Turium blog post)
2. Asking a question
3. Getting AI answer with sources
4. Adding a text note
5. Asking another question

Upload to Loom/YouTube and add link to README!

---

## Performance Tips

**Backend**:
- Enable gzip compression
- Use Railway's free tier (512MB RAM)
- Database persists across deployments

**Frontend**:
- Vercel auto-optimizes
- Global CDN included
- Auto HTTPS

---

## 💡 Pro Tips for Impression

1. **Add a live demo link** at the top of README
2. **Screenshot the interface** - show it's actually working
3. **Short video walkthrough** (30 sec - 1 min)
4. **Mention deployment** in interview: "I've deployed it live, would you like to test it?"
5. **Production mindset**: Talk about monitoring, logging, error handling you added
