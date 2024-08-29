from sqlalchemy import (
    Column,
    Integer,
	String,
	ForeignKey
)

from src.domain.entities          import Subcategory, SubcategoryList
from src.domain.repositories      import SubcategoryRepository
from src.infrastructure.database  import Base
from src.library                  import Repository, Table


class SubcategoryTable(Base, Table):
	__tablename__ = 'subcategories'

	id          = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False, index=True)
	name        = Column(String(255), nullable=False, unique=True)


class SaSubcategoryRepository(
	Repository[Subcategory, SubcategoryList, SubcategoryTable],
	SubcategoryRepository
):
	entity      = Subcategory
	entity_list = SubcategoryList
	table       = SubcategoryTable
