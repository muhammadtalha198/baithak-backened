# app/models/__init__.py
from app.models.user import User
from app.models.app_config import AppConfig

__all__ = ["User", "AppConfig"]