from sqlalchemy                 import MetaData
from sqlalchemy.ext.asyncio     import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker

from src.config                 import settings
from src.constants              import DB_NAMING_CONVENTION


metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
engine   = create_async_engine(
    str(settings.DATABASE_URL),
    echo = settings.DEBUG, # displaying SQL queries in the console
)

Base           = declarative_base(metadata=metadata)
SessionFactory = sessionmaker(
    bind             = engine,
    class_           = AsyncSession,
    # expire_on_commit = False # Sessions do not lose the object after a commit
)
