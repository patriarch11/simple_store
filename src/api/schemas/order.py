from pydantic      import RootModel, BaseModel

from src.constants import OrderStatus
from src.library   import ResponseSchema


class OrderRequest(BaseModel):
	order_id: int


class OrderResponse(ResponseSchema):
	user_id       : int
	product_id    : int
	quantity      : int
	product_price : float
	discount_pct  : float
	status        : OrderStatus


class OrderListResponse(RootModel[list[OrderResponse]]):
	...
