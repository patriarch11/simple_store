from abc                    import abstractmethod
from typing                 import Optional

from sqlalchemy.ext.asyncio import  AsyncSession

from src.domain.entities    import Product, ProductList
from src.library            import RepositoryABC


class ProductRepository(RepositoryABC[Product, ProductList]):
	@classmethod
	@abstractmethod
	async def get_list_of_available(cls,
	    s               : AsyncSession,
		category_ids    : list[int],
		subcategory_ids : list[int],
		limit           : Optional[int],
		offset          : Optional[int]
	) -> ProductList:
		...

	@classmethod
	@abstractmethod
	async def get_list_by_filters(cls,
	    s               : AsyncSession,
	    ids             : Optional[list[int]],
		category_ids    : Optional[list[int]],
		subcategory_ids : Optional[list[int]]
	) -> ProductList:
		"""Fetch a list of products, applying an 'OR' condition to the provided filters."""
		...
