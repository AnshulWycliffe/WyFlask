import pytest
from flask import Flask, g
from wyflask.security import login_required, role_required, hash_password, verify_password
from wyflask.exceptions import AuthenticationError, AuthorizationError

class MockUser:
    def __init__(self, roles=None):
        self.roles = roles or []

def test_password_hashing():
    password = "supersecretpassword"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(hashed, password) is True
    assert verify_password(hashed, "wrongpassword") is False

def test_login_required():
    app = Flask(__name__)
    
    @app.route("/protected")
    @login_required
    def protected():
        return "ok"
        
    with app.app_context():
        # Without user
        with pytest.raises(AuthenticationError):
            protected()
            
        # With user
        g.user = MockUser()
        assert protected() == "ok"

def test_role_required():
    app = Flask(__name__)
    
    @app.route("/admin")
    @role_required("admin")
    def admin_panel():
        return "admin data"
        
    with app.app_context():
        # Without user
        with pytest.raises(AuthenticationError):
            admin_panel()
            
        # With user, no roles
        g.user = MockUser()
        with pytest.raises(AuthorizationError):
            admin_panel()
            
        # With wrong role
        g.user = MockUser(["manager"])
        with pytest.raises(AuthorizationError):
            admin_panel()
            
        # With correct role
        g.user = MockUser(["admin"])
        assert admin_panel() == "admin data"
        
        # With multiple roles where one is correct
        g.user = MockUser(["manager", "admin"])
        assert admin_panel() == "admin data"
