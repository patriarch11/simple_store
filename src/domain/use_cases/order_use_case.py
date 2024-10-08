from fastapi                import  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants          import OrderStatus
from src.domain.entities    import Order
from src.domain.services    import OrderService, ProductService


class OrderUseCase:
	@staticmethod
	def _calculate_amount(price: float, discount: float, quantity: int) -> float:
		if discount > 0:
			price -= price / 100 * discount
		return price * quantity

	def __init__(self,
	    order_service   : OrderService,
	    product_service : ProductService,
	):
		self.order_service   = order_service
		self.product_service = product_service

	async def _get_reserved_order_by_id(self, s: AsyncSession, order_id: int) -> Order:
		order = await self.order_service.get_by_id(s, order_id)
		if not order:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
		if order.status != OrderStatus.RESERVED:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Order not reserved')
		return order

	async def create(self, s: AsyncSession, product_id: int, user_id: int, quantity: int) -> Order:
		if quantity <= 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Quantity can\'n be less or equal 0')

		product = await self.product_service.get_by_id(s, product_id)
		await self.product_service.update_reserved_count(s, product, quantity)

		return await self.order_service.create(s, Order(
			user_id              = user_id,
			product_id           = product.id,
			product_price        = product.price,
			product_discount_pct = product.discount_pct,
			quantity             = quantity,
			amount               = self._calculate_amount(product.price, product.discount_pct, quantity),
			status               = OrderStatus.RESERVED
		))

	async def cancel(self, s: AsyncSession, order_id: int) -> Order:
		order   = await self._get_reserved_order_by_id(s, order_id)
		product = await self.product_service.get_by_id(s, order.product_id)

		_ = await self.product_service.update_reserved_count(s, product, -order.quantity)

		return await self.order_service.update_status(s, order.id, OrderStatus.CANCELLED)

	async def sell(self, s: AsyncSession, order_id: int) -> Order:
		order   = await self._get_reserved_order_by_id(s, order_id)
		product = await self.product_service.get_by_id(s, order.product_id)

		product = await self.product_service.update_reserved_count(s, product, -order.quantity)
		_ = await self.product_service.update_total_count(s, product, -order.quantity)

		return await self.order_service.update_status(s, order.id, OrderStatus.COMPLETED)
