from flask import Flask
from .module import Module
from ..exceptions import ModuleError

class Registry:
    """Manages application modules."""
    def __init__(self):
        self._modules: dict[str, Module] = {}

    def register(self, module: Module):
        """Add a module to the registry."""
        if not isinstance(module, Module):
            raise ModuleError(f"Expected a Module instance, got {type(module)}")
        if module.name in self._modules:
            raise ModuleError(f"Module '{module.name}' is already registered.")
        self._modules[module.name] = module

    def register_all(self, app: Flask):
        """Register all added modules to the Flask application."""
        for module in self._modules.values():
            app.register_blueprint(module.blueprint)

registry = Registry()
