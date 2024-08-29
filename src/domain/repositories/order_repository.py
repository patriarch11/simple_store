from src.domain.entities import Order, OrderList
from src.library         import RepositoryABC


class OrderRepository(RepositoryABC[Order, OrderList]):
	...
