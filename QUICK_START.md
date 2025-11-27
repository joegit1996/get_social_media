# Quick Start Guide

## Fastest Way to Get Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Without API (Basic Mode)
```bash
python app.py
```
Then visit: http://localhost:5000

**This works immediately** but with lower accuracy. The app uses web scraping as a fallback.

### 3. For Better Accuracy: Set Up Google API (5 minutes)

**Option A: Using .env file (Recommended)**
1. Create a `.env` file in the project root
2. Add these lines:
   ```
   GOOGLE_API_KEY=your-api-key-here
   GOOGLE_CSE_ID=your-search-engine-id-here
   ```
3. Follow the detailed guides to get your credentials:
   - **For creating credentials**: See [GOOGLE_CREDENTIALS_GUIDE.md](GOOGLE_CREDENTIALS_GUIDE.md)
   - **For full setup**: See [GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)

**Option B: Using environment variables**
```bash
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-cse-id"
python app.py
```

### 4. Test It!
1. Open http://localhost:5000
2. Enter: Business Name = "McDonald's", Country = "Kuwait"
3. Click "Search Social Media Links"
4. Check the results!

---

## Which Guide Should I Read?

- **Just want to run it?** → This file (QUICK_START.md)
- **Need to create API credentials?** → [GOOGLE_CREDENTIALS_GUIDE.md](GOOGLE_CREDENTIALS_GUIDE.md)
- **Full API setup instructions?** → [GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)
- **General project info?** → [README.md](README.md)

---

## Troubleshooting

**App won't start?**
- Make sure Flask is installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

**No results found?**
- Try different business name variations
- Check if the business has public social media pages
- If using API: Verify your credentials are correct

**API errors?**
- Check your API key and CSE ID are correct
- Verify Custom Search API is enabled
- Check if you've exceeded the 100 queries/day free limit



