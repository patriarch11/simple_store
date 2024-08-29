from typing     import Type

from sqlalchemy import (
    Column,
    Integer,
	String,
)

from src.domain.entities.category  import Category
from src.domain.repositories       import CategoryRepository
from src.infrastructure.database   import Base
from src.library                   import Repository, Table


class CategoryTable(Table, Base):
	__tablename__ = 'categories'

	id   = Column(Integer,     primary_key=True)
	name = Column(String(255), nullable=False, unique=True)


class SaCategoryRepository(Repository, CategoryRepository):
	table  : Type[CategoryTable] = CategoryTable
	entity : Type[Category]      = Category
