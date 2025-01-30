import os
import platform
from urllib.parse import quote_plus
import logging
from modules.config.app_config import AppConfig as CONFIG

log = logging.getLogger(__name__)

def get_database_connection_string() -> str:
    """
    Generates a dynamic database connection string.
    Supports SQL Server (ODBC) and SQLite as of now, with room for expansion.
    """
    
    # Get database type from ENV (Default: SQLite)
    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if database_type == "sqlserver":
        return get_sql_server_connection_string()
    elif database_type == "sqlite":
        return get_sqlite_connection_string()
    else:
        raise ValueError(f"Unsupported database type: {database_type}")

def get_sql_server_connection_string() -> str:
    """
    Generates a connection string for SQL Server using environment variables.
    """
    default_host: str = CONFIG.DATABASE.host
    default_instance: str = CONFIG.DATABASE.instance if hasattr(CONFIG.DATABASE, "instance") else ""
    default_database: str = CONFIG.DATABASE.database
    default_port: int = CONFIG.DATABASE.port
    get_platform = platform.system()
    env = os.getenv("ENVIRONMENT")
    default_multi_subnet_failover: str = CONFIG.DATABASE.multi_subnet_failover if hasattr(CONFIG.DATABASE, "multi_subnet_failover") else ""

    database_host = os.getenv("SQL_HOST", default_host)
    database_name = os.getenv("SQL_DATABASE", default_database)
    database_instance = os.getenv("SQL_INSTANCE", default_instance)
    database_port = os.getenv("SQL_PORT", str(default_port))
    database_multi_subnet_failover = os.getenv("SQL_MULTI_SUBNET_FAILOVER", default_multi_subnet_failover)

    default_database_driver = (
        "/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1"
        if get_platform == "Linux"
        else "ODBC Driver 17 for SQL Server"
    )

    database_driver = os.getenv("DATABASE_DRIVER", default_database_driver)
    database_driver_with_brackets = f"{{{database_driver}}}"

    server = f"{database_host},{database_port}" if get_platform == "Linux" else f"{database_host}\\{database_instance}"

    connection_parameter_string = (
        f"DRIVER={database_driver_with_brackets};SERVER={server};"
        f"DATABASE={database_name};"
        f"Integrated Security=true;Trusted_Connection=Yes;"
    )

    if len(database_multi_subnet_failover):
        connection_parameter_string += f"{database_multi_subnet_failover};"

    log.info(f"SQL Server connection string: {connection_parameter_string}")
    
    params = quote_plus(connection_parameter_string)
    
    return f"mssql+pyodbc://?odbc_connect={params}"

def get_sqlite_connection_string() -> str:
    """
    Generates a connection string for SQLite.
    """
    default_sqlite_path = os.getenv("SQLITE_DB_PATH", "database.sqlite")
    
    log.info(f"Using SQLite database at: {default_sqlite_path}")
    
    return f"sqlite:///{default_sqlite_path}"