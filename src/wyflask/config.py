import os
from typing import Any

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SECRET_KEY = "test-secret"

class ProductionConfig(Config):
    """Production configuration."""
    # In production, SECRET_KEY must be provided via environment
    pass

def get_config(config_name: str | type | None = None) -> Any:
    """Retrieve the configuration object based on string name or type."""
    if isinstance(config_name, type):
        return config_name()

    if config_name is None:
        env = os.environ.get("WYFLASK_ENV", "development").lower()
        if env == "testing":
            return TestingConfig()
        elif env == "production":
            return ProductionConfig()
        return DevelopmentConfig()
    
    if isinstance(config_name, str):
        # We can try to load by string path, e.g. "config.DevelopmentConfig"
        # For simple cases, we map the built-ins:
        mapping = {
            "development": DevelopmentConfig(),
            "testing": TestingConfig(),
            "production": ProductionConfig()
        }
        if config_name.lower() in mapping:
            return mapping[config_name.lower()]
        
        # In a real app, this might dynamically import from the app's config.py
        # We will handle string-based object import here.
        import importlib
        try:
            module_name, class_name = config_name.rsplit(".", 1)
            module = importlib.import_module(module_name)
            config_class = getattr(module, class_name)
            return config_class()
        except (ValueError, ImportError, AttributeError):
            pass

    return config_name
