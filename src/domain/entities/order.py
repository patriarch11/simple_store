from src.constants import OrderStatus
from src.library   import Entity


class Order(Entity):
	user_id    : int
	product_id : int
	status     : OrderStatus
