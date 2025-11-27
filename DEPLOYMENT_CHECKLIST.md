# Vercel Deployment Checklist

## Pre-Deployment Steps

### 1. ✅ Code is Ready
- [x] Flask app configured (`app.py`)
- [x] Vercel serverless handler (`api/index.py`)
- [x] Vercel configuration (`vercel.json`)
- [x] Requirements file updated (`requirements.txt`)
- [x] Templates directory (`templates/index.html`)
- [x] .gitignore configured

### 2. Git Repository Setup

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Vercel deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/joegit1996/get_social_media.git

# Push to GitHub
git push -u origin main
```

### 3. Deploy to Vercel

**Option A: Via Vercel Dashboard (Recommended)**
1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select `joegit1996/get_social_media`
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
5. Add Environment Variables:
   - `GOOGLE_API_KEY` = (your API key)
   - `GOOGLE_CSE_ID` = (your CSE ID)
6. Click "Deploy"

**Option B: Via Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Add environment variables
vercel env add GOOGLE_API_KEY
vercel env add GOOGLE_CSE_ID

# Deploy to production
vercel --prod
```

### 4. Post-Deployment

After deployment, your app will be available at:
- **Web Interface**: `https://your-app-name.vercel.app/`
- **API Endpoint**: `https://your-app-name.vercel.app/api/find?business_name=Apple&country=USA`

## Testing

1. **Test Web Interface**:
   - Visit `https://your-app-name.vercel.app/`
   - Enter a business name and country
   - Verify results appear

2. **Test API Endpoint**:
   ```bash
   curl "https://your-app-name.vercel.app/api/find?business_name=McDonald's&country=Kuwait"
   ```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**:
   - Ensure all dependencies are in `requirements.txt`
   - Check that package names match exactly (Flask-CORS not flask-cors)

2. **500 Internal Server Error**:
   - Check Vercel function logs in dashboard
   - Verify environment variables are set correctly
   - Ensure `api/index.py` properly imports the app

3. **Template Not Found**:
   - Verify `templates/` directory is included in deployment
   - Check that `template_folder='templates'` is set in Flask app

4. **CORS Errors**:
   - Flask-CORS should handle this automatically
   - If issues persist, check CORS configuration in `app.py`

## Environment Variables

Required (Optional but recommended):
- `GOOGLE_API_KEY`: Your Google Custom Search API key
- `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID

The app will work without these, but with reduced accuracy.

## File Structure for Vercel

```
.
├── api/
│   └── index.py          # Vercel serverless function handler
├── templates/
│   └── index.html        # Web interface template
├── app.py                # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## Notes

- Vercel automatically detects Python projects
- Serverless functions have a 10-second timeout by default (can be increased)
- Free tier includes 100GB bandwidth and 100 hours of execution time
- Environment variables are encrypted and secure

