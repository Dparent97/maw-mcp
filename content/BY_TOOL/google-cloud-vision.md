# Google Cloud Vision API

OCR and image analysis using Google's Cloud Vision API.

---

## Common Issues

### Claude.ai Sandbox Blocks External API Calls
**Date:** 2025-12-19
**Project:** oil_record_book_tool
**Context:** Testing OCR service that calls Google Cloud Vision API

**Problem:**
When running code in Claude.ai's sandbox (web interface), HTTP requests to external APIs like `vision.googleapis.com` get blocked by the egress proxy with a 403 error.

**Solution:**
Test OCR functionality locally on your machine, not in Claude.ai sandbox. The code itself is fine - it's an environment restriction.

```python
# This works locally, not in Claude.ai sandbox
from google.cloud import vision

client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
```

**Prevention:**
Remember: Claude.ai sandbox has network restrictions. Use it for code review and generation, but test API integrations locally.

---

### Credentials Setup
**Date:** 2025-12-19
**Project:** oil_record_book_tool
**Context:** Setting up Google Cloud Vision for OCR

**Setup:**
```bash
# Store credentials securely
cp ~/Downloads/your-service-account.json ~/.config/gcloud/project-credentials.json

# Add to shell profile (~/.zshrc)
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/project-credentials.json"

# Or add to project .env file
echo 'GOOGLE_APPLICATION_CREDENTIALS=/Users/dp/.config/gcloud/project-credentials.json' >> .env
```

**In Flask app.py:**
```python
from dotenv import load_dotenv
load_dotenv()  # Must be called before importing google.cloud
```

---

### Table/Form OCR Parsing
**Date:** 2025-12-19
**Project:** oil_record_book_tool
**Context:** Parsing structured forms (End of Hitch Sounding Form)

**Problem:**
OCR returns raw text - table structure is lost. Regex patterns may not match Vision API's actual output format.

**Solution:**
1. Use `document_text_detection()` not `text_detection()` - better for forms
2. Build regex patterns conservatively, test with actual output
3. Make the parser tolerant of variations

```python
# Use document detection for forms
response = client.document_text_detection(image=image)
full_text = response.full_text_annotation.text

# Flexible pattern matching
tank_pattern = re.compile(
    r'#(\d+)\s+(Port|Stbd).*?(\d+)\s+(\d+).*?([\d,]+)',
    re.IGNORECASE | re.DOTALL
)
```

**Prevention:**
Test with actual photos before assuming regex works. Print raw OCR output first, then build patterns.

---

*Last updated: 2025-12-19*
