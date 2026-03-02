"""Stubbed database initialization.

In the full application this module would create an SQLAlchemy engine,
configure sessions, and possibly apply migrations.  For now, it contains a
placeholder function so the service/repository layers can import without
error.
"""


def init_db() -> None:
    """Create database connections and prepare schema.

    Raises NotImplementedError to remind developers that the real logic must
    be supplied when integration tests or actual application code are added.
    """
    raise NotImplementedError
