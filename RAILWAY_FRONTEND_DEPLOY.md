# 🚂 Deploy Frontend to Railway

## Current Status

✅ **Backend is deployed**: `https://rasan-ai-labs-production.up.railway.app/`  
❌ **Frontend is NOT deployed** - That's why you only see JSON

## Solution: Deploy Frontend as Separate Service

Railway allows multiple services in one project. We need to add the frontend as a second service.

## Step-by-Step Deployment Guide

### Option 1: Deploy Frontend as Static Site Service (Recommended)

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Open your project: "RASAN AI Labs" (or whatever you named it)

2. **Add New Service**
   - Click **"+ New"** button
   - Select **"GitHub Repo"** (same repo as backend)
   - OR select **"Static Site"** if available

3. **Configure Frontend Service**
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm ci && npm run build`
   - **Output Directory**: `dist/`
   - **Start Command**: (leave empty for static sites)

4. **Set Environment Variables**
   - `VITE_API_URL`: `https://rasan-ai-labs-production.up.railway.app/api/v1`
   - Railway will generate a URL for your frontend (e.g., `https://your-frontend.up.railway.app`)

5. **Get Frontend URL**
   - Railway will assign a URL like: `https://your-frontend-name.up.railway.app`
   - Copy this URL

6. **Update Backend CORS**
   - Go to your backend service settings
   - Add environment variable:
     ```
     CORS_ORIGINS=https://your-frontend-name.up.railway.app,https://rasan-ai-labs-production.up.railway.app
     ```
   - Redeploy backend service

### Option 2: Deploy Frontend with Dockerfile

If Railway doesn't support static sites directly:

1. **Create railway-frontend.json** (already exists via Dockerfile)
2. **Add New Service in Railway**
   - Click **"+ New"** → **"GitHub Repo"**
   - Select same repository
   - Railway will detect the Dockerfile

3. **Configure Service**
   - Set **Root Directory** to `frontend/`
   - Railway will use `frontend/Dockerfile`
   - Set environment variable:
     ```
     VITE_API_URL=https://rasan-ai-labs-production.up.railway.app/api/v1
     ```

4. **Get Frontend URL and Update CORS** (same as Option 1, step 6)

## Alternative: Serve Frontend from Backend (Simpler, Single Service)

If you prefer one service, we can modify the backend to serve static frontend files. This is simpler but less scalable.

### Quick Fix: Serve Frontend from Backend

I'll update the backend to serve the frontend build files. This way, one Railway service serves both.

## Verification

After deployment:

1. **Frontend URL should show your React app** (not JSON)
2. **Backend API should work** at `/api/v1/*` endpoints
3. **Frontend can make API calls** to backend

## Troubleshooting

### Frontend shows "Cannot connect to API"
- Check `VITE_API_URL` environment variable in frontend service
- Verify backend CORS includes frontend URL
- Check browser console for CORS errors

### 404 errors on routes
- Make sure `nginx.conf` is configured correctly (for Dockerfile option)
- Check that SPA routing is enabled

### Build fails
- Check Railway build logs
- Verify `package.json` has all dependencies
- Ensure Node.js version is compatible

## Next Steps

1. Choose deployment option (Static Site or Dockerfile)
2. Deploy frontend service
3. Get frontend URL from Railway
4. Update backend CORS settings
5. Test the full application!

---

**Need help?** Check Railway logs for detailed error messages.

