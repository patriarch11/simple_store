from sqlalchemy                  import MetaData
from sqlalchemy.ext.declarative  import declarative_base

from src.constants               import DB_NAMING_CONVENTION
from src.library                 import Model

metadata  = MetaData(naming_convention=DB_NAMING_CONVENTION)
Base      = declarative_base(metadata=metadata)


class BaseModel(Base, Model):
	...
	