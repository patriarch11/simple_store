from sqlalchemy.ext.asyncio import AsyncSession

from src.constants           import OrderStatus
from src.domain.entities     import Order, OrderList
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[Order, OrderList, OrderRepository]):
	async def update_status(self, s: AsyncSession, order_id: int, status: OrderStatus) -> Order:
		return await self.repo.update(s, order_id, {
			'status': status
		})
