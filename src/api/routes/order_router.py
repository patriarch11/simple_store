from fastapi          import APIRouter, status

from src.api.schemas  import (
	OrderSchema,
	OrderCreateSchema,
	CancelOrderSchema,
	SellOrderSchema
)
from src.dependencies import get_order_use_case


class OrderRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.use_case = get_order_use_case()
		self.add_api_route(
			'/create',
			self.create,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED:  {
					'model'       : OrderSchema,
					'description' : 'Order created, product reserved'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Invalid quantity'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Product not found'
				}
			}
		)
		self.add_api_route(
			'/cancel',
			self.cancel,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK:  {
					'model'       : OrderSchema,
					'description' : 'Order canceled'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Order status must be "RESERVED"'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Order not found'
				}
			}
		)
		self.add_api_route(
			'/sell',
			self.sell,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK:  {
					'model'       : OrderSchema,
					'description' : 'Product sold'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Order status must be "RESERVED"'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Order not found'
				}
			}
		)

	async def create(self, order: OrderCreateSchema) -> OrderSchema:
		return OrderSchema.from_entity(
			await self.use_case.create(order.product_id, order.user_id, order.quantity)
		)

	async def cancel(self, order: CancelOrderSchema) -> OrderSchema:
		return OrderSchema.from_entity(
			await self.use_case.cancel(order.id)
		)

	async def sell(self, order: SellOrderSchema) -> OrderSchema:
		return OrderSchema.from_entity(
			await self.use_case.sell(order.id)
		)

router = OrderRouter()
