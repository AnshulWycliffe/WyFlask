import pytest
from flask import Flask
from wyflask.routing import Module, Registry
from wyflask.exceptions import ModuleError

def test_module_creation():
    mod = Module("test_mod")
    assert mod.name == "test_mod"
    
    @mod.route("/hello")
    def hello():
        return "world"

def test_registry_registration():
    registry = Registry()
    mod = Module("test_mod")
    registry.register(mod)
    
    with pytest.raises(ModuleError):
        registry.register(mod)

def test_registry_register_all():
    app = Flask(__name__)
    registry = Registry()
    
    mod = Module("api")
    @mod.route("/status")
    def status():
        return "ok"
    
    registry.register(mod)
    registry.register_all(app)
    
    client = app.test_client()
    response = client.get("/status")
    assert response.status_code == 200
    assert response.data == b"ok"
