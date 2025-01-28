import logging
from contextlib import contextmanager
from modules.database.core.base import PublicBase
from functools import lru_cache, wraps
from typing import Iterator
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from modules.database.core.database_settings import (
    get_echo_sql, patch_database_settings, use_sqlite
)
from modules.database.core.sqlite import get_sqlite_connection_string
from sqlalchemy import create_engine
from modules.config.app_config import AppConfig as CONFIG
from pydash import get

log = logging.getLogger(__name__)

def in_memory(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        with patch_database_settings(in_memory=True):
            return fn(*args, **kwargs)
    return inner

def get_connection_string() -> str:
    connection_string = get_sqlite_connection_string() if use_sqlite() else ""
    log.info(f"Using connection string {connection_string}.")
    return connection_string

@lru_cache()
def get_engine() -> Engine:
    connection_params = {}
    if not use_sqlite():
        # SQLite engine does not support these params
        connection_params = {
            "pool_size": get(CONFIG.DATABASE, "database.db_conn_pool_size", 10),
            "max_overflow": get(CONFIG.DATABASE, "database.db_conn_max_overflow", 10),
        }
    engine = create_engine(
        get_connection_string(),
        echo=get_echo_sql(),
        **connection_params
    )
    PublicBase.metadata.bind = engine
    PublicBase.metadata.create_all(engine)
    return engine

@event.listens_for(Engine, "connect")
def attached_db(dbapi_conn, rec):
    if use_sqlite():
        log.debug("SQLite database connection established.")

@lru_cache()
def get_sessionmaker() -> sessionmaker:
    engine = get_engine()
    s = sessionmaker(bind=engine)
    s.configure(bind=engine)
    return s

def get_session() -> Session:
    return get_sessionmaker()()

@contextmanager
def disable_integrity_checks(engine: Engine, table_name: str):
    if not use_sqlite():
        engine.execute(f"ALTER TABLE {table_name} NOCHECK CONSTRAINT ALL")
    yield
    if not use_sqlite():
        engine.execute(f"ALTER TABLE {table_name} CHECK CONSTRAINT ALL")

@contextmanager
def session_scope(
    scope_name: str = "Unnamed session", **extra_settings
) -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.
    """
    with patch_database_settings(**extra_settings):
        session: Session = get_sessionmaker()()
        try:
            yield session
            session.commit()
        except:
            log.exception(f"Rolling back session {scope_name}")
            session.rollback()
            raise
        else:
            log.info(f"Session {scope_name} closing normally.")
        finally:
            session.close()

if __name__ == "__main__":
    log.debug(get_connection_string())
    ss = get_session()
    log.debug(ss.__class__)
    ee = get_engine()
    log.debug(ee)
    with session_scope() as session:
        print(session)
