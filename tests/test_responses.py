import pytest
from flask import Flask
from wyflask import create_app
from wyflask.responses import success, error
from wyflask.exceptions import NotFoundError

def test_success_response():
    app = Flask(__name__)
    with app.app_context():
        response, status = success(message="Created", data={"id": 1}, status_code=201)
        assert status == 201
        assert response.json["success"] is True
        assert response.json["message"] == "Created"
        assert response.json["data"] == {"id": 1}

def test_error_response():
    app = Flask(__name__)
    with app.app_context():
        response, status = error(message="Invalid", status_code=422, errors={"field": "bad"})
        assert status == 422
        assert response.json["success"] is False
        assert response.json["message"] == "Invalid"
        assert response.json["errors"] == {"field": "bad"}

def test_error_handlers():
    app = create_app("testing")
    
    @app.route("/trigger-error")
    def trigger_error():
        raise NotFoundError("Resource not found")
        
    client = app.test_client()
    response = client.get("/trigger-error")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert response.json["error"]["code"] == "NOTFOUND_ERROR"
    assert response.json["error"]["message"] == "Resource not found"
