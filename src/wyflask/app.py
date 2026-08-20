import os
from flask import Flask
from .config import get_config
from .routing import registry

def create_app(config: str | type | None = None) -> Flask:
    """
    Application factory for WyFlask.
    
    Creates a Flask instance, loads configuration, initializes framework extensions,
    registers middleware, and discovers/registers application modules.
    """
    # Use the caller's project root (cwd) so Flask finds
    # app/templates/ and app/static/ in the user's project.
    project_root = os.getcwd()
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "app", "templates"),
        static_folder=os.path.join(project_root, "app", "static"),
    )
    
    # Load configuration
    cfg = get_config(config)
    app.config.from_object(cfg)

    # Register framework error handlers
    from .responses import register_error_handlers
    register_error_handlers(app)

    # Register middleware
    from .middleware import register_middleware
    register_middleware(app)

    # Register all application modules
    registry.register_all(app)

    return app
