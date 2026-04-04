# 🚀 Deployment Guide - Render + Netlify

This guide walks you through deploying the backend to Render and the frontend to Netlify.

---

## 📋 Prerequisites

1. **Render Account** — Sign up at [render.com](https://render.com) (free tier available)
2. **GitHub Repository** — Push your code to GitHub (Render deploys from Git)
3. **Anthropic API Key** — Get a free key from [console.anthropic.com](https://console.anthropic.com/)

---

## 🔑 Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git & Push to GitHub

```bash
# Navigate to project root
cd guvi\ hack

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: AI Document Analysis app"

# Create a new repository on GitHub (https://github.com/new)
# Then add it as remote and push
git remote add origin https://github.com/YOUR_USERNAME/document-ai.git
git branch -M main
git push -u origin main
```

### 1.2 Update Frontend Configuration

The frontend is already configured to use the `REACT_APP_API_URL` environment variable:

```javascript
// frontend/src/App.js
const API_URL = process.env.REACT_APP_API_URL || 'https://doc-analyzer-ai.onrender.com';
```

---

## 🎯 Step 2: Deploy Backend on Render

### 2.1 Create Backend Service

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

**Service Configuration:**
```
Name:                  document-ai-backend
Environment:           Python 3
Build Command:         pip install -r requirements.txt && pip install gunicorn
Start Command:         gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
Root Directory:        backend
Plan:                  Free
```

### 2.2 Add Environment Variables

In the Render dashboard for the backend service:

1. Click **"Environment"** tab
2. Add these environment variables:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** `sk-ant-xxxxx...` (your actual API key)

3. Add another variable:
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://documentanalyzera.netlify.app`

4. Optional for preview deployments:
   - **Key:** `ALLOWED_ORIGINS`
   - **Value:** `https://documentanalyzera.netlify.app`

### 2.3 Deploy

Click **"Create Web Service"** and wait for deployment (2-5 minutes).

**Backend URL:** `https://doc-analyzer-ai.onrender.com`

---

## 🎨 Step 3: Deploy Frontend on Netlify

### 3.1 Create Frontend Service

1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"Add new site"** → **"Import an existing project"**
3. Import the same GitHub repository
4. Configure the site:

**Service Configuration:**
```
Base directory:        frontend
Build command:         npm run build
Publish directory:     build
```

### 3.2 Add Environment Variables

In the Netlify dashboard for the frontend site:

1. Click **"Environment"** tab
2. Add this variable:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://doc-analyzer-ai.onrender.com`

### 3.3 Deploy

Click **"Deploy site"** and wait for deployment.

**Frontend URL:** `https://documentanalyzera.netlify.app`

---

## ✅ Step 4: Verify Deployment

### 4.1 Check Backend Health

Visit: `https://doc-analyzer-ai.onrender.com/health`

Expected response:
```json
{"status": "healthy"}
```

### 4.2 Check Frontend

Visit: `https://documentanalyzera.netlify.app`

You should see the upload interface.

### 4.3 Test Full Workflow

1. Upload a test document (PDF, DOCX, or image)
2. Wait for analysis
3. Verify results appear and can be downloaded

---

## 🔄 Step 5: Update Both Services (Important!)

After creating both services, update the environment variables:

### For Backend Service:
Go to **Environment** and update:
- **FRONTEND_URL:** `https://documentanalyzera.netlify.app`
- **ALLOWED_ORIGINS:** `https://documentanalyzera.netlify.app`

### For Frontend Project:
Go to **Environment Variables** and confirm:
- **REACT_APP_API_URL:** `https://doc-analyzer-ai.onrender.com`

Then redeploy both:
1. Redeploy the backend on Render if you changed CORS variables
2. Redeploy the frontend on Netlify if you changed `REACT_APP_API_URL`

---

## 🌐 Your Live Links

After successful deployment:

- **Frontend:** `https://documentanalyzera.netlify.app`
- **Backend API:** `https://doc-analyzer-ai.onrender.com`
- **API Docs:** `https://doc-analyzer-ai.onrender.com/docs`

---

## 💡 Troubleshooting

### Common Issues

#### Backend fails with "No module named 'x'"

1. Check `backend/requirements.txt` includes all dependencies
2. Redeploy the backend service
3. Check deployment logs in Render dashboard

#### Frontend shows "Cannot connect to API"

1. Verify `REACT_APP_API_URL` is set correctly
2. Check the backend is running (test `/health` endpoint)
3. Check CORS is properly configured
4. Redeploy frontend

#### API Key not working

1. Verify key starts with `sk-ant-`
2. Check key is active at [console.anthropic.com](https://console.anthropic.com/)
3. Ensure it's set in environment variables (not in code)
4. Redeploy backend after updating

#### Free tier limitations

- Apps spin down after 15 minutes of inactivity
- First request takes ~30 seconds to wake up
- Monthly usage limits apply
- Consider upgrading with paid plans for production

---

## 📊 Monitoring

### View Logs

In Render dashboard, go to each service and click **"Logs"** tab to see real-time logs.

### Monitor Performance

Check **Metrics** tab to see:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔐 Security Notes

⚠️ **Important:**
- Never commit `.env` file to GitHub
- Always use environment variables in dashboard
- Keep API keys confidential
- Rotate keys periodically
- For production, consider upgrading to paid plan

---

## 🎓 Next Steps

### Optional Enhancements

1. **Custom Domain** — Render allows custom domains (upgrade to paid)
2. **SSL/TLS** — Automatically included (HTTPS)
3. **Email Notifications** — Set up for deployment status
4. **GitHub Integrations** — Auto-deploy on push

### Performance Optimization

1. Add caching to reduce API calls
2. Implement request queuing for large files
3. Use CDN for frontend assets
4. Optimize PDF parsing libraries

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Anthropic API:** https://docs.anthropic.com/

---

**Happy deploying! 🎉**
