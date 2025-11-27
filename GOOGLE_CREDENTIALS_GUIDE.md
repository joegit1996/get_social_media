# Detailed Guide: Creating API Credentials in Google Cloud Console

This guide provides step-by-step instructions with detailed explanations for creating API credentials in Google Cloud Console.

## Prerequisites

- A Google account
- A Google Cloud project (if you don't have one, see Step 1 below)

---

## Step 1: Create or Select a Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project** (if you don't have one)
   - Click on the **project dropdown** at the top of the page (next to "Google Cloud")
   - Click **"New Project"** button
   - Enter a project name (e.g., "Social Media Finder" or "Business Social Links")
   - Optionally, select an organization (if you're part of one)
   - Click **"Create"**
   - Wait 10-30 seconds for the project to be created

3. **Select Your Project**
   - Click the project dropdown again
   - Select the project you just created (or an existing one)

---

## Step 2: Enable Custom Search API

1. **Navigate to APIs & Services**
   - In the left sidebar, click **"APIs & Services"**
   - Then click **"Library"** (or go directly to: https://console.cloud.google.com/apis/library)

2. **Search for Custom Search API**
   - In the search bar at the top, type: **"Custom Search API"**
   - Click on **"Custom Search API"** from the results

3. **Enable the API**
   - Click the blue **"Enable"** button
   - Wait for the API to be enabled (you'll see a success message)
   - You should now see "API enabled" with a green checkmark

---

## Step 3: Create API Credentials (API Key)

### Method A: From the API Page

1. **After enabling the API**, you'll see a page with API details
2. Click **"Go to credentials"** button (or click **"Credentials"** in the left sidebar)

### Method B: Direct Navigation

1. In the left sidebar, click **"APIs & Services"**
2. Click **"Credentials"**

### Creating the API Key

**Method 1: Direct from Credentials Page (Standard Method)**

1. **Click "Create Credentials"**
   - At the top of the page, click the **"+ CREATE CREDENTIALS"** button
   - A dropdown menu will appear

2. **Select "API Key"**
   - If you see **"API key"** in the dropdown, click it
   - Your API key will be **immediately created and displayed** in a popup dialog
   - Skip to step 3 below

**Method 2: If "API Key" is NOT in the dropdown menu**

If you see options like:
- "OAuth client ID"
- "Service Account"
- "Help me choose"
- But NOT "API key"

Try these alternatives:

**Alternative A: From the API Page**
1. Go back to **"APIs & Services"** > **"Library"**
2. Search for and click on **"Custom Search API"**
3. Click the **"Credentials"** tab at the top
4. Click **"Create Credentials"** → **"API Key"**
5. This should create the API key

**Alternative B: Use "Help me choose"**
1. Click **"+ CREATE CREDENTIALS"**
2. Select **"Help me choose"** (if available)
3. Answer the questions:
   - **Which API are you using?** → Select "Custom Search API"
   - **Where will you be calling the API from?** → Select "Other UI (e.g. Windows, CLI tool)"
   - **What data will you be accessing?** → Select "Application data"
4. Click **"What credentials do I need?"**
5. It should suggest creating an API key - click **"Create API key"**

**Alternative C: Direct URL Method**
1. Make sure you have the Custom Search API enabled (Step 2)
2. Go directly to this URL (replace `YOUR_PROJECT_ID` with your actual project ID):
   ```
   https://console.cloud.google.com/apis/credentials?project=YOUR_PROJECT_ID
   ```
3. Or try: https://console.cloud.google.com/apis/credentials
4. Look for a section that says **"API keys"** and click **"Create API key"** or **"+ CREATE CREDENTIALS"** → **"API Key"**

**Alternative D: Check if API Key section exists**
1. On the Credentials page, scroll down
2. Look for a section titled **"API keys"** (separate from OAuth 2.0 Client IDs)
3. If you see this section, click **"Create API key"** or **"+ CREATE"** within that section

3. **Copy Your API Key**
   - **IMPORTANT**: Copy the API key now (it looks like: `AIzaSyD...` - a long string)
   - Save it somewhere safe (you won't be able to see it again in full)
   - Click **"Close"** in the dialog

4. **Secure Your API Key** (Highly Recommended)
   
   **Why restrict?** Unrestricted API keys can be used by anyone who gets them, potentially costing you money.
   
   **How to restrict:**
   - Find your newly created API key in the credentials list
   - Click on the **API key name** (or click the pencil/edit icon)
   - Under **"API restrictions"**:
     - Select **"Restrict key"**
     - In the dropdown, check **"Custom Search API"**
     - Uncheck any other APIs if they're selected
   - Under **"Application restrictions"** (optional but recommended):
     - You can leave it as "None" for local development
     - Or select "HTTP referrers" and add `http://localhost:5000/*` for web restrictions
   - Click **"Save"** at the bottom
   - Wait for the changes to be saved

---

## Step 4: Verify Your API Key

1. **Check the API Key Status**
   - In the Credentials page, you should see your API key listed
   - It should show:
     - **Key name**: (the name you gave it, or "API key 1" by default)
     - **Type**: API key
     - **Status**: Enabled (with a green checkmark)

2. **Test the API Key** (Optional)
   - You can test it by making a simple API call, but the easiest way is to just use it in your application

---

## Step 5: Get Your Search Engine ID (CSE ID)

The API key alone isn't enough - you also need a Custom Search Engine ID.

1. **Go to Google Custom Search**
   - Visit: https://cse.google.com/cse/all
   - Sign in with the **same Google account** you used for Google Cloud

2. **Create a New Search Engine**
   - Click the **"Add"** button (usually a blue button or "+" icon)
   - You'll see a form to create a new search engine

3. **Fill in the Search Engine Details**
   - **Sites to search**: 
     - Option 1: Leave this **empty** to search the entire web (recommended for finding social media links)
     - Option 2: Enter `instagram.com` and `facebook.com` (one per line) to search only these sites
   - **Name of the search engine**: Enter a name (e.g., "Social Media Finder")
   - **Language**: Select your preferred language (or leave default)

4. **Create the Search Engine**
   - Click **"Create"** button
   - Wait for it to be created

5. **Get Your Search Engine ID**
   - After creation, you'll be taken to the control panel
   - Click on **"Setup"** in the left menu
   - Click on **"Basics"**
   - Look for **"Search engine ID"** (also called "CX" or "CSE ID")
   - It looks like: `017576662512468239146:omuauf_lfve` (a long string with numbers and letters)
   - **Copy this ID** and save it with your API key

---

## Step 6: Configure Your Application

Now that you have both credentials, configure your application:

### Option 1: Using .env File (Easiest)

1. **Create a `.env` file** in your project root directory (`/Users/joe/get social media links/`)

2. **Add your credentials**:
   ```
   GOOGLE_API_KEY=AIzaSyD...your-actual-api-key-here
   GOOGLE_CSE_ID=017576662512468239146:omuauf_lfve
   ```
   (Replace with your actual values)

3. **Save the file**

4. **Restart your Flask application** - it will automatically load these values

### Option 2: Using Environment Variables

**On macOS/Linux:**
```bash
export GOOGLE_API_KEY="AIzaSyD...your-actual-api-key-here"
export GOOGLE_CSE_ID="017576662512468239146:omuauf_lfve"
```

**On Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=AIzaSyD...your-actual-api-key-here
set GOOGLE_CSE_ID=017576662512468239146:omuauf_lfve
```

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="AIzaSyD...your-actual-api-key-here"
$env:GOOGLE_CSE_ID="017576662512468239146:omuauf_lfve"
```

---

## Visual Guide: Where to Find Everything

### Google Cloud Console Navigation:
```
Google Cloud Console
├── Project Selector (top bar)
├── APIs & Services
│   ├── Library (to enable APIs)
│   └── Credentials (to create API keys)
└── Billing (if you need to set up billing)
```

### Google Custom Search Navigation:
```
Google Custom Search
├── All search engines (list of your engines)
└── [Your Search Engine]
    ├── Setup
    │   └── Basics (contains Search Engine ID)
    ├── Public URL
    └── Control Panel
```

---

## Common Issues & Solutions

### Issue: "API key not valid" error
**Solutions:**
- Make sure you copied the entire API key (they're long strings)
- Verify the Custom Search API is enabled in your project
- Check that your API key restrictions allow Custom Search API
- Wait a few minutes after creating the key (sometimes there's a short delay)

### Issue: "Search engine ID not found" error
**Solutions:**
- Verify you copied the entire Search Engine ID
- Make sure you're using the same Google account for both Cloud Console and Custom Search
- Check that the search engine is active (not deleted)

### Issue: "Quota exceeded" error
**Solutions:**
- Google Custom Search API has 100 free queries per day
- Check your quota usage in Google Cloud Console → APIs & Services → Dashboard
- Wait until the next day, or set up billing for more queries
- The app will automatically fall back to web scraping if quota is exceeded

### Issue: Can't find "Create Credentials" button
**Solutions:**
- Make sure you have the correct permissions (you need to be a project owner or editor)
- Try refreshing the page
- Make sure you've selected the correct project

### Issue: "API Key" option not showing in Create Credentials dropdown
**Solutions:**
- **Make sure Custom Search API is enabled first** (Step 2) - this is crucial!
- Try Method 2 (Alternative A) - go to the API page and create from there
- Check if there's a separate "API keys" section on the Credentials page
- Make sure you're in the correct project
- Try using the direct URL: `https://console.cloud.google.com/apis/credentials`
- If still not showing, you might need to enable billing (though API keys should work without billing for the free tier)

---

## Security Checklist

- ✅ API key is restricted to Custom Search API only
- ✅ API key is saved in `.env` file (not committed to git)
- ✅ `.env` is in `.gitignore` (already included in the project)
- ✅ Search Engine ID is kept private
- ✅ Never share your API keys publicly

---

## Next Steps

Once you've set up your credentials:

1. **Test your setup:**
   ```bash
   python app.py
   ```
   Then visit `http://localhost:5000` and try a search

2. **Check the console output** - if you see "Google API search error", check your credentials

3. **Verify it's working** - when you search, you should see "Google Custom Search API" in the sources list

---

## Need More Help?

- **Google Cloud Console Help**: https://cloud.google.com/docs
- **Custom Search API Documentation**: https://developers.google.com/custom-search/v1/overview
- **API Key Best Practices**: https://cloud.google.com/docs/authentication/api-keys

---

**Remember**: Keep your API keys secure and never commit them to version control!

