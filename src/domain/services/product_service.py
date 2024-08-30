from typing                  import Optional

from src.domain.entities     import Product, ProductList
from src.domain.repositories import ProductRepository
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	async def get_list_by_category_and_subcategory(self,
		category_id    : Optional[int],
		subcategory_id : Optional[int]
	) -> ProductList:
		filters = {}
		if category_id:
			filters['category_id'] = category_id
		if subcategory_id:
			filters['subcategory_id'] = subcategory_id
		return await self.repo.filter(**filters)
