import os
import json
import logging
from box import Box

logger = logging.getLogger(__name__)

class AppConfig:
    def __init__(self):
        self.ENV = os.getenv("ENVIRONMENT")
        self.DATABASE = self._get_db_config(self)

    @staticmethod
    def _get_db_config(self):
        config = self.load_config("JSON/db_config.json")
        return Box({
            "host": config.get("DB_HOST"),
            "database": config.get("DB_NAME"),
            "port": config.get("DB_PORT", 10501),
            "db_conn_pool_size": config.get("DB_POOL_SIZE", 10),
            "db_conn_max_overflow": config.get("DB_MAX_OVERFLOW", 10),
            "hostname": config.get("HOSTNAME_COLUMN"),
            "ipaddress": config.get("IP_ADDRESS_COLUMN")
        })

    def load_config(self, file_path):
        try:
            with open(file_path, "r") as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            raise Exception(f"The file {file_path} not found")
        except json.JSONDecodeError:
            raise Exception(f"Failed to decode JSON from the file {file_path}")

AppConfig = AppConfig()