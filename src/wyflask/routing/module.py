from flask import Blueprint

class Module:
    """
    A higher-level abstraction over Flask Blueprints.
    """
    def __init__(self, name: str, import_name: str | None = None, **kwargs):
        self.name = name
        self.import_name = import_name or name
        self.blueprint = Blueprint(name, self.import_name, **kwargs)

    def route(self, rule: str, **options):
        """Decorator for registering routes."""
        def decorator(f):
            self.blueprint.route(rule, **options)(f)
            return f
        return decorator
