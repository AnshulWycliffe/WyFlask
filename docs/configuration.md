# Configuration Management

WyFlask uses object-oriented, environment-driven configuration for clean separation between development, testing, and production environments.

---

## Built-In Configuration Classes

WyFlask provides base configuration classes in `wyflask.config`:

```python
from wyflask.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
```

- **`Config`**: Base class. Reads `SECRET_KEY` from environment or defaults to `"dev-secret-key"`. `DEBUG = False`, `TESTING = False`.
- **`DevelopmentConfig`**: Inherits `Config` and sets `DEBUG = True`.
- **`TestingConfig`**: Sets `TESTING = True` and uses `SECRET_KEY = "test-secret"`.
- **`ProductionConfig`**: `DEBUG = False`, requiring explicit `SECRET_KEY` from environment variables.

---

## Defining Application Configuration

In your project's `app/config.py`:

```python
import os
from wyflask.config import Config

class AppConfig(Config):
    """Base application settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-dev-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(AppConfig):
    """Local development settings."""
    DEBUG = True

class TestingConfig(AppConfig):
    """Unit and integration test settings."""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"

class ProductionConfig(AppConfig):
    """Production deployment settings."""
    DEBUG = False
    # In production, ensure SECRET_KEY and DATABASE_URL are set via environment
```

---

## Loading Configuration in `create_app`

You can supply configuration to `create_app()` in several flexible ways:

### 1. By String Dotted Path (Recommended)
```python
from wyflask import create_app

app = create_app("app.config.DevelopmentConfig")
```

### 2. By Direct Class or Instance
```python
from wyflask import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)
```

### 3. Environment-Based Selection via `WYFLASK_ENV`
If no parameter is passed, WyFlask reads the `WYFLASK_ENV` environment variable:

```bash
# In shell or .env
export WYFLASK_ENV=production
```

```python
from wyflask import create_app

# Automatically selects ProductionConfig if WYFLASK_ENV=production
app = create_app()
```
