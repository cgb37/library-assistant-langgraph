# Shared configuration and service logic for the Quart app

# This module will provide configuration loading and shared database service setup.

# config_service.py

import os
from typing import Any

class ConfigService:
    def __init__(self):
        # MongoDB configuration
        mongo_username = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'admin')
        mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'password')
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        mongo_port = os.getenv('MONGO_PORT', '27017')
        mongo_database = os.getenv('MONGO_INITDB_DATABASE', 'library_assistant')
        
        self.config = {
            'MONGO_URL': f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin',
            'MONGO_DATABASE': mongo_database
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

config_service = ConfigService()
