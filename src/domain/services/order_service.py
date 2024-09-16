from src.constants           import OrderStatus
from src.domain.entities     import Order, OrderList
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[Order, OrderList, OrderRepository]):
	@staticmethod
	def calculate_amount(price: float, discount_pct: float, quantity: int) -> float:
		if discount_pct:
			price -= price / 100 * discount_pct
		return price * quantity

	async def update_status(self,
		order_id     : int,
	    status       : OrderStatus,
		price        : float = None,
		discount_pct : float = None,
		quantity     : int   = None
	) -> Order:
		to_update = {'status': status}
		if status in [OrderStatus.CANCELLED, OrderStatus.COMPLETED]:
			# set fixed amount
			to_update['amount'] = self.calculate_amount(price, discount_pct, quantity)
		return await self.repo.update(order_id, to_update)
