import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# Thêm đường dẫn gốc của project vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load các biến môi trường
load_dotenv()

# Import cấu hình database URL
from app.core.config import settings

# Import Base và các models
from app.core.database import Base
from app.models.product import Product  # Import tất cả models ở đây
from app.models.user import User  # Import tất cả models ở đây

# Khởi tạo Alembic Config
config = context.config

# Cấu hình database URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Cấu hình fileConfig
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Đặt target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
