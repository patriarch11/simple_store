from sqlalchemy import (
    Column,
    Integer,
	String,
)

from src.domain.entities         import Category, CategoryList
from src.domain.repositories     import CategoryRepository
from src.infrastructure.database import Base
from src.library                 import Repository, Table


class CategoryTable(Table, Base):
	__tablename__ = 'categories'

	id   = Column(Integer,     primary_key=True)
	name = Column(String(255), nullable=False, unique=True)


class SaCategoryRepository(
	Repository[Category, CategoryList, CategoryTable],
	CategoryRepository
):
	entity      = Category
	entity_list = CategoryList
	table       = CategoryTable
