from typing                  import Optional

from src.domain.entities     import Product, ProductList
from src.domain.repositories import ProductRepository
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	async def get_list(self,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		return await self.repo.get_list(category_ids, subcategory_ids, limit, offset)
