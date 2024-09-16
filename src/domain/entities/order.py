from typing        import Optional

from src.constants import OrderStatus
from src.library   import Entity, EntityList


class Order(Entity):
	"""
		amount can be fixed only when order is canceled or completed.
		in other cases amount will be dynamically calculated from product price, quantity
		and discount. this is necessary so as not to update the price on each
		uncompleted order when the price of the product is updated
	"""
	user_id    : int
	product_id : int
	quantity   : int
	amount     : Optional[float] = None
	status     : OrderStatus


class OrderList(EntityList[Order]):
	...

