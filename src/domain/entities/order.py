from src.constants import OrderStatus
from src.library   import Entity, EntityList


class Order(Entity):
	user_id      : int
	product_id   : int
	amount       : float
	discount_pct : float
	status       : OrderStatus


class OrderList(EntityList[Order]):
	...
