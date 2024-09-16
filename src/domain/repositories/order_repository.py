from abc                    import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

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
