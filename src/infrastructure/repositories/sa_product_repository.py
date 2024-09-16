from typing                      import Optional

from sqlalchemy                  import (
    Column,
    Integer,
    Float,
	String,
    ForeignKey,

	select,
	or_
)
from sqlalchemy.ext.asyncio       import AsyncSession

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
	discount_pct   = Column(Float,   nullable=False, default=0.0)
	price          = Column(Float,   nullable=False, default=0.0)
	total_count    = Column(Integer, nullable=False)
	reserved_count = Column(Integer, nullable=False)


class SaProductRepository(
	Repository[Product, ProductList, ProductTable],
	ProductRepository
):
	entity      = Product
	entity_list = ProductList
	table       = ProductTable

	@classmethod
	def _list_q(cls,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	):
		q = cls.select_q()
		if len(category_ids):
			q = q.where(
				cls.table.category_id.in_(category_ids)
			)
		if len(subcategory_ids):
			q = q.where(
				cls.table.subcategory_id.in_(subcategory_ids)
			)
		return cls.paginate_q(q, limit, offset)

	@classmethod
	async def get_list_of_available(cls,
	    s               : AsyncSession,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		return cls.entity_list.model_validate(
			await cls.fetch_many(
				s,
				cls._list_q(
					category_ids,
					subcategory_ids,
					limit,
					offset
				).where(cls.table.total_count > cls.table.reserved_count)
			)
		)

	@classmethod
	async def get_list_by_filters(cls,
		s               : AsyncSession,
		ids             : Optional[list[int]],
		category_ids    : Optional[list[int]],
		subcategory_ids : Optional[list[int]]
	) -> ProductList:
		or_clauses = []
		if ids and len(ids):
			or_clauses.append(cls.table.id.in_(ids))
		if category_ids and len(category_ids):
			or_clauses.append(cls.table.category_id.in_(category_ids))
		if subcategory_ids and len(subcategory_ids):
			or_clauses.append(cls.table.subcategory_id.in_(subcategory_ids))
		q = select(cls.table)
		if len(or_clauses):
			q = q.where(or_(*or_clauses))
		res = await s.execute(q)
		rows = res.fetchall()
		return cls.entity_list.model_validate(
			[dict(r[0].__dict__) for r in rows]
		)
