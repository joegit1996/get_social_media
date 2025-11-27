# Business Social Media Finder

A web application that finds Instagram and Facebook social media links for businesses based on their name and country.

## Features

- 🔍 **Multi-source Search**: Uses multiple methods to find social media links
  - Google Custom Search API (recommended for accuracy)
  - Google Web Search (fallback)
  - Direct Instagram/Facebook URL pattern matching
- ✅ **Link Verification**: Verifies that found links are valid and match the business
- 🎯 **Confidence Scoring**: Provides confidence levels (high/medium/low) for results
- 🎨 **Modern UI**: Clean, responsive web interface

## How It Works

### Search Methods

1. **Google Custom Search API** (if configured)
   - Most accurate method
   - Searches specifically for Instagram and Facebook pages
   - Requires API key setup

2. **Google Web Search** (fallback)
   - Scrapes Google search results
   - Extracts social media links from search results

3. **Direct URL Pattern Matching**
   - Generates possible username variations from business name
   - Tests common URL patterns
   - Verifies each potential link

### Verification & Accuracy

The system ensures accuracy through:

1. **Link Validation**: Checks if links return valid pages (not 404 errors)
2. **Business Name Matching**: Compares business name with page titles using similarity algorithms
3. **Multiple Source Cross-referencing**: Uses multiple search methods and compares results
4. **Confidence Scoring**: 
   - **High**: Both Instagram and Facebook links found and verified
   - **Medium**: One verified link found
   - **Low**: No verified links found

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - Flask (web framework)
   - flask-cors (CORS support)
   - requests (HTTP library)
   - python-dotenv (for .env file support)

3. **Optional: Set up Google Custom Search API** (recommended for better accuracy)
   
   To get more accurate results, you can set up Google Custom Search API:
   
   a. Go to [Google Cloud Console](https://console.cloud.google.com/)
   b. Create a new project or select an existing one
   c. Enable the "Custom Search API"
   d. Create credentials (API Key)
   e. Set up a Custom Search Engine at [Google Custom Search](https://cse.google.com/)
   f. Get your Search Engine ID (CSE ID)
   
   g. Set environment variables:
   
   **Option 1: Using a .env file (Recommended)**:
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your-api-key-here
   GOOGLE_CSE_ID=your-cse-id-here
   ```
   
   **Option 2: Using environment variables**:
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   export GOOGLE_CSE_ID="your-cse-id-here"
   ```
   
   For detailed setup instructions, see [GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)

## Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Enter a business name and country** (e.g., "McDonald's" and "Kuwait")

4. **Click "Search Social Media Links"**

5. **View the results** with confidence levels and source information

## Example

Input:
- Business Name: `McDonald's`
- Country: `Kuwait`

Output:
- Instagram: `https://www.instagram.com/mcdonaldskuwait/`
- Facebook: `https://www.facebook.com/McDonaldsKuwait/`
- Confidence: `HIGH`
- Sources: `Google Custom Search API, Instagram Direct Search`

## Limitations & Notes

1. **Rate Limiting**: Web scraping methods include delays to be respectful of servers
2. **API Requirements**: Some methods require API keys for optimal performance
3. **Privacy Settings**: Some social media pages may be private or restricted
4. **Name Variations**: Businesses may use different names on social media than their official name
5. **Regional Variations**: Some businesses have country-specific pages that may not be found

## API Quota & Fallbacks

The application has **automatic fallbacks** if you reach Google Custom Search API limits:

### Free Tier Limits
- **100 free queries per day** for Google Custom Search API
- After 100 queries, the API will return quota errors

### Automatic Fallback System

When the API quota is exceeded, the app **automatically falls back** to:

1. **Google Web Search (Web Scraping)**: Scrapes Google search results directly
   - No API limits
   - Slightly less accurate but still effective
   - Respects rate limiting (1 second delays)

2. **Direct URL Pattern Matching**: Tries common username variations
   - Works independently of APIs
   - Very fast and accurate for businesses with predictable usernames
   - Uses country code variations (e.g., `mbvisionkw`)

3. **Multiple Search Methods**: The app tries all methods in parallel
   - If one fails, others continue working
   - Results are cross-referenced for accuracy

### Error Handling

The app detects quota errors (HTTP 403, 429) and automatically:
- Logs the quota error
- Switches to fallback methods
- Continues searching without interruption
- Shows "Google Web Search" in sources instead of "Google Custom Search API"

**You don't need to do anything** - the fallback happens automatically!

## Improving Accuracy

To improve the accuracy of results:

1. **Use Google Custom Search API**: This is the most reliable method
2. **Be specific with business names**: Include full business names when possible
3. **Include location context**: The country parameter helps narrow down results
4. **Verify manually**: Always verify important links manually before using them

## Troubleshooting

- **No results found**: Try different variations of the business name or check if the business has public social media pages
- **Low confidence results**: The system couldn't verify the links - manually check before using
- **API errors**: Make sure your Google API key is valid and has the Custom Search API enabled

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

