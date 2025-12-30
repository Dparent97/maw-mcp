# Gemini Vision API

Patterns for integrating Google's Gemini Vision API via Vertex AI.

---

## Setup

### Prerequisites
1. GCP project with billing enabled
2. Vertex AI API enabled
3. Service account with "Vertex AI User" role
4. JSON key file downloaded

### Environment Variables
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
export GCP_PROJECT_ID=your-project-id
export GCP_LOCATION=us-central1  # or your preferred region
```

---

## Mock Mode Pattern

Always implement mock mode for development:

```python
# config.py
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# main.py
@app.post("/analyze")
async def analyze(file: UploadFile, mock: bool = Query(default=None)):
    use_mock = mock if mock is not None else settings.MOCK_MODE
    
    if use_mock:
        return get_mock_response(scenario="breaker_panel")
    else:
        return await gemini_service.analyze(file)
```

### Mock Response Library
Create `mock_responses.py` with realistic scenarios:
- breaker_panel
- hvac_system
- machinery
- water_heater
- electrical_outlet
- valve_assembly

Each should return varied positions, confidence scores, and appropriate warnings.

---

## Lazy Initialization

Don't initialize Gemini client at import time. See: [BY_ERROR/import-time-init.md](../BY_ERROR/import-time-init.md)

```python
# BAD
gemini_service = GeminiVisionService()  # Crashes without credentials

# GOOD
class LazyGeminiService:
    _instance = None
    def __getattr__(self, name):
        if self._instance is None:
            self._instance = GeminiVisionService()
        return getattr(self._instance, name)
```

---

## Prompt Engineering

Store prompts in YAML files, not hardcoded:

```yaml
# prompts/home_maintenance_v1.yaml
system_instruction: |
  Analyze this image of equipment/infrastructure.
  Identify components, safety warnings, and maintenance needs.
  
output_format:
  - detected_objects (array)
  - system_context (string)
  - confidence (float)
```

Load dynamically for easy iteration without code changes.

---

## Common Issues

### "Permission denied" on API call
- Check service account has Vertex AI User role
- Verify GOOGLE_APPLICATION_CREDENTIALS path is correct
- Confirm project has billing enabled

### Slow response times
- Gemini Vision takes 2-5 seconds typically
- Show loading state in UI
- Consider image compression before upload

### Rate limiting
- Default: 60 requests/minute
- Implement client-side throttling
- Queue requests if needed

---

## Projects Using This

| Project | Use Case |
|---------|----------|
| Reality-layer | AR equipment identification |

---

*Last updated: 2025-12-11*
