from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from ..exceptions import WyFlaskError

def register_error_handlers(app: Flask):
    """Register global error handlers for the application."""
    
    @app.errorhandler(WyFlaskError)
    def handle_wyflask_error(e):
        # We can inspect the class name to generate an error code
        code = e.__class__.__name__.upper().replace("ERROR", "_ERROR").strip("_")
        response = {
            "success": False,
            "error": {
                "code": code,
                "message": str(e)
            }
        }
        
        # Determine status code based on exception type, default to 400
        status_code = 400
        if "NOTFOUND" in code:
            status_code = 404
        elif "AUTHENTICATION" in code:
            status_code = 401
        elif "AUTHORIZATION" in code:
            status_code = 403
            
        return jsonify(response), status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        # For HTTP exceptions, check if request wants JSON
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = {
                "success": False,
                "error": {
                    "code": "HTTP_ERROR",
                    "message": e.description
                }
            }
            return jsonify(response), e.code
        # Otherwise let Flask handle HTML response
        return e

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # Never expose internal stack traces in production responses
        response = {
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred."
            }
        }
        if app.debug:
            response["error"]["details"] = str(e)
            
        return jsonify(response), 500
