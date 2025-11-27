# Quick Deployment Guide

## ✅ Repository Setup Complete!

Your local repository is ready. Follow these steps to deploy:

## Step 1: Push to GitHub

```bash
# Push your code to GitHub
git push -u origin main
```

If you get an error about the branch name, try:
```bash
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Select **`joegit1996/get_social_media`**
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
5. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add `GOOGLE_API_KEY` = (your API key)
   - Add `GOOGLE_CSE_ID` = (your CSE ID)
   - Note: These are optional but recommended for better accuracy
6. Click **"Deploy"**

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI (if not already installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (first time - follow prompts)
vercel

# Add environment variables (optional but recommended)
vercel env add GOOGLE_API_KEY
vercel env add GOOGLE_CSE_ID

# Deploy to production
vercel --prod
```

## Step 3: Test Your Deployment

After deployment, your app will be live at:
- **Web Interface**: `https://your-app-name.vercel.app/`
- **API Endpoint**: `https://your-app-name.vercel.app/api/find?business_name=McDonald's&country=Kuwait`

### Test the Web Interface:
1. Visit your Vercel URL
2. Enter a business name (e.g., "McDonald's")
3. Enter a country (e.g., "Kuwait")
4. Click "Search Social Media Links"

### Test the API:
```bash
curl "https://your-app-name.vercel.app/api/find?business_name=McDonald's&country=Kuwait"
```

## Project Structure

```
.
├── api/
│   └── index.py          # Vercel serverless function handler
├── templates/
│   └── index.html        # Web interface
├── app.py                # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## Environment Variables

**Optional but Recommended:**
- `GOOGLE_API_KEY`: Your Google Custom Search API key
- `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID

**Note:** The app works without these variables, but with reduced accuracy. It will automatically fall back to web scraping methods.

## Troubleshooting

### If deployment fails:

1. **Check Vercel logs**: Go to your project dashboard → Functions → View logs
2. **Verify requirements.txt**: Ensure all dependencies are listed
3. **Check Python version**: Vercel uses Python 3.9 by default (should work fine)
4. **Verify file structure**: Ensure `api/index.py` exists and properly imports `app`

### Common Issues:

- **ModuleNotFoundError**: Check `requirements.txt` has all dependencies
- **500 Error**: Check Vercel function logs for details
- **Template not found**: Verify `templates/` directory is included

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Vercel
3. ✅ Test the deployment
4. ✅ Share your app URL!

## Support

For detailed setup instructions, see:
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Complete checklist
- [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) - Detailed Vercel guide
- [README.md](README.md) - Project documentation

