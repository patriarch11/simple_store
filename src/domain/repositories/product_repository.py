from abc                 import abstractmethod
from typing              import Optional

from src.domain.entities import Product, ProductList
from src.library         import RepositoryABC


class ProductRepository(RepositoryABC[Product, ProductList]):
	@abstractmethod
	async def get_list(self,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		...

	@abstractmethod
	async def get_list_with_free_count(self,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		...
