# env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from models import Base  # <-- the DeclarativeBase subclass that holds all metadata



target_metadata = Base.metadata

# DATABASE_URL = os.getenv("DATABASE_URL")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")
DATABASE_URL=f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
if not DATABASE_URL:
    raise RuntimeError(
        "Environment variable 'DATABASE_URL' is required but not set."
    )

config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create an Engine using the URL from env var
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        url=DATABASE_URL,          # <-- override any config value
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
