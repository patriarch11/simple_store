from sqlalchemy import (
    Column,
    Integer,
	String,
    ForeignKey,
)

from src.domain.entities          import Product, ProductList
from src.domain.repositories      import ProductRepository
from src.infrastructure.database  import Base
from src.library                  import Repository, Table


class ProductTable(Base, Table):
	__tablename__ = 'products'

	id             = Column(Integer, primary_key=True)
	category_id    = Column(Integer, ForeignKey('categories.id'),    nullable=False)
	subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False)
	name           = Column(String(255), nullable=False)
	discount_pct   = Column(Integer)
	price          = Column(Integer, nullable=False)
	total_count    = Column(Integer, nullable=False)
	free_count     = Column(Integer, nullable=False)


class SaProductRepository(
	Repository[Product, ProductList, ProductTable],
	ProductRepository
):
	entity      = Product
	entity_list = ProductList
	table       = ProductTable
