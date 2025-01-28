import os
import tempfile
from modules.database.core.database_settings import (
    get_sqlite_filename,
    use_in_memory_database,
)

def get_tempfile_for_database() -> str:
    """
    Returns the file path for a temporary SQLite database.
    """
    tempdir: str = tempfile.gettempdir()
    return os.path.join(tempdir, f"{get_sqlite_filename()}.sqlite")

def get_sqlite_connection_string() -> str:
    """
    Returns the SQLite connection string, either for an in-memory database or a file-based database.
    """
    filename = ":memory:" if use_in_memory_database() else get_sqlite_filename()
    return f"sqlite:///{filename}"
