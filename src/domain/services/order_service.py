from src.constants           import OrderStatus
from src.domain.entities     import Order, OrderList
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[Order, OrderList, OrderRepository]):
	async def cancel_reserved_by_product_id(self, product_id: int):
		await self.repo.update_many_by_product_id_and_status(
			product_id,
			OrderStatus.RESERVED,
			{'status': OrderStatus.CANCELLED}
		)

	async def update_reserved_product_price_by_product_id(self, product_id: int, product_price: float):
		await self.repo.update_many_by_product_id_and_status(
			product_id,
			OrderStatus.RESERVED,
			{'product_price': product_price}
		)

	async def update_reserved_discount_by_product_id(self, product_id: int, discount_pct: float):
		await self.repo.update_many_by_product_id_and_status(
			product_id,
			OrderStatus.RESERVED,
			{'discount_pct': discount_pct}
		)

	async def update_status(self, order_id: int, status: OrderStatus) -> Order:
		return await self.repo.update(order_id, {
			'status': status
		})

	async def delete_by_product_id(self, product_id: int):
		await self.repo.delete_many_by_product_id(product_id)
