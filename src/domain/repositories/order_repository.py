from abc                    import abstractmethod
from typing                 import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.constants          import SalesReportOrder, SortOrder, OrderStatus
from src.domain.entities    import Order, OrderList
from src.library            import RepositoryABC


class OrderRepository(RepositoryABC[Order, OrderList]):
	@classmethod
	@abstractmethod
	async def delete_many_by_product_id(cls, s: AsyncSession, product_id: int) -> None:
		...

	@classmethod
	@abstractmethod
	async def update_reserved_amount_by_product_id(cls, s: AsyncSession, product_id: int):
			...

	@classmethod
	@abstractmethod
	async def update_reserved_by_product_id(cls, s: AsyncSession, product_id: int, to_update: dict):
		...

	@classmethod
	@abstractmethod
	async def get_list_by_filters(cls,
		s                  : AsyncSession,
	    status             : Optional[OrderStatus],
	    user_ids           : Optional[list[int]],
	    product_ids        : Optional[list[int]],
	    product_price_from : Optional[float],
	    product_price_to   : Optional[float],
	    amount_from        : Optional[float],
	    amount_to          : Optional[float],
	    order_by           : Optional[SalesReportOrder],
	    sort               : Optional[SortOrder],
	) -> OrderList:
		"""Fetch a list of orders, applying an 'AND' condition to the provided filters."""
		...