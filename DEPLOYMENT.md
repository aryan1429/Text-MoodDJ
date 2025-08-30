Deployment guide — Frontend on Vercel, Backend on Render

Checklist
- Frontend: build with Vite and host on Vercel
- Backend: FastAPI app served by Uvicorn on Render
- Set environment variables (GIPHY_API_KEY, ALLOWED_ORIGIN, any YouTube keys)

Frontend (Vercel)
1. In the Vercel dashboard, create a new Project and import this repository.
2. Select the `frontend` folder as the Root Directory during import.
3. Build Settings:
   - Framework Preset: Other
   - Build Command: npm run build
   - Output Directory: dist
4. (Optional) Add Environment Variable `VITE_API_BASE` pointing to your Render backend URL (for example `https://your-backend.onrender.com`).
   - If not set, the frontend will default to `http://localhost:8000` during development.
5. Deploy. Vercel will run the build and serve the `dist` folder.

Notes for Vercel:
- The included `vercel.json` config sets up a static-build using the `dist` folder and routes all requests to `index.html` so client-side routing works.

Backend (Render)
1. In the Render dashboard create a new Web Service and connect your repository.
2. Set the Root Directory to `backend`.
3. Environment:
   - Build Command: pip install -r requirements.txt
   - Start Command: bash start.sh
4. Add the following Environment Variables in Render:
   - GIPHY_API_KEY = <your key>
   - ALLOWED_ORIGIN = https://<your-frontend-domain>  # e.g. https://your-frontend.vercel.app
   - (any other keys from your `.env`)
5. Deploy. Render will install the requirements and run `start.sh` which launches Uvicorn on the port Render assigns via $PORT.

CORS and API Base
- Make sure `ALLOWED_ORIGIN` in Render matches the Vercel frontend URL. The backend reads `ALLOWED_ORIGIN` to configure CORS.
- Alternatively, set ALLOWED_ORIGIN to `*` for quick testing (not recommended for production).

Verification
- After Vercel and Render deployments finish, update `VITE_API_BASE` in Vercel to `https://<render-service>.onrender.com` and redeploy the frontend.
- Visit the frontend URL and try submitting text to ensure the API calls succeed.
- Check Render logs for errors if API calls fail.

Helpful tips
- If your frontend fails to find the API during build-time, `import.meta.env.VITE_API_BASE` is only available at build time; on Vercel set it in Project Environment Variables.
- Use `withCredentials: true` on the frontend (already configured) and ensure Render allows cookies; cross-site cookies may require SameSite adjustments.

If you want, I can:
- Create a Render service YAML for Infrastructure as Code
- Add a tiny healthcheck endpoint `/` in the backend that returns 200 so Render shows `Healthy`

Troubleshooting: "bash: start.sh: No such file or directory"
- Cause: Render runs the `Start Command` from the service's configured Root Directory. If you set the Root Directory to the repo root, `start.sh` in `backend/` won't be found and you'll see this error.
- Quick fixes:
   1. Set the service Root Directory to `backend` in the Render dashboard so `start.sh` is found.
   2. Or change the Start Command to `bash backend/start.sh` (if Root Directory is repo root).
   3. Or use the `render.yaml` I added (`render.yaml` at repo root) which sets `startCommand: bash backend/start.sh` and `buildCommand: pip install -r backend/requirements.txt` — import this YAML in the Render dashboard when creating the service.

I added `render.yaml` to the repo so you can create a Render service from the file (it points to `backend/start.sh`). If Render still fails to find the script, double-check the Root Directory setting or use the full path in the Start Command.
