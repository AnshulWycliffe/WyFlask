"""
Core framework exceptions.
"""

class WyFlaskError(Exception):
    """Base exception for all WyFlask errors."""
    pass

class ConfigurationError(WyFlaskError):
    """Raised when there is a configuration issue."""
    pass

class ModuleError(WyFlaskError):
    """Raised when a module is misconfigured or cannot be registered."""
    pass

class ValidationError(WyFlaskError):
    """Raised when data validation fails."""
    pass

class AuthenticationError(WyFlaskError):
    """Raised when authentication fails or is missing."""
    pass

class AuthorizationError(WyFlaskError):
    """Raised when a user lacks required permissions."""
    pass

class NotFoundError(WyFlaskError):
    """Raised when a requested resource is not found."""
    pass
