from pydantic      import RootModel, BaseModel

from src.constants import OrderStatus
from src.library   import Schema

class OrderCreateSchema(BaseModel):
	product_id : int
	user_id    : int
	quantity   : int


class CancelOrderSchema(BaseModel):
	id: int

class SellOrderSchema(CancelOrderSchema):
	...

class OrderSchema(Schema):
	user_id              : int
	product_id           : int
	product_price        : float
	product_discount_pct : float
	quantity             : int
	amount               : float
	status               : OrderStatus


class OrderListSchema(RootModel[list[OrderSchema]]):
	...

