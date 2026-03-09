"""Database engine/session configuration for SteelWorks."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .orm_models import Base

load_dotenv()

DEFAULT_DB_URL = "sqlite+pysqlite:///:memory:"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

engine: Engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def configure_database(database_url: str) -> None:
    """Reconfigure global engine/session factory for a new database URL."""
    global DATABASE_URL, engine, SessionLocal
    DATABASE_URL = database_url
    engine = create_engine(DATABASE_URL, future=True)
    SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def init_db() -> None:
    """Create all tables for the current engine."""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all tables for the current engine."""
    Base.metadata.drop_all(bind=engine, checkfirst=True)


@contextmanager
def get_session() -> Iterator[Session]:
    """Yield a managed SQLAlchemy session with commit/rollback semantics."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
