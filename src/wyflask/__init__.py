"""
WyFlask: A production-grade Python web framework built on top of Flask.
"""

from .app import create_app
from .config import Config

__version__ = "0.1.3"
__all__ = ["create_app", "Config"]
