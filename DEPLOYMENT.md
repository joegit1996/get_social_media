# Deployment Guide for Vercel

This guide will help you deploy the Business Social Media Finder to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. GitHub repository: https://github.com/joegit1996/get_social_media.git
3. Google API credentials (optional but recommended)

## Step 1: Push Code to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Business Social Media Finder"

# Add remote (if not already added)
git remote add origin https://github.com/joegit1996/get_social_media.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project? **No** (first time)
   - Project name: **get-social-media** (or your preferred name)
   - Directory: **./** (current directory)
   - Override settings? **No**

4. **Set Environment Variables:**
   ```bash
   vercel env add GOOGLE_API_KEY
   vercel env add GOOGLE_CSE_ID
   ```
   
   Enter your values when prompted.

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Option B: Using Vercel Dashboard

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com/dashboard
   - Click **"Add New Project"**

2. **Import GitHub Repository:**
   - Select **"Import Git Repository"**
   - Choose `joegit1996/get_social_media`
   - Click **"Import"**

3. **Configure Project:**
   - Framework Preset: **Other** (or leave default)
   - Root Directory: **./** (current directory)
   - Build Command: Leave empty (Vercel will auto-detect)
   - Output Directory: Leave empty

4. **Add Environment Variables:**
   - Click **"Environment Variables"**
   - Add:
     - `GOOGLE_API_KEY` = your Google API key
     - `GOOGLE_CSE_ID` = your Google CSE ID
   - Click **"Save"**

5. **Deploy:**
   - Click **"Deploy"**
   - Wait for deployment to complete

## Step 3: Verify Deployment

After deployment, Vercel will provide you with a URL like:
- `https://get-social-media.vercel.app`

Test the API:
```bash
curl "https://your-app.vercel.app/api/find?business_name=Apple&country=USA"
```

## Project Structure for Vercel

```
get_social_media/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── templates/
│   └── index.html        # Frontend template
├── app.py                 # Main Flask application
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
└── .env                   # Local environment variables (not deployed)
```

## Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

- `GOOGLE_API_KEY`: Your Google Custom Search API key (optional)
- `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID (optional)

**Note:** The app works without these, but with lower accuracy. It will automatically fall back to web scraping.

## API Endpoints After Deployment

Once deployed, your API will be available at:

- **Homepage:** `https://your-app.vercel.app/`
- **API Endpoint:** `https://your-app.vercel.app/api/find`
- **Legacy Endpoint:** `https://your-app.vercel.app/api/search` (POST only)

## Testing the Deployed API

```bash
# GET request
curl "https://your-app.vercel.app/api/find?business_name=McDonald's&country=Kuwait"

# POST request
curl -X POST https://your-app.vercel.app/api/find \
  -H "Content-Type: application/json" \
  -d '{"business_name": "McDonald'\''s", "country": "Kuwait"}'
```

## Troubleshooting

### Issue: "Module not found" errors
- Make sure all dependencies are in `requirements.txt`
- Check that `vercel.json` is correctly configured

### Issue: Templates not found
- Ensure `templates/` folder is in the root directory
- Check that `app.py` has `template_folder='templates'`

### Issue: Environment variables not working
- Make sure variables are set in Vercel Dashboard
- Redeploy after adding environment variables
- Check variable names match exactly (case-sensitive)

### Issue: API returns errors
- Check Vercel function logs in the dashboard
- Verify the API endpoint URL is correct
- Test locally first to ensure code works

## Updating Deployment

After making changes:

```bash
# Commit changes
git add .
git commit -m "Update description"
git push

# Deploy to Vercel
vercel --prod
```

Or use Vercel's automatic deployments (if GitHub integration is enabled).

## Free Tier Limits

Vercel Free Tier includes:
- 100GB bandwidth per month
- Serverless function execution time limits
- Automatic HTTPS
- Custom domains (with limitations)

For production use with high traffic, consider Vercel Pro.

## Support

- Vercel Documentation: https://vercel.com/docs
- Flask on Vercel: https://vercel.com/docs/functions/serverless-functions/runtimes/python

