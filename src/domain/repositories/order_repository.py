from src.domain.entities import Order
from src.library         import RepositoryABC


class OrderRepository(RepositoryABC[Order]):
	...
