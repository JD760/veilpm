from fastapi import Request
from src.core.config import Settings, settings


def get_settings(request: Request) -> Settings:
    return settings
