from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context

# Importar os modelos para 'autogenerate'
import models.__all_models
from core.config import settings

# Alembic Config object, acesso aos valores do .ini file
config = context.config

# Configurar o logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData do modelo
target_metadata = settings.DBBaseModel.metadata

# Pegar a URL do banco de dados usando a função DB_URL
def get_database_url():
    return settings.DB_URL

# Migrations offline
def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Migrations online
def run_migrations_online() -> None:
    url = get_database_url()
    connectable = create_engine(url, poolclass=pool.NullPool)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()