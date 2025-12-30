# BeautifulSoup / Web Scraping

Patterns for extracting data from web pages.

---

## Common Patterns

### Open Graph Meta Tag Extraction
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Context:** Paste-a-link feature to create products from URLs.

**Pattern:** Extract product info using OG tags (standard across most e-commerce sites):
```python
from bs4 import BeautifulSoup
import requests

def extract_product_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Try Open Graph first (most reliable)
    og_title = soup.find("meta", property="og:title")
    og_image = soup.find("meta", property="og:image")
    
    # Fallback to Twitter cards
    if not og_title:
        og_title = soup.find("meta", attrs={"name": "twitter:title"})
    if not og_image:
        og_image = soup.find("meta", attrs={"name": "twitter:image"})
    
    # Fallback to regular title
    if not og_title:
        title_tag = soup.find("title")
        name = title_tag.text.strip() if title_tag else None
    else:
        name = og_title.get("content", "").strip()
    
    image_url = og_image.get("content", "").strip() if og_image else None
    
    return {"name": name, "image_url": image_url}
```

**Why OG tags:**
- Standardized across platforms (Facebook, LinkedIn, etc.)
- Sites maintain them for social sharing
- More stable than scraping page-specific HTML
- Work on Costco, Walmart, Amazon, Target, etc.

---

### Cleaning Product Names
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Pattern:** Remove site suffixes from extracted titles:
```python
import re

def clean_product_name(name):
    # Remove " | Costco", " - Walmart.com", etc.
    name = re.split(
        r'\s*[\|\-–—]\s*(?:Costco|Walmart|Amazon|Target|Sam\'s Club)',
        name,
        flags=re.IGNORECASE
    )[0].strip()
    return name

# "Kirkland Trail Mix | Costco" → "Kirkland Trail Mix"
```

---

### URL Path Fallback
**Date:** 2025-12-21
**Project:** crew-shopping-list

**Pattern:** Extract product name from URL when scraping fails:
```python
from urllib.parse import urlparse, unquote

def name_from_url(url):
    path = urlparse(url).path
    segments = [s for s in path.split('/') if s]
    if segments:
        name = segments[-1]
        # Clean up common URL patterns
        name = re.sub(r'\.product\.\d+\.html$', '', name)  # Costco
        name = re.sub(r'\.html$', '', name)
        name = re.sub(r'/\d+$', '', name)  # Walmart numeric IDs
        name = name.replace('-', ' ')
        name = unquote(name)  # URL decode
        return ' '.join(word.capitalize() for word in name.split())
    return None

# "kirkland-trail-mix.product.100334841.html" → "Kirkland Trail Mix"
```

---

## Anti-Scraping Workarounds

### Browser-like Headers
**Problem:** Many sites block requests without proper headers.

**Solution:**
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
```

### Graceful Fallback
**Pattern:** Always return partial data rather than failing completely:
```python
try:
    # Try full scrape
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract OG tags...
except requests.exceptions.Timeout:
    # Fallback to URL parsing
    name = name_from_url(url)
    return {"name": name, "image_url": None, "partial": True}
```
