from functools import wraps
from flask import g
from ..exceptions import AuthenticationError, AuthorizationError

def login_required(f):
    """
    Decorator to require that a user is logged in.
    The application must set `g.user` (or similar, depending on how you implement auth).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We check if g has a user object and it is not None.
        if getattr(g, "user", None) is None:
            raise AuthenticationError("You must be logged in to access this resource.")
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """
    Decorator to require that a user has at least one of the specified roles.
    Requires `login_required` to be implicitly satisfied.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(g, "user", None)
            if user is None:
                raise AuthenticationError("You must be logged in to access this resource.")
            
            user_roles = getattr(user, "roles", [])
            if not any(role in user_roles for role in roles):
                raise AuthorizationError(f"You do not have permission to access this resource. Required roles: {', '.join(roles)}.")
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
