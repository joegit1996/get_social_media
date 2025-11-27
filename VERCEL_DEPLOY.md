# Quick Vercel Deployment Guide

## Quick Start

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Deploy via Vercel Dashboard:**
   - Go to https://vercel.com/new
   - Import `joegit1996/get_social_media`
   - Add environment variables:
     - `GOOGLE_API_KEY`
     - `GOOGLE_CSE_ID`
   - Click Deploy

3. **Or use Vercel CLI:**
   ```bash
   npm install -g vercel
   vercel login
   vercel
   vercel env add GOOGLE_API_KEY
   vercel env add GOOGLE_CSE_ID
   vercel --prod
   ```

## Project Structure

- `api/index.py` - Vercel serverless function entry point
- `app.py` - Main Flask application
- `vercel.json` - Vercel configuration
- `templates/` - HTML templates

## API Endpoints

After deployment:
- `https://your-app.vercel.app/api/find?business_name=Apple&country=USA`
- `https://your-app.vercel.app/` - Web interface

