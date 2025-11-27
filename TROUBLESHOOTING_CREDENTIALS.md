# Troubleshooting: API Key Not Showing in Create Credentials

If you don't see "API Key" as an option when clicking "Create Credentials", here are solutions:

## Quick Fixes

### ✅ Solution 1: Enable the API First (Most Common Issue)

**The API must be enabled before you can create an API key for it!**

1. Go to **APIs & Services** → **Library**
2. Search for **"Custom Search API"**
3. Click on it and click **"Enable"**
4. Wait for it to enable (you'll see a success message)
5. **Now go back** to **APIs & Services** → **Credentials**
6. Try creating the API key again

### ✅ Solution 2: Create from the API Page

1. Go to **APIs & Services** → **Library**
2. Click on **"Custom Search API"** (make sure it's enabled)
3. Click the **"Credentials"** tab at the top of the page
4. Click **"Create Credentials"** → **"API Key"**
5. This should work even if the main Credentials page doesn't show it

### ✅ Solution 3: Look for "API Keys" Section

On the Credentials page:
1. Scroll down past "OAuth 2.0 Client IDs" and "Service Accounts"
2. Look for a section titled **"API keys"**
3. Click **"+ CREATE API KEY"** or **"Create API key"** in that section

### ✅ Solution 4: Use Direct Navigation

1. Make sure you're in the correct project
2. Go directly to: `https://console.cloud.google.com/apis/credentials`
3. Look for the API keys section
4. Or try: `https://console.cloud.google.com/apis/credentials/key`

## What Options Are You Seeing?

### If you see:
- **"OAuth client ID"** → This is for web apps with user login (not what we need)
- **"Service Account"** → This is for server-to-server (not what we need)
- **"Help me choose"** → Use this! It will guide you to create an API key

### If you see "Help me choose":
1. Click **"Help me choose"**
2. Select **"Custom Search API"** as the API
3. Select **"Other UI"** or **"Web browser"** as where you're calling from
4. Select **"Application data"** as what you're accessing
5. Click **"What credentials do I need?"**
6. It should suggest **"API Key"** - click **"Create API key"**

## Common Reasons API Key Option Doesn't Show

1. **API not enabled** (most common) - Enable Custom Search API first
2. **Wrong project selected** - Check the project dropdown at the top
3. **Insufficient permissions** - You need to be Owner or Editor of the project
4. **Billing not set up** - Some projects require billing, but API keys should work without it for free tier
5. **New project** - Sometimes there's a delay, wait a minute and refresh

## Step-by-Step: Complete Workflow

If nothing above works, follow this complete workflow:

1. **Create/Select Project**
   - Go to https://console.cloud.google.com/
   - Select or create a project

2. **Enable Custom Search API** (CRITICAL STEP)
   - Go to: https://console.cloud.google.com/apis/library
   - Search: "Custom Search API"
   - Click it → Click "Enable"
   - Wait for confirmation

3. **Create API Key from API Page**
   - Stay on the Custom Search API page
   - Click **"Credentials"** tab (at the top, next to "Overview")
   - Click **"+ CREATE CREDENTIALS"**
   - Select **"API Key"**
   - Copy the key immediately

4. **Restrict the Key**
   - Click on the key name in the list
   - Under "API restrictions" → Select "Restrict key"
   - Check "Custom Search API"
   - Click "Save"

## Still Not Working?

### Check These:

- [ ] Is Custom Search API enabled? (Go to APIs & Services → Library → Search for it)
- [ ] Are you in the correct project? (Check the project dropdown at top)
- [ ] Do you have Owner/Editor permissions?
- [ ] Have you tried refreshing the page?
- [ ] Have you tried a different browser?
- [ ] Is your Google account a personal account or workspace account? (Both should work)

### Alternative: Contact Support

If none of the above works:
1. Go to: https://console.cloud.google.com/support
2. Create a support case
3. Mention: "Cannot create API key for Custom Search API - option not showing in Create Credentials"

## Remember

**The key point**: You MUST enable the Custom Search API BEFORE you can create an API key for it. This is the #1 reason the option doesn't show!

---

**Need more help?** Check the main guide: [GOOGLE_CREDENTIALS_GUIDE.md](GOOGLE_CREDENTIALS_GUIDE.md)



