import pytest
from wyflask.config import get_config, DevelopmentConfig, TestingConfig, ProductionConfig

def test_get_config_default():
    config = get_config()
    assert isinstance(config, DevelopmentConfig)
    assert config.DEBUG is True

def test_get_config_testing():
    config = get_config("testing")
    assert isinstance(config, TestingConfig)
    assert config.TESTING is True

def test_get_config_production():
    config = get_config("production")
    assert isinstance(config, ProductionConfig)
    assert config.DEBUG is False
    assert config.TESTING is False
