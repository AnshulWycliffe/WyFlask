# Testing Guide

Testing in WyFlask is streamlined using `pytest` and Flask's built-in test client.

---

## 1. Setup Pytest

Install `pytest`:
```bash
pip install pytest
```

---

## 2. Test Configuration & Fixtures

Create `tests/conftest.py` to define test fixtures:

```python
import pytest
from wyflask import create_app
from wyflask.routing import registry
from app.modules.main import main_module
from app.modules.users import users_module

@pytest.fixture(scope="session")
def app():
    """Create test application instance with TestingConfig."""
    # Ensure modules are registered
    try:
        registry.register(main_module)
        registry.register(users_module)
    except Exception:
        pass  # Already registered

    test_app = create_app("testing")
    return test_app

@pytest.fixture
def client(app):
    """Test client fixture for making requests."""
    return app.test_client()
```

---

## 3. Writing Unit & Integration Tests

In `tests/test_users.py`:

```python
def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data["success"] is True
    assert "data" in json_data

def test_not_found_error(client):
    response = client.get("/users/99999")
    assert response.status_code == 404
    
    json_data = response.get_json()
    assert json_data["success"] is False
    assert json_data["error"]["code"] == "NOT_FOUND_ERROR"

def test_middleware_headers(client):
    response = client.get("/")
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
```

---

## 4. Running the Tests

Execute pytest in your terminal:

```bash
pytest -v
```
