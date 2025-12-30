# Python Learnings

Patterns and gotchas from Python projects.

---

## FastAPI Patterns

### Dependency Injection for Services
```python
# Good: inject service as dependency
def get_gemini_service():
    return GeminiVisionService()

@app.post("/analyze")
async def analyze(
    file: UploadFile,
    service: GeminiVisionService = Depends(get_gemini_service)
):
    return await service.analyze(file)
```

### Query Parameters with Defaults
```python
@app.post("/analyze")
async def analyze(
    file: UploadFile,
    mock: bool = Query(default=None),  # Optional, None if not provided
    scenario: str = Query(default="default")  # Optional with default
):
    use_mock = mock if mock is not None else settings.MOCK_MODE
```

---

## Common Gotchas

### Mutable Default Arguments
```python
# BAD: shared list across calls
def add_item(item, items=[]):
    items.append(item)
    return items

# GOOD: None sentinel
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Import-Time Side Effects
See: [BY_ERROR/import-time-init.md](../BY_ERROR/import-time-init.md)

```python
# BAD: runs at import
client = SomeAPIClient()  # Network call at import time

# GOOD: lazy init
_client = None
def get_client():
    global _client
    if _client is None:
        _client = SomeAPIClient()
    return _client
```

### Async/Await in FastAPI
```python
# If function does I/O, make it async
async def fetch_data():
    async with httpx.AsyncClient() as client:
        return await client.get(url)

# If function is CPU-bound, don't use async
def compute_hash(data):
    return hashlib.sha256(data).hexdigest()
```

---

## Testing Patterns

### Pytest Fixtures for FastAPI
```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
```

### Mock External Services
```python
@pytest.fixture
def mock_gemini(monkeypatch):
    def mock_analyze(*args, **kwargs):
        return {"objects": [], "context": "mock"}
    monkeypatch.setattr("gemini_service.analyze", mock_analyze)
```

---

## Environment & Config

### Pydantic Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mock_mode: bool = False
    gcp_project_id: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### .env.example Pattern
Always create `.env.example` documenting all variables:
```bash
# .env.example
MOCK_MODE=true
GCP_PROJECT_ID=your-project-id
LOG_LEVEL=INFO
```

---

## Project Structure

```
backend/
├── main.py           # FastAPI app, routes
├── config.py         # Settings, env vars
├── exceptions.py     # Custom exceptions
├── logging_config.py # Logging setup
├── requirements.txt  # Dependencies
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py   # Shared fixtures
└── .env.example
```

---

*Last updated: 2025-12-11*
