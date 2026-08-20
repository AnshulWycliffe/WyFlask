import pytest
from wyflask import create_app

def test_create_app():
    """Test that the application factory returns a valid Flask app."""
    app = create_app("testing")
    assert app is not None
    assert app.config["TESTING"] is True
