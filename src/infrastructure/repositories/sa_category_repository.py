from sqlalchemy import (
    Column,
    Integer,
	String,
)

from src.infrastructure.database import Base
from src.library                 import Table


class CategoryTable(Base, Table):
	__tablename__ = 'categories'

	id   = Column(Integer,     primary_key=True)
	name = Column(String(255), nullable=False, unique=True)
