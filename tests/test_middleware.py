import pytest
from wyflask import create_app

def test_request_middleware():
    app = create_app("testing")
    
    @app.route("/ping")
    def ping():
        return "pong"
        
    client = app.test_client()
    response = client.get("/ping", headers={"X-Request-ID": "test-id-123"})
    
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == "test-id-123"
    assert "X-Process-Time" in response.headers
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
