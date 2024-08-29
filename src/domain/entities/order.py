from src.constants import OrderStatus
from src.library   import BaseEntity


class Order(BaseEntity):
	user_id    : int
	product_id : int
	status     : OrderStatus
