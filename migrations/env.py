import asyncio
import os
import re
import sys

from logging.config                  import fileConfig

from alembic                         import context
from dotenv                          import load_dotenv
from sqlalchemy                      import pool
from sqlalchemy.engine               import Connection
from sqlalchemy.ext.asyncio          import async_engine_from_config

from src.infrastructure.database     import metadata
from src.infrastructure.repositories import (
	CategoryTable,
	OrderTable,
	ProductTable,
	SubcategoryTable,
)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
	print('DATABASE_URL is specified in environment')
	sys.exit(1)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
	fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_next_migration_number():
	migrations_dir = os.path.join(os.path.dirname(__file__), 'versions')
	existing_migrations = os.listdir(migrations_dir)
	numbers = []
	for filename in existing_migrations:
		match = re.match(r'(\d+)_', filename)
		if match:
			numbers.append(int(match.group(1)))
	if not numbers:
		return '0001'
	else:
		return '{:04}'.format(max(numbers) + 1)


def process_revision_directives(context, revision, directives):
	if context.config.cmd_opts.autogenerate:
		script = directives[0]
		script.rev_id = get_next_migration_number()

def run_migrations_offline() -> None:
	"""Run migrations in 'offline' mode.

	This configures the context with just a URL
	and not an Engine, though an Engine is acceptable
	here as well.  By skipping the Engine creation
	we don't even need a DBAPI to be available.

	Calls to context.execute() here emit the given string to the
	script output.

	"""
	url = config.get_main_option('sqlalchemy.url')
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={'paramstyle': 'named'},
	)

	with context.begin_transaction():
		context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
	context.configure(
		connection                  = connection,
		target_metadata             = target_metadata,
		process_revision_directives = process_revision_directives,
	)

	with context.begin_transaction():
		context.run_migrations()


async def run_async_migrations() -> None:
	"""In this scenario we need to create an Engine
	and associate a connection with the context.

	"""

	connectable = async_engine_from_config(
		config.get_section(config.config_ini_section, {}),
		prefix='sqlalchemy.',
		poolclass=pool.NullPool,
	)

	async with connectable.connect() as connection:
		await connection.run_sync(do_run_migrations)

	await connectable.dispose()


def run_migrations_online() -> None:
	"""Run migrations in 'online' mode."""

	asyncio.run(run_async_migrations())


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
