from abc                 import abstractmethod
from typing              import Optional

from src.domain.entities import Order, OrderList
from src.library         import RepositoryABC


class OrderRepository(RepositoryABC[Order, OrderList]):
	@abstractmethod
	async def get_list(self,
		user_ids    : list[int],
		product_ids : list[int],
		limit       : Optional[int],
		offset      : Optional[int]
	) -> OrderList:
		...

	@abstractmethod
	async def get_list_of_completed(self,
		user_ids    : list[int],
		product_ids : list[int],
		limit       : Optional[int],
		offset      : Optional[int]
	) -> OrderList:
		...

	@abstractmethod
	async def delete_many_by_product_id(self, product_id: int) -> None:
		...
