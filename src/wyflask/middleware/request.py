import time
import uuid
from flask import Flask, request, g, current_app

def register_middleware(app: Flask):
    """
    Registers standard WyFlask middleware.
    """
    
    @app.before_request
    def before_request():
        # Set a unique request ID
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # Start timing
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        # Calculate timing
        if hasattr(g, "start_time"):
            elapsed = time.time() - g.start_time
            response.headers["X-Process-Time"] = str(elapsed)
            
        # Add Request ID
        if hasattr(g, "request_id"):
            response.headers["X-Request-ID"] = g.request_id
            
        # Security headers
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        
        return response
