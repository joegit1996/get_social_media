# API Documentation

Simple REST API to find social media links for businesses.

## Base URL

```
http://localhost:5001
```

## Endpoint

### `/api/find`

Find Instagram, Facebook, and website links for a business.

**Methods:** `GET` or `POST`  
**Authentication:** None required

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `business_name` | string | Yes | Name of the business |
| `country` | string | No | Country name (e.g., "Kuwait", "USA") |

#### Request Examples

**GET Request:**
```bash
curl "http://localhost:5001/api/find?business_name=McDonald's&country=Kuwait"
```

**POST Request (JSON):**
```bash
curl -X POST http://localhost:5001/api/find \
  -H "Content-Type: application/json" \
  -d '{"business_name": "McDonald'\''s", "country": "Kuwait"}'
```

**POST Request (Form Data):**
```bash
curl -X POST http://localhost:5001/api/find \
  -d "business_name=McDonald's&country=Kuwait"
```

**Without Country (Optional):**
```bash
curl "http://localhost:5001/api/find?business_name=Apple"
```

#### Response Format

**Success Response (200 OK):**
```json
{
  "business_name": "McDonald's",
  "country": "Kuwait",
  "instagram": "https://www.instagram.com/mcdonaldskuwait/",
  "facebook": "https://www.facebook.com/mcdonaldskuwait/",
  "website": "https://www.mcdonalds.com.kw/",
  "confidence": "high",
  "sources": [
    "Google Custom Search API",
    "Instagram Direct Search",
    "Facebook Direct Search"
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "business_name parameter is required"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Error message here"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `business_name` | string | The business name that was searched |
| `country` | string or null | The country that was searched (null if not provided) |
| `instagram` | string or null | Instagram URL if found |
| `facebook` | string or null | Facebook URL if found |
| `website` | string or null | Official website URL if found |
| `confidence` | string | Confidence level: "high", "medium", or "low" |
| `sources` | array | List of search methods used |

#### Confidence Levels

- **high**: 2+ links found and verified
- **medium**: 1 link found and verified
- **low**: No verified links found

#### Example Usage

**JavaScript (Fetch):**
```javascript
fetch('http://localhost:5001/api/find?business_name=McDonald\'s&country=Kuwait')
  .then(response => response.json())
  .then(data => {
    console.log('Instagram:', data.instagram);
    console.log('Facebook:', data.facebook);
    console.log('Website:', data.website);
  });
```

**Python (Requests):**
```python
import requests

response = requests.get(
    'http://localhost:5001/api/find',
    params={'business_name': "McDonald's", 'country': 'Kuwait'}
)
data = response.json()
print(f"Instagram: {data['instagram']}")
print(f"Facebook: {data['facebook']}")
print(f"Website: {data['website']}")
```

**cURL:**
```bash
# GET request
curl "http://localhost:5001/api/find?business_name=McDonald's&country=Kuwait"

# POST request
curl -X POST http://localhost:5001/api/find \
  -H "Content-Type: application/json" \
  -d '{"business_name": "McDonald'\''s", "country": "Kuwait"}'
```

#### Notes

- Country parameter is optional but recommended for better accuracy
- The API automatically falls back to web scraping if Google API quota is exceeded
- Results are verified to ensure links are valid and match the business
- No authentication or API keys required for this endpoint

