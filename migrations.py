from alembic import context
from sqlalchemy import create_engine

from core.config import settings
import models.__all_models


def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


def run_migrations_offline():
    context.configure(url=settings.DB_URL,
                      target_metadata=settings.DBBaseModel.metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(settings.DB_URL)
    connection = engine.connect()
    context.configure(connection=connection,
                      target_metadata=settings.DBBaseModel.metadata)

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


run_migrations()