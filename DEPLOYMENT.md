# 🚀 Deployment Guide

## Easiest: Vercel (Frontend) + Render (Backend)

### Step 1: Deploy Backend to Render

1. **Push to GitHub** (if not already):
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up
   - Click **"New +"** → **"Web Service"**
   - Select **"Build and deploy from a Git repository"**
   - Connect your GitHub account and choose your repo
   - Configure:
     - **Name**: `ai-knowledge-box` (or any name)
     - **Root Directory**: `backend`
     - **Environment**: `Python 3.9` (important - select 3.9.x)
     - **Build Command**: `pip install --prefer-binary -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click **"Advanced"** → Add environment variable:
     - **Key**: `GROQ_API_KEY`
     - **Value**: your Groq API key
   - Click **"Create Web Service"**
   - Wait ~5 minutes for first deploy
   - Copy your Render URL (e.g., `https://ai-knowledge-box.onrender.com`)

### Step 2: Deploy Frontend to Vercel

1. **Update API URL** in `frontend/vite-project/src/App.jsx`:
```javascript
// Change this line:
const API = "http://localhost:8000";
// To your Render URL:
const API = "https://ai-knowledge-box.onrender.com";
```

2. **Deploy**:
```bash
cd frontend/vite-project
npm run build
npx vercel --prod
```

Done! You'll get a live URL like `https://ai-knowledge-box.vercel.app`

---

## Alternative Free Options

### Option 2: Koyeb (Easy, Free Tier)

**Backend on Koyeb:**
1. Go to [koyeb.com](https://koyeb.com) and sign up
2. Click **"Create App"**
3. Select **"GitHub"** and connect your repo
4. Configure:
   - **Root path**: `/backend`
   - **Build command**: `pip install -r requirements.txt`
   - **Run command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Add env var: `GROQ_API_KEY`
5. Deploy

**Pros**: Fast deploys, good free tier, simple UI

---

### Option 3: Fly.io (Fast Global Deploy)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy backend
cd backend
fly launch --no-deploy
fly secrets set GROQ_API_KEY=your_key
fly deploy

# Deploy frontend
cd ../frontend/vite-project
fly launch
fly deploy
```

**Pros**: Global edge network, 3 VMs free, fast

---

### Option 4: All-in-One on Render

**Both frontend and backend on Render (static + web service):**

1. Deploy backend as web service (as above)
2. Deploy frontend as static site:
   - New → Static Site
   - Root Directory: `frontend/vite-project`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

**Pros**: Everything in one place, easy to manage

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
