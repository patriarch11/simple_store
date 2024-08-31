from typing                  import Optional

from src.domain.entities     import OrderList
from src.domain.repositories import OrderRepository
from src.domain.services     import ProductService


class OrderUseCase:
	def __init__(self, repo: OrderRepository, product_service: ProductService):
		self.repo         = repo
		self.product_service = product_service

	async def get_list_of_completed(self,
		category_ids    : list[int],
		subcategory_ids : list[int],
		user_ids        : list[int],
		product_ids     : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> OrderList:
		if len(category_ids) or len(subcategory_ids):
			products = await self.product_service.get_list(
				category_ids,
				subcategory_ids,
				None,
				None
			)
			product_ids.extend(
				[p.id for p in products.root]
			)
		return await self.repo.get_list_of_completed(
			user_ids,
			product_ids,
			limit,
			offset
		)
