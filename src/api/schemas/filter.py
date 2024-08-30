from typing   import Optional

from fastapi  import Query
from pydantic import BaseModel


class CategoryFilter(BaseModel):
	category_id    : Optional[int]
	subcategory_id : Optional[int]

	@classmethod
	def as_query(cls,
		category_id    : Optional[int] = Query(None),
		subcategory_id : Optional[int] = Query(None)
	):
		return cls(**locals())
