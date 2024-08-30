from src.domain.entities     import Product
from src.domain.repositories import ProductRepository
from src.domain.services     import OrderService


class ProductUseCase:
	def __init__(self, repo: ProductRepository, order_service: OrderService):
		self.repo          = repo
		self.order_service = order_service

	async def update_count(self, product: Product, count: int) -> Product:
		to_update  = {}
		difference = count - product.total_count
		to_update['total_count'] = count

		if difference < 0: # count was reduced
			if abs(difference) == product.total_count: # count is 0
				free_count = 0
				# cancel all product reservation
				await self.order_service.cancel_reserved_by_product_id(product.id)
			else:
				free_count = product.free_count - difference

		elif difference > 0: # count was increased
			free_count = product.free_count + difference
		else: # count not changed
			return product

		to_update['free_count'] = free_count
		return await self.repo.update(product.id, to_update)

	async def update_price(self, product_id: int, price: float) -> Product:
		await self.order_service.update_reserved_amount_by_product_id(
			product_id,
			price
		)
		return await self.repo.update(product_id, {'price': price})

	async def update_discount(self, product_id: int, dicsount_pct: float) -> Product:
		await self.order_service.update_reserved_discount_by_product_id(
			product_id,
			dicsount_pct
		)
		return await self.repo.update(product_id, {'discount_pct': dicsount_pct})

	async def delete(self, product_id: int):
		await self.order_service.delete_by_product_id(product_id)
		await self.repo.delete(product_id)
