from typing   import Optional

from fastapi  import Query
from pydantic import BaseModel


class CategoryFilter(BaseModel):
	category_ids    : list[int]
	subcategory_ids : list[int]

	@classmethod
	def as_query(cls,
		category_ids    : list[int] = Query([]),
		subcategory_ids : list[int] = Query([])
	):
		return cls(**locals())


class PaginationParams(BaseModel):
	limit  : Optional[int]
	offset : Optional[int]

	@classmethod
	def as_query(cls,
		limit  : Optional[int] = Query(None),
		offset : Optional[int] = Query(None)
	):
		return cls(**locals())


class CategoryPaginationFilter(CategoryFilter, PaginationParams):
	@classmethod
	def as_query(cls,
		category_ids    : list[int]     = Query([]),
		subcategory_ids : list[int]     = Query([]),
		limit           : Optional[int] = Query(None),
		offset          : Optional[int] = Query(None)
	):
		return cls(**locals())
