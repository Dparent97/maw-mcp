# Import-Time Initialization Errors

Services that connect to external APIs at import time break when credentials are missing or in mock mode.

---

## The Problem

```python
# BAD: connects to GCP at import
from gemini_service import gemini_service  # Crashes if no credentials

class GeminiVisionService:
    def __init__(self):
        self.client = genai.Client()  # Runs immediately on import
```

When this module is imported anywhere, it tries to connect - even in tests, mock mode, or when credentials aren't configured yet.

---

## The Solution: Lazy Initialization

```python
# GOOD: lazy init, only connects when used
class LazyGeminiService:
    _instance = None
    
    def __getattr__(self, name):
        if self._instance is None:
            self._instance = GeminiVisionService()
        return getattr(self._instance, name)

gemini_service = LazyGeminiService()
```

Or use a factory function:

```python
_service = None

def get_gemini_service():
    global _service
    if _service is None:
        _service = GeminiVisionService()
    return _service
```

---

## When You'll Hit This

- External API clients (Gemini, OpenAI, AWS, etc.)
- Database connections
- Any service requiring environment variables
- Services requiring network access

---

## Signs of This Problem

- "Connection refused" on import
- Tests failing before any test runs
- Mock mode not working
- "Missing credentials" during import, not during use

---

## Projects Where This Occurred

| Project | Date | Service | Resolution |
|---------|------|---------|------------|
| Reality-layer | 2025-12-11 | Gemini Vision | Added lazy wrapper class |

---

*Last updated: 2025-12-11*
