from src.constants import OrderStatus
from src.library   import Entity, EntityList


class Order(Entity):
	user_id              : int
	product_id           : int
	product_price        : float
	product_discount_pct : float
	quantity             : int
	amount               : float
	status               : OrderStatus


class OrderList(EntityList[Order]):
	...

