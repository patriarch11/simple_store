from src.constants import OrderStatus
from src.library   import BaseModel


class Order(BaseModel):
	user_id    : int
	product_id : int
	status     : OrderStatus
