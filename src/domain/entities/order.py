from src.constants import OrderStatus
from src.library   import Entity, EntityList


class BaseOrder(Entity):
	user_id    : int
	product_id : int
	quantity   : int
	status     : OrderStatus


class Order(BaseOrder):
	amount : float

	@classmethod
	def from_base_and_product(cls,
	    base_order   : BaseOrder,
	    price        : float,
	    discount_pct : float,
	) -> 'Order':
		if discount_pct:
			price = price - (price / 100 * discount_pct)
		return cls(
			**base_order.model_dump(),
			amount = base_order.quantity * price
		)

class OrderList(EntityList[Order]):
	...

