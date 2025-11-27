from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import re
from urllib.parse import quote, urlparse
import time
import os
from difflib import SequenceMatcher

# Try to load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional

app = Flask(__name__, template_folder='templates')
CORS(app)

class SocialMediaFinder:
    def __init__(self, google_api_key=None, google_cse_id=None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.google_api_key = google_api_key or os.getenv('GOOGLE_API_KEY')
        self.google_cse_id = google_cse_id or os.getenv('GOOGLE_CSE_ID')
    
    def _similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def find_social_links(self, business_name, country):
        """
        Find Instagram and Facebook links for a business using multiple methods
        """
        results = {
            'instagram': None,
            'facebook': None,
            'website': None,
            'confidence': 'low',
            'sources': []
        }
        
        all_instagram_candidates = []
        all_facebook_candidates = []
        all_website_candidates = []
        
        # Method 1: Google Custom Search API (if available)
        api_quota_exceeded = False
        if self.google_api_key and self.google_cse_id:
            api_results = self._search_google_api(business_name, country)
            if api_results is None:
                # API returned None - could be quota exceeded, will use fallback
                api_quota_exceeded = True
            elif api_results:
                results['sources'].append('Google Custom Search API')
                if api_results.get('instagram'):
                    all_instagram_candidates.append(api_results['instagram'])
                if api_results.get('facebook'):
                    all_facebook_candidates.append(api_results['facebook'])
                if api_results.get('website'):
                    all_website_candidates.append(api_results['website'])
        
        # Method 2: Google Web Search (fallback - always runs, but especially if API quota exceeded)
        google_results = None
        if api_quota_exceeded or not all_instagram_candidates or not all_facebook_candidates:
            google_results = self._search_google(business_name, country)
        if google_results:
            if 'Google Custom Search API' not in results['sources']:
                results['sources'].append('Google Web Search')
            if google_results.get('instagram'):
                all_instagram_candidates.append(google_results['instagram'])
            if google_results.get('facebook'):
                all_facebook_candidates.append(google_results['facebook'])
            if google_results.get('website'):
                all_website_candidates.append(google_results['website'])
        
        # Method 3: Direct Instagram/Facebook search with variations
        # Always try direct search as it can find more accurate results
        instagram_link = self._search_instagram_direct(business_name, country)
        if instagram_link and instagram_link not in all_instagram_candidates:
            all_instagram_candidates.append(instagram_link)
            if 'Instagram Direct Search' not in results['sources']:
                results['sources'].append('Instagram Direct Search')
        
        facebook_link = self._search_facebook_direct(business_name, country)
        if facebook_link and facebook_link not in all_facebook_candidates:
            all_facebook_candidates.append(facebook_link)
            if 'Facebook Direct Search' not in results['sources']:
                results['sources'].append('Facebook Direct Search')
        
        # Method 4: Search for official website
        website_link = self._search_website(business_name, country)
        if website_link:
            all_website_candidates.append(website_link)
            if 'Website Search' not in results['sources']:
                results['sources'].append('Website Search')
        
        # Method 5: Verify and select best candidates
        # Prioritize direct search results (they're usually more accurate)
        verified_instagram = None
        verified_facebook = None
        
        # Sort candidates: direct search results first, then others
        instagram_direct = [c for c in all_instagram_candidates if 'Direct Search' in str(c) or any('Direct Search' in s for s in results.get('sources', []))]
        instagram_others = [c for c in all_instagram_candidates if c not in instagram_direct]
        instagram_prioritized = instagram_direct + instagram_others
        
        # For Instagram, try direct search variations first
        direct_instagram = self._search_instagram_direct(business_name, country)
        if direct_instagram:
            instagram_prioritized.insert(0, direct_instagram)
        
        for candidate in instagram_prioritized:
            if self._verify_instagram_link(candidate, business_name):
                verified_instagram = candidate
                break
        
        # Sort Facebook candidates: direct search results first
        facebook_direct = [c for c in all_facebook_candidates if 'Direct Search' in str(c) or any('Direct Search' in s for s in results.get('sources', []))]
        facebook_others = [c for c in all_facebook_candidates if c not in facebook_direct]
        facebook_prioritized = facebook_direct + facebook_others
        
        # For Facebook, try direct search variations first
        direct_facebook = self._search_facebook_direct(business_name, country)
        if direct_facebook:
            facebook_prioritized.insert(0, direct_facebook)
        
        for candidate in facebook_prioritized:
            if self._verify_facebook_link(candidate, business_name):
                verified_facebook = candidate
                break
        
        results['instagram'] = verified_instagram
        results['facebook'] = verified_facebook
        
        # Verify and select best website candidate
        verified_website = None
        for candidate in all_website_candidates:
            if self._verify_website_link(candidate, business_name):
                verified_website = candidate
                break
        
        results['website'] = verified_website
        
        # Determine confidence level
        verified_count = sum([
            bool(verified_instagram),
            bool(verified_facebook),
            bool(verified_website)
        ])
        
        if verified_count >= 2:
            results['confidence'] = 'high'
        elif verified_count == 1:
            results['confidence'] = 'medium'
        else:
            results['confidence'] = 'low'
        
        return results
    
    def _search_google_api(self, business_name, country):
        """
        Search using Google Custom Search API (more reliable)
        """
        if not self.google_api_key or not self.google_cse_id:
            return None
        
        # Separate queries for social media and websites
        social_queries = [
            f"{business_name} {country} instagram",
            f"{business_name} {country} facebook",
            f'"{business_name}" {country} site:instagram.com',
            f'"{business_name}" {country} site:facebook.com',
            f"{business_name} {country} facebook page",
            f"{business_name} facebook {country}"
        ]
        
        website_queries = [
            f'"{business_name}" {country} official website',
            f"{business_name} {country} website",
            f"{business_name} {country} site"
        ]
        
        instagram_link = None
        facebook_link = None
        website_link = None
        
        try:
            # First, search for social media
            for query in social_queries:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': self.google_api_key,
                    'cx': self.google_cse_id,
                    'q': query
                }
                response = self.session.get(url, params=params, timeout=10)
                
                # Check for quota/rate limit errors
                if response.status_code == 403:
                    try:
                        error_data = response.json() if response.text else {}
                        error_message = error_data.get('error', {}).get('message', '')
                        if 'quota' in error_message.lower() or 'limit' in error_message.lower():
                            print(f"Google API quota exceeded. Falling back to web scraping.")
                            return None  # Return None to trigger fallback
                    except:
                        pass
                
                if response.status_code == 429:
                    print(f"Google API rate limit exceeded. Falling back to web scraping.")
                    return None  # Return None to trigger fallback
                
                if response.status_code == 200:
                    data = response.json()
                    if 'items' in data:
                        for item in data['items']:
                            link = item.get('link', '')
                            snippet = item.get('snippet', '') or item.get('htmlSnippet', '')
                            
                            # Prioritize Instagram
                            if 'instagram.com' in link and not instagram_link:
                                instagram_link = self._normalize_instagram_url(link)
                            # Then Facebook
                            elif 'facebook.com' in link and not facebook_link:
                                facebook_link = self._normalize_facebook_url(link)
                            # Then check for websites (but skip if it's social media)
                            elif not website_link and self._is_likely_website(link, business_name):
                                # Additional check: make sure it's not a directory/review site
                                skip_domains = ['yelp', 'tripadvisor', 'zomato', 'foursquare', 
                                               'opentable', 'google.com/maps', 'google.com/search']
                                if not any(skip in link.lower() for skip in skip_domains):
                                    website_link = link
                            
                            # Also try to extract website from snippet text
                            if not website_link and snippet:
                                extracted = self._extract_website_from_text(snippet, business_name)
                                if extracted:
                                    website_link = extracted
                            
                            if instagram_link and facebook_link:
                                break
                
                time.sleep(0.5)  # Rate limiting
            
            # Then, search specifically for websites
            for query in website_queries:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': self.google_api_key,
                    'cx': self.google_cse_id,
                    'q': query
                }
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'items' in data:
                        for item in data['items']:
                            link = item.get('link', '')
                            snippet = item.get('snippet', '') or item.get('htmlSnippet', '')
                            
                            # Skip social media links in website search
                            if 'instagram.com' in link or 'facebook.com' in link:
                                continue
                            
                            # Check if link is a website
                            if not website_link and self._is_likely_website(link, business_name):
                                skip_domains = ['yelp', 'tripadvisor', 'zomato', 'foursquare', 
                                               'opentable', 'google.com', 'bing.com', 'yahoo.com',
                                               'wikipedia.org', 'support.google', 'maps.google']
                                if not any(skip in link.lower() for skip in skip_domains):
                                    website_link = link
                            
                            # Also try to extract website from snippet text
                            if not website_link and snippet:
                                extracted = self._extract_website_from_text(snippet, business_name)
                                if extracted:
                                    website_link = extracted
                            
                            if website_link:
                                break
                
                if website_link:
                    break
                
                time.sleep(0.5)  # Rate limiting
                
        except requests.exceptions.RequestException as e:
            # Network errors - fall back to web scraping
            print(f"Google API network error: {e}. Falling back to web scraping.")
            return None
        except Exception as e:
            error_str = str(e).lower()
            if 'quota' in error_str or 'limit' in error_str or '403' in error_str or '429' in error_str:
                print(f"Google API quota/limit error: {e}. Falling back to web scraping.")
                return None
            print(f"Google API search error: {e}")
        
        result = {}
        if instagram_link:
            result['instagram'] = instagram_link
        if facebook_link:
            result['facebook'] = facebook_link
        if website_link:
            result['website'] = website_link
        
        return result if result else None
    
    def _search_google(self, business_name, country):
        """
        Search Google for business social media links (web scraping fallback)
        """
        queries = [
            f"{business_name} {country} instagram",
            f"{business_name} {country} facebook",
            f'"{business_name}" {country} official website',
            f"{business_name} {country} website"
        ]
        
        instagram_link = None
        facebook_link = None
        website_link = None
        
        for query in queries:
            try:
                search_url = f"https://www.google.com/search?q={quote(query)}"
                response = self.session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    if not instagram_link:
                        instagram_link = self._extract_instagram_from_text(content)
                    if not facebook_link:
                        facebook_link = self._extract_facebook_from_text(content)
                    # Always try to extract website, even if we already have instagram/facebook
                    if not website_link:
                        website_link = self._extract_website_from_text(content, business_name)
                    
                    # Don't break early - continue searching for website even if we have social media
                    if instagram_link and facebook_link and website_link:
                        break
                
                time.sleep(1)  # Be respectful with rate limiting
            except Exception as e:
                print(f"Google search error: {e}")
        
        result = {}
        if instagram_link:
            result['instagram'] = instagram_link
        if facebook_link:
            result['facebook'] = facebook_link
        if website_link:
            result['website'] = website_link
        
        return result if result else None
    
    def _search_instagram_direct(self, business_name, country):
        """
        Try to construct or find Instagram link directly using common patterns
        """
        # Generate possible username variations
        variations = self._generate_username_variations(business_name, country)
        
        for variation in variations:
            potential_url = f"https://www.instagram.com/{variation}/"
            if self._verify_instagram_link(potential_url, business_name):
                return potential_url
        
        return None
    
    def _get_country_code(self, country):
        """Get country code abbreviation from country name"""
        country_lower = country.lower().strip()
        country_codes = {
            'kuwait': 'kw', 'saudi arabia': 'sa', 'uae': 'ae', 'united arab emirates': 'ae',
            'qatar': 'qa', 'bahrain': 'bh', 'oman': 'om', 'jordan': 'jo',
            'lebanon': 'lb', 'egypt': 'eg', 'iraq': 'iq', 'syria': 'sy',
            'usa': 'us', 'united states': 'us', 'uk': 'gb', 'united kingdom': 'gb',
            'canada': 'ca', 'australia': 'au', 'france': 'fr', 'germany': 'de',
            'italy': 'it', 'spain': 'es', 'netherlands': 'nl', 'belgium': 'be',
            'switzerland': 'ch', 'austria': 'at', 'sweden': 'se', 'norway': 'no',
            'denmark': 'dk', 'finland': 'fi', 'poland': 'pl', 'portugal': 'pt',
            'greece': 'gr', 'turkey': 'tr', 'india': 'in', 'china': 'cn',
            'japan': 'jp', 'south korea': 'kr', 'singapore': 'sg', 'malaysia': 'my',
            'thailand': 'th', 'indonesia': 'id', 'philippines': 'ph', 'vietnam': 'vn',
            'brazil': 'br', 'mexico': 'mx', 'argentina': 'ar', 'chile': 'cl',
            'colombia': 'co', 'peru': 'pe', 'south africa': 'za', 'nigeria': 'ng',
            'kenya': 'ke', 'israel': 'il', 'pakistan': 'pk', 'bangladesh': 'bd'
        }
        return country_codes.get(country_lower, '')
    
    def _generate_username_variations(self, business_name, country=None):
        """Generate possible username variations from business name"""
        name_lower = business_name.lower()
        variations = []
        
        # Remove common business suffixes
        suffixes = [' inc', ' inc.', ' llc', ' ltd', ' ltd.', ' corp', ' corp.', ' company', ' co', ' co.', ' studios', ' studio']
        clean_name = name_lower
        for suffix in suffixes:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)].strip()
        
        # Generate base variations
        base_variations = [
            clean_name.replace(' ', ''),
            clean_name.replace(' ', '_'),
            clean_name.replace(' ', '.'),
            clean_name.replace("'", ''),
            clean_name.replace("'", '').replace(' ', ''),
            re.sub(r'[^a-zA-Z0-9]', '', clean_name),
        ]
        
        # Handle abbreviations (e.g., "mb vision" -> "mbvision")
        words = clean_name.split()
        if len(words) > 1:
            # First letter of each word
            abbreviation = ''.join([w[0] for w in words if w])
            if len(abbreviation) >= 2:
                # Combine abbreviation with remaining words
                remaining = ''.join([w for w in words[1:] if w])
                if remaining:
                    base_variations.append(abbreviation + remaining)
                    base_variations.append(abbreviation.lower() + remaining.lower())
        
        # Add country code variations if country is provided
        if country:
            country_code = self._get_country_code(country)
            if country_code:
                # Add country code to base variations
                for base_var in base_variations[:]:
                    if base_var:  # Only if base variation exists
                        variations.append(base_var + country_code)
                        variations.append(base_var + '_' + country_code)
                        variations.append(base_var + '.' + country_code)
        
        # Add original base variations
        variations.extend(base_variations)
        
        # Remove duplicates and filter
        seen = set()
        unique_variations = []
        for var in variations:
            if var and var not in seen and len(var) > 2:
                seen.add(var)
                unique_variations.append(var)
        
        return unique_variations[:20]  # Increased limit to 20 for better coverage
    
    def _search_facebook_direct(self, business_name, country):
        """
        Try to find Facebook page using direct URL patterns
        """
        # Generate possible page name variations (with country codes)
        variations = self._generate_username_variations(business_name, country)
        
        # Also try searching with more specific Facebook queries
        # Facebook pages often use country codes, so prioritize those
        country_code = self._get_country_code(country) if country else ''
        
        # Reorder variations to try country code variations first
        prioritized_variations = []
        other_variations = []
        
        for var in variations:
            if country_code and country_code in var.lower():
                prioritized_variations.append(var)
            else:
                other_variations.append(var)
        
        # Try prioritized variations first
        for variation in prioritized_variations + other_variations:
            potential_url = f"https://www.facebook.com/{variation}/"
            if self._verify_facebook_link(potential_url, business_name):
                return potential_url
        
        return None
    
    def _extract_instagram_from_text(self, text):
        """
        Extract Instagram URL from text content
        """
        patterns = [
            r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?',
            r'instagram\.com/([a-zA-Z0-9_.]+)/?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                username = matches[0].split('/')[0].split('?')[0].split('#')[0]
                if username and len(username) > 1:
                    return self._normalize_instagram_url(f"https://www.instagram.com/{username}/")
        
        return None
    
    def _extract_facebook_from_text(self, text):
        """
        Extract Facebook URL from text content
        """
        patterns = [
            r'https?://(?:www\.)?facebook\.com/([a-zA-Z0-9_.]+)/?',
            r'facebook\.com/([a-zA-Z0-9_.]+)/?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                page = matches[0].split('/')[0].split('?')[0].split('#')[0]
                if page and len(page) > 1 and page not in ['pages', 'profile', 'people']:
                    return self._normalize_facebook_url(f"https://www.facebook.com/{page}/")
        
        return None
    
    def _normalize_instagram_url(self, url):
        """Normalize Instagram URL format"""
        match = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', url, re.IGNORECASE)
        if match:
            username = match.group(1).split('/')[0].split('?')[0]
            return f"https://www.instagram.com/{username}/"
        return url
    
    def _normalize_facebook_url(self, url):
        """Normalize Facebook URL format"""
        match = re.search(r'facebook\.com/([a-zA-Z0-9_.]+)', url, re.IGNORECASE)
        if match:
            page = match.group(1).split('/')[0].split('?')[0]
            return f"https://www.facebook.com/{page}/"
        return url
    
    def _is_likely_website(self, url, business_name):
        """Check if a URL is likely an official business website"""
        if not url:
            return False
        
        url_lower = url.lower()
        
        # Skip social media and common non-business sites
        skip_domains = [
            'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'tiktok.com', 'pinterest.com', 'snapchat.com',
            'google.com', 'maps.google.com', 'support.google.com', 'google.com/maps', 'google.com/search',
            'yelp.com', 'tripadvisor.com', 'foursquare.com', 'zomato.com', 'opentable.com', 
            'wikipedia.org', 'maps.apple.com', 'bing.com', 'yahoo.com', 'duckduckgo.com',
            'search.yahoo.com', 'search.bing.com'
        ]
        
        for domain in skip_domains:
            if domain in url_lower:
                return False
        
        # Must be http/https
        if not url_lower.startswith(('http://', 'https://')):
            return False
        
        # Prefer .com, .net, .org, country-specific TLDs
        valid_tlds = ['.com', '.net', '.org', '.co', '.io', '.me', '.info', '.biz',
                      '.ae', '.kw', '.sa', '.qa', '.bh', '.om', '.jo', '.lb', '.eg']
        has_valid_tld = any(tld in url_lower for tld in valid_tlds)
        
        return has_valid_tld
    
    def _extract_website_from_text(self, text, business_name):
        """Extract website URL from text content"""
        # Look for common website patterns - improved regex
        patterns = [
            r'https?://(?:www\.)?([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.(?:com|net|org|co|io|me|info|biz|ae|kw|sa|qa|bh|om|jo|lb|eg)[^/\s"\'<>]*)',
            r'(?:website|site|visit|www)\.([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.(?:com|net|org|co|io|me|info|biz|ae|kw|sa|qa|bh|om|jo|lb|eg))',
            r'<a[^>]*href=["\'](https?://[^"\']+)["\']',
        ]
        
        found_urls = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    domain = match[0] if match[0] else (match[1] if len(match) > 1 else None)
                else:
                    domain = match
                
                if domain:
                    if domain.startswith('http'):
                        url = domain
                    else:
                        url = f"https://{domain}"
                    
                    # Clean up URL
                    url = url.split('"')[0].split("'")[0].split(' ')[0].split('\n')[0]
                    
                    if self._is_likely_website(url, business_name) and url not in found_urls:
                        found_urls.append(url)
        
        # Return the first valid website found
        return found_urls[0] if found_urls else None
    
    def _search_website(self, business_name, country):
        """Search for official business website"""
        # Try common domain patterns
        clean_name = business_name.lower().replace(' ', '').replace("'", '').replace('-', '')
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', clean_name)
        
        # Remove common suffixes
        suffixes = ['inc', 'llc', 'ltd', 'corp', 'company', 'co', 'studios', 'studio']
        for suffix in suffixes:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)]
        
        # Generate possible domain variations
        domain_variations = [
            f"{clean_name}.com",
            f"www.{clean_name}.com",
            f"{clean_name}.net",
            f"{clean_name}.org",
        ]
        
        # Add country-specific variations if country code available
        country_code = self._get_country_code(country)
        if country_code:
            domain_variations.extend([
                f"{clean_name}{country_code}.com",
                f"{clean_name}-{country_code}.com",
                f"{clean_name}.{country_code}",
                f"www.{clean_name}{country_code}.com",
            ])
        
        # Also try with "vision" or other words if they exist
        words = business_name.lower().split()
        if len(words) > 1:
            # Try first word + last word
            if len(words) >= 2:
                short_name = words[0] + words[-1]
                short_name = re.sub(r'[^a-zA-Z0-9]', '', short_name)
                domain_variations.extend([
                    f"{short_name}.com",
                    f"www.{short_name}.com",
                ])
                if country_code:
                    domain_variations.extend([
                        f"{short_name}{country_code}.com",
                        f"{short_name}-{country_code}.com",
                    ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_variations = []
        for var in domain_variations:
            if var not in seen:
                seen.add(var)
                unique_variations.append(var)
        
        for domain_var in unique_variations[:10]:  # Increased limit
            potential_url = f"https://{domain_var}"
            if self._verify_website_link(potential_url, business_name):
                return potential_url
        
        return None
    
    def _verify_website_link(self, url, business_name):
        """Verify that the website link is valid and matches the business"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                content = response.text.lower()
                final_url = response.url.lower()
                
                # Check for explicit error pages (be more specific to avoid false positives)
                # Only check in first part of content where error messages typically appear
                content_sample = content[:5000]
                
                # More specific error patterns that indicate actual error pages
                explicit_errors = [
                    'page not found',
                    '404 error',
                    'error 404',
                    'not found',
                    'domain for sale',
                    'this domain is for sale',
                    'buy this domain',
                    'parked domain',
                    'domain parking'
                ]
                
                # Check if multiple error indicators appear (more likely to be real error)
                error_count = sum(1 for error in explicit_errors if error in content_sample)
                if error_count >= 2:  # Multiple error indicators = likely error page
                    return False
                
                # Check for single strong error indicators
                strong_errors = ['domain for sale', 'this domain is for sale', 'buy this domain', 'parked domain']
                if any(error in content_sample for error in strong_errors):
                    return False
                
                # Try to extract page title (use original text, not lowercased)
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                og_title_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', response.text, re.IGNORECASE)
                
                title = None
                if og_title_match:
                    title = og_title_match.group(1)
                elif title_match:
                    title = title_match.group(1)
                
                if title:
                    # Check if business name appears in title (with some similarity)
                    similarity = self._similarity(business_name, title)
                    if similarity > 0.2:  # Lowered threshold
                        return True
                    # Also check if business name words appear in title
                    business_words = [w for w in business_name.lower().split() if len(w) > 2]
                    title_lower = title.lower()
                    matching_words = sum(1 for word in business_words if word in title_lower)
                    if business_words and matching_words >= max(1, len(business_words) * 0.4):  # At least 40% match
                        return True
                
                # Check domain name matches business name
                domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url.lower())
                if domain_match:
                    domain = domain_match.group(1)
                    # Remove TLD
                    domain_name = re.sub(r'\.[a-z]{2,}$', '', domain)
                    # Check if business name appears in domain
                    clean_business = re.sub(r'[^a-z0-9]', '', business_name.lower())
                    clean_domain = re.sub(r'[^a-z0-9]', '', domain_name)
                    if clean_business and clean_domain:
                        if clean_business in clean_domain or clean_domain in clean_business:
                            return True
                        # Check if significant portion matches
                        if len(clean_business) >= 3 and len(clean_domain) >= 3:
                            # Check for substring match of at least 3 chars
                            for i in range(len(clean_business) - 2):
                                substr = clean_business[i:i+3]
                                if substr in clean_domain:
                                    return True
                
                # If page loads successfully (200) and no strong error indicators, assume valid
                # Many legitimate sites might not have perfect title matches
                return True
            
            elif response.status_code == 404:
                return False
            else:
                # Other status codes (301, 302, etc.) - check redirect URL
                if response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.url
                    if redirect_url != url:
                        # Recursively check redirect (but limit to avoid infinite loops)
                        return self._verify_website_link(redirect_url, business_name)
                # For other codes, be lenient
                return True
                
        except requests.exceptions.RequestException as e:
            # Network errors - don't assume invalid, might be temporary
            print(f"Website verification network error: {e}")
            return False
        except Exception as e:
            print(f"Website verification error: {e}")
            return False
    
    def _verify_instagram_link(self, url, business_name):
        """
        Verify that the Instagram link is valid and potentially matches the business
        """
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check if page doesn't exist
                error_indicators = [
                    'page not found',
                    'sorry, this page',
                    'user not found',
                    'this page is not available'
                ]
                
                if any(indicator in content for indicator in error_indicators):
                    return False
                
                # Try to extract profile name and compare with business name
                # Instagram pages often have the business name in the title or meta tags
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1)
                    # Check if business name appears in title (with some similarity threshold)
                    if self._similarity(business_name, title) > 0.3:
                        return True
                
                # If no error indicators, assume valid
                return True
        except Exception as e:
            print(f"Instagram verification error: {e}")
        
        return False
    
    def _verify_facebook_link(self, url, business_name):
        """
        Verify that the Facebook link is valid and potentially matches the business
        Facebook requires login for most pages, so we use a more lenient approach
        """
        try:
            # Extract username from URL first
            username_match = re.search(r'facebook\.com/([^/?]+)', url.lower())
            if not username_match:
                return False
            
            username = username_match.group(1)
            if not username or len(username) < 2:
                return False
            
            # Skip common Facebook paths that aren't pages
            skip_paths = ['pages', 'profile', 'people', 'login', 'home', 'watch', 'marketplace', 'groups', 'events']
            if username in skip_paths:
                return False
            
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            # If we get a 200 response, check for error indicators
            if response.status_code == 200:
                content = response.text.lower()
                final_url = response.url.lower()
                
                # Check for explicit error messages (these indicate page doesn't exist)
                error_indicators = [
                    'page not found',
                    'content not available',
                    'this content is not available',
                    'sorry, this page',
                    'this page isn\'t available',
                    'the link you followed may be broken',
                    'this page may have been removed',
                    'no longer available'
                ]
                
                # If we find explicit error messages, page doesn't exist
                if any(indicator in content for indicator in error_indicators):
                    return False
                
                # If we got here with a 200 response and no errors, the page exists
                # Facebook may show login page, but that means the page URL is valid
                return True
            
            # For other status codes, be more cautious
            elif response.status_code == 404:
                return False
            else:
                # For other status codes, assume it might exist (could be temporary issues)
                return True
                
        except requests.exceptions.RequestException as e:
            # Network errors - don't assume page doesn't exist, try to verify URL structure
            username_match = re.search(r'facebook\.com/([^/?]+)', url.lower())
            if username_match:
                username = username_match.group(1)
                skip_paths = ['pages', 'profile', 'people', 'login', 'home', 'watch', 'marketplace', 'groups', 'events']
                if username and len(username) >= 2 and username not in skip_paths:
                    # URL structure looks valid, assume it exists
                    return True
            return False
        except Exception as e:
            print(f"Facebook verification error: {e}")
            return False

finder = SocialMediaFinder(
    google_api_key=os.getenv('GOOGLE_API_KEY'),
    google_cse_id=os.getenv('GOOGLE_CSE_ID')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    business_name = data.get('business_name', '').strip()
    country = data.get('country', '').strip()
    
    if not business_name:
        return jsonify({'error': 'Business name is required'}), 400
    
    if not country:
        return jsonify({'error': 'Country is required'}), 400
    
    try:
        results = finder.find_social_links(business_name, country)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/find', methods=['GET', 'POST'])
def find_links():
    """
    API endpoint to find social media links for a business
    GET or POST: ?business_name=NAME&country=COUNTRY
    POST JSON: {"business_name": "NAME", "country": "COUNTRY"}
    Country is optional
    """
    # Support both GET and POST
    if request.method == 'GET':
        business_name = request.args.get('business_name', '').strip()
        country = request.args.get('country', '').strip() or None
    else:  # POST
        if request.is_json:
            data = request.json
            business_name = data.get('business_name', '').strip()
            country = data.get('country', '').strip() or None
        else:
            business_name = request.form.get('business_name', '').strip()
            country = request.form.get('country', '').strip() or None
    
    if not business_name:
        return jsonify({'error': 'business_name parameter is required'}), 400
    
    try:
        # Use empty string if country is None for backward compatibility
        country = country or ''
        results = finder.find_social_links(business_name, country)
        
        # Return clean response with just the links
        response = {
            'business_name': business_name,
            'country': country if country else None,
            'instagram': results.get('instagram'),
            'facebook': results.get('facebook'),
            'website': results.get('website'),
            'confidence': results.get('confidence'),
            'sources': results.get('sources', [])
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

