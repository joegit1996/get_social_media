# Google Custom Search API Setup Guide

This guide will walk you through setting up Google Custom Search API to improve the accuracy of social media link searches.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top
4. Click **"New Project"**
5. Enter a project name (e.g., "Social Media Finder")
6. Click **"Create"**
7. Wait for the project to be created, then select it from the dropdown

## Step 2: Enable Custom Search API

1. In the Google Cloud Console, go to **"APIs & Services"** > **"Library"**
2. Search for **"Custom Search API"**
3. Click on **"Custom Search API"**
4. Click the **"Enable"** button
5. Wait for the API to be enabled (this may take a minute)

## Step 3: Create API Credentials

> **📖 For detailed step-by-step instructions with screenshots guidance, see [GOOGLE_CREDENTIALS_GUIDE.md](GOOGLE_CREDENTIALS_GUIDE.md)**

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API Key"**
4. Your API key will be created and displayed
5. **Important**: Click **"RESTRICT KEY"** to secure it:
   - Under **"API restrictions"**, select **"Restrict key"**
   - Choose **"Custom Search API"** from the list
   - Click **"Save"**
6. Copy your API key and save it securely (you'll need it in Step 6)

**Quick Tips:**
- Copy the API key immediately - you won't see it in full again
- Restrict the key to Custom Search API only for security
- The API key looks like: `AIzaSyD...` (a long string)

## Step 4: Create a Custom Search Engine

1. Go to [Google Custom Search](https://cse.google.com/cse/all)
2. Sign in with the same Google account
3. Click **"Add"** to create a new search engine
4. In the **"Sites to search"** field, you can enter:
   - `instagram.com` (to search Instagram)
   - `facebook.com` (to search Facebook)
   - Or leave it empty to search the entire web (recommended for this use case)
5. Enter a name for your search engine (e.g., "Social Media Finder")
6. Click **"Create"**

## Step 5: Get Your Search Engine ID (CSE ID)

1. After creating the search engine, you'll see a list of your search engines
2. Click on the search engine you just created
3. Go to **"Setup"** > **"Basics"**
4. Find the **"Search engine ID"** (it looks like: `017576662512468239146:omuauf_lfve`)
5. Copy this ID and save it (you'll need it in Step 6)

## Step 6: Configure Your Application

You have two options to configure the API keys:

### Option A: Environment Variables (Recommended)

**On macOS/Linux:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
export GOOGLE_CSE_ID="your-search-engine-id-here"
```

**On Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your-api-key-here
set GOOGLE_CSE_ID=your-search-engine-id-here
```

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
$env:GOOGLE_CSE_ID="your-search-engine-id-here"
```

### Option B: Using a .env File

1. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file in your project root:
   ```
   GOOGLE_API_KEY=your-api-key-here
   GOOGLE_CSE_ID=your-search-engine-id-here
   ```

3. Update `app.py` to load the .env file (add at the top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Step 7: Test Your Setup

1. Start your Flask application:
   ```bash
   python app.py
   ```

2. Open `http://localhost:5000` in your browser

3. Try searching for a business (e.g., "McDonald's", "Kuwait")

4. Check the console output - if you see "Google API search error", there might be an issue with your setup

## Troubleshooting

### "API key not valid" error
- Make sure you copied the API key correctly
- Verify the Custom Search API is enabled in your project
- Check that your API key restrictions allow Custom Search API

### "Search engine ID not found" error
- Verify you copied the Search Engine ID correctly
- Make sure the search engine is active in Google Custom Search

### "Quota exceeded" error
- Google Custom Search API has a free tier: 100 queries per day
- After that, you'll need to set up billing
- The application will automatically fall back to web scraping if the API fails

### API not working but no errors
- Check that environment variables are set correctly
- Restart your Flask application after setting environment variables
- Verify the API key has the correct restrictions

## Free Tier Limits

- **100 free queries per day** for Custom Search API
- After 100 queries, you'll need to enable billing or wait until the next day
- The application automatically falls back to web scraping methods if the API quota is exceeded

## Security Best Practices

1. **Never commit your API keys to version control**
   - Add `.env` to `.gitignore` (already included)
   - Don't share your API keys publicly

2. **Restrict your API key**
   - Only allow Custom Search API
   - Consider adding IP restrictions if deploying to a server

3. **Rotate keys if compromised**
   - If you suspect your key is compromised, delete it and create a new one

## Next Steps

Once set up, your application will:
- Use Google Custom Search API for more accurate results
- Automatically fall back to web scraping if the API is unavailable
- Show "Google Custom Search API" in the sources when using the API

Enjoy more accurate social media link finding! 🎉

