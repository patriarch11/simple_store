from abc                    import abstractmethod
from typing                 import Optional

from sqlalchemy.ext.asyncio import  AsyncSession

from src.domain.entities    import Product, ProductList
from src.library            import RepositoryABC


class ProductRepository(RepositoryABC[Product, ProductList]):
	@classmethod
	@abstractmethod
	async def get_list_of_available(self,
	    s               : AsyncSession,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		...
