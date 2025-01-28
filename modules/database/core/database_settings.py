import logging
import os
from contextlib import contextmanager
from typing import Mapping, MutableMapping, Union
from unittest import mock

log = logging.getLogger(__name__)

GLOBAL_SETTINGS: MutableMapping[str, Union[bool, str]] = {
    "in_memory": True,  # Default to in-memory for SQLite compatibility
    "sqlite_filename": os.environ.get("SQLITE_FILENAME", "database.sqlite"),  # Updated default SQLite file name
    "database_schema": None,  # Removed schema usage as SQLite does not support schemas
    "use_sqlite": True,  # Set to True since SQLite is now being used
    "table_prefix": os.environ.get("SQL_TABLE_PREFIX", "Import_"),
    "echo_sql": bool(os.environ.get("ECHO_SQL", False)),
}

def get_schema() -> Union[str, None]:
    return GLOBAL_SETTINGS["database_schema"]

def use_in_memory_database() -> bool:
    return GLOBAL_SETTINGS["in_memory"]

def get_sqlite_filename() -> str:
    return GLOBAL_SETTINGS["sqlite_filename"]

def use_sqlite() -> bool:
    return GLOBAL_SETTINGS["use_sqlite"]

def get_table_prefix() -> str:
    return GLOBAL_SETTINGS["table_prefix"]

def get_echo_sql() -> bool:
    return GLOBAL_SETTINGS["echo_sql"]

@contextmanager
def patch_database_settings(**new_settings):
    with mock.patch.dict(GLOBAL_SETTINGS, new_settings):
        yield GLOBAL_SETTINGS
