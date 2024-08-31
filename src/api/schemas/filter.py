from typing   import Optional

from fastapi  import Query
from pydantic import BaseModel


class CategoryFilter(BaseModel):
	category_ids    : list[int]
	subcategory_ids : list[int]


class UsersFilter(BaseModel):
	user_ids: list[int]


class ProductsFilter(BaseModel):
	product_ids: list[int]


class SalesReportFilter(CategoryFilter, UsersFilter, ProductsFilter):
	...


class PaginationParams(BaseModel):
	limit  : Optional[int]
	offset : Optional[int]


class CategoryPaginationFilter(CategoryFilter, PaginationParams):
	@classmethod
	def as_query(cls,
		category_ids    : list[int]     = Query([]),
		subcategory_ids : list[int]     = Query([]),
		limit           : Optional[int] = Query(None),
		offset          : Optional[int] = Query(None)
	):
		return cls(**locals())


class SalesReportPaginationFilter(SalesReportFilter, PaginationParams):
	@classmethod
	def as_query(cls,
		category_ids    : list[int]     = Query([]),
		subcategory_ids : list[int]     = Query([]),
		user_ids        : list[int]     = Query([]),
		product_ids     : list[int]     = Query([]),
		limit           : Optional[int] = Query(None),
		offset          : Optional[int] = Query(None)
	):
		return cls(**locals())
