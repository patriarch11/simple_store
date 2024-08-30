from abc                 import abstractmethod

from src.constants       import OrderStatus
from src.domain.entities import Order, OrderList
from src.library         import RepositoryABC


class OrderRepository(RepositoryABC[Order, OrderList]):
	@abstractmethod
	async def update_many_by_product_id_and_status(self,
		product_id : int,
		status     : OrderStatus,
		to_update  : dict
	) -> None:
		...

	@abstractmethod
	async def delete_many_by_product_id(self, product_id: int) -> None:
		...
