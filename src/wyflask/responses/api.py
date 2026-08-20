from typing import Any
from flask import jsonify

def success(message: str = "Success", data: Any = None, status_code: int = 200, **kwargs):
    """
    Returns a consistent JSON success response.
    """
    response_data = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response_data["data"] = data
    
    response_data.update(kwargs)
    
    return jsonify(response_data), status_code

def error(message: str = "Error", status_code: int = 400, errors: Any = None, **kwargs):
    """
    Returns a consistent JSON error response.
    """
    response_data = {
        "success": False,
        "message": message,
    }
    if errors is not None:
        response_data["errors"] = errors
        
    response_data.update(kwargs)
    
    return jsonify(response_data), status_code
