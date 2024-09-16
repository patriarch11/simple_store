from fastapi             import  HTTPException, status

from src.constants       import OrderStatus
from src.domain.entities import BaseOrder, Order
from src.domain.services import OrderService, ProductService


class OrderUseCase:
	def __init__(self, order_service: OrderService, product_service: ProductService):
		self.order_service   = order_service
		self.product_service = product_service

	async def _get_reserved_order_by_id(self, order_id: int) -> BaseOrder:
		order = await self.order_service.get_by_id(order_id)
		if not order:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
		if order.status != OrderStatus.RESERVED:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Order not reserved')
		return order

	async def create(self, product_id: int, user_id: int, quantity: int) -> Order:
		if quantity <= 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Quantity can\'n be less or equal 0')

		product = await self.product_service.get_by_id(product_id)
		await self.product_service.update_reserved_count(product, quantity)

		order = await self.order_service.create(BaseOrder(
			user_id       = user_id,
			product_id    = product.id,
			quantity      = quantity,
			status        = OrderStatus.RESERVED
		))
		return Order.from_base_and_product(order, product.price, product.discount_pct)

	async def cancel(self, order_id: int) -> Order:
		order   = await self._get_reserved_order_by_id(order_id)
		product = await self.product_service.get_by_id(order.product_id)

		_ = await self.product_service.update_reserved_count(product, -order.quantity)

		order = await self.order_service.update_status(order.id, OrderStatus.CANCELLED)
		return Order.from_base_and_product(order, product.price, product.discount_pct)

	async def sell(self, order_id: int) -> Order:
		order   = await self._get_reserved_order_by_id(order_id)
		product = await self.product_service.get_by_id(order.product_id)

		product = await self.product_service.update_reserved_count(product, -order.quantity)
		_ = await self.product_service.update_total_count(product, -order.quantity)

		order = await self.order_service.update_status(order.id, OrderStatus.COMPLETED)
		return Order.from_base_and_product(order, product.price, product.discount_pct)
