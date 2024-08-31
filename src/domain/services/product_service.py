from typing                  import Optional

from src.domain.entities     import Product, ProductList
from src.domain.repositories import ProductRepository
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	async def create(self, product: Product) -> Product:
		product.free_count = product.total_count
		return await super().create(product)

	async def get_list_with_free_count(self,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		return await self.repo.get_list_with_free_count(category_ids, subcategory_ids, limit, offset)

	async def increase_free_count(self, product: Product, increment: int):
		free_count = product.free_count + increment
		await self.repo.update(product.id, {
			'free_count': free_count
		})

	async def decrease_free_count(self, product: Product, decrement: int):
		free_count = product.free_count - decrement
		await self.repo.update(product.id, {
			'free_count': free_count
		})

	async def decrease_total_count(self, product: Product, decrement: int):
		total_count = product.total_count - decrement
		await self.repo.update(product.id, {
			'total_count': total_count
		})
