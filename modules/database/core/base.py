from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Removed get_schema since SQLite does not support schemas
PublicBase = declarative_base(
    metadata=MetaData(),  # Removed schema parameter for SQLite compatibility
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

class Base(PublicBase):
    __abstract__ = True
