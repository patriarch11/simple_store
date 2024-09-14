from src.constants           import OrderStatus
from src.domain.entities     import BaseOrder, OrderList
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[BaseOrder, OrderList, OrderRepository]):
	async def update_status(self, order_id: int, status: OrderStatus) -> BaseOrder:
		return await self.repo.update(order_id, {
			'status': status
		})
