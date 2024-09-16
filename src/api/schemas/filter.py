from typing        import Optional

from fastapi       import Query, HTTPException, status as http_status, Depends
from pydantic      import BaseModel

from src.constants import SalesReportOrder, SortOrder, OrderStatus

def validate_order_status(status: Optional[int] = Query(None)) -> Optional[OrderStatus]:
	if status:
		try:
			return OrderStatus(status)
		except ValueError:
			raise HTTPException(http_status.HTTP_422_UNPROCESSABLE_ENTITY, f'Invalid order satus: {status}')
	return None


class CategoryFilter(BaseModel):
	category_ids    : list[int]
	subcategory_ids : list[int]


class UsersFilter(BaseModel):
	user_ids: list[int]


class ProductsFilter(BaseModel):
	product_ids: list[int]


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


class SalesReportFilter(CategoryFilter, UsersFilter, ProductsFilter):
	status             : Optional[OrderStatus]
	product_price_from : Optional[float]
	product_price_to   : Optional[float]
	amount_from        : Optional[float]
	amount_to          : Optional[float]
	order_by           : Optional[SalesReportOrder]
	sort_by            : Optional[SortOrder]

	@classmethod
	def as_query(cls,
		category_ids       : list[int]                  = Query([]),
		subcategory_ids    : list[int]                  = Query([]),
		user_ids           : list[int]                  = Query([]),
		product_ids        : list[int]                  = Query([]),
	    status             : Optional[OrderStatus]      = Depends(validate_order_status),
	    product_price_from : Optional[float]            = Query(None),
	    product_price_to   : Optional[float]            = Query(None),
	    amount_from        : Optional[float]            = Query(None),
		amount_to          : Optional[float]            = Query(None),
	    order_by           : Optional[SalesReportOrder] = Query(None),
	    sort_by            : Optional[SortOrder]        = Query(None),
	):
		return cls(**locals())
