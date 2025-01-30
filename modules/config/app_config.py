import os
import json
import logging
from box import Box

logger = logging.getLogger(__name__)

class AppConfig:
    def __init__(self):
        self.ENV = os.getenv("ENVIRONMENT", "Dev")  # Default to 'Dev' if not set
        self.config = self.load_config("JSON/db_config.json")
        self.database_type = os.getenv("DATABASE_TYPE", self.config.get("database_type", "sqlite")).lower()
        self.DATABASE = self._get_db_config()

    def _get_db_config(self):
        """
        Dynamically loads database configuration based on the selected database type.
        Supports SQLite and SQL Server.
        """
        if self.database_type == "sqlite":
            sqlite_config = self.config.get("sqlite", {})
            return Box({
                "database": os.getenv("SQLITE_DB_PATH", sqlite_config.get("database", "database.sqlite"))
            })

        elif self.database_type == "sqlserver":
            return Box({
                "host": os.getenv("DB_HOST", self.config.get("DB_HOST", "localhost")),
                "database": os.getenv("DB_NAME", self.config.get("DB_NAME", "default_db")),
                "port": int(os.getenv("DB_PORT", self.config.get("DB_PORT", 10501))),
                "db_conn_pool_size": int(os.getenv("DB_POOL_SIZE", self.config.get("DB_POOL_SIZE", 10))),
                "db_conn_max_overflow": int(os.getenv("DB_MAX_OVERFLOW", self.config.get("DB_MAX_OVERFLOW", 10))),
                "hostname": self.config.get("HOSTNAME_COLUMN"),
                "ipaddress": self.config.get("IP_ADDRESS_COLUMN")
            })

        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    @staticmethod
    def load_config(file_path):
        """
        Loads the JSON configuration file.
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"The file {file_path} not found")
        except json.JSONDecodeError:
            raise Exception(f"Failed to decode JSON from the file {file_path}")

AppConfig = AppConfig()