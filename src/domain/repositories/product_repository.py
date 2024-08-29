from src.domain.entities import Product, ProductList
from src.library         import RepositoryABC


class ProductRepository(RepositoryABC[Product, ProductList]):
	...
