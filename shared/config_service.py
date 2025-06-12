# Shared configuration and service logic for the Quart app

# This module will provide configuration loading and shared database service setup.

# config_service.py

import os
from typing import Any

class ConfigService:
    def __init__(self):
        self.config = {
            'DATABASE_URL': os.getenv('DATABASE_URL', 'sqlite:///library_assistant.db')
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

config_service = ConfigService()
