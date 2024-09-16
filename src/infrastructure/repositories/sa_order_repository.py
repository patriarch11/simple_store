from typing                     import Optional

from sqlalchemy                 import (
    Column,
    Integer,
    Float,
    ForeignKey,
	Enum,

	update,
	delete,

	and_
)

from src.constants                import OrderStatus
from src.domain.entities          import Order, OrderList
from src.domain.repositories      import OrderRepository
from src.infrastructure.database  import Base
from src.library                  import Repository, Table


class OrderTable(Base, Table):
	__tablename__ = 'orders'

	"""
		amount can be fixed only when order is canceled or completed.
		in other cases amount will be dynamically calculated from product price, quantity
		and discount. this is necessary so as not to update the price on each
		uncompleted order when the price of the product is updated
	"""

	id         = Column(Integer, primary_key=True)
	user_id    = Column(Integer, nullable=False)
	product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
	quantity   = Column(Integer, nullable=False)
	amount     = Column(Float,   nullable=True)
	status     = Column(Enum(OrderStatus), nullable=False)


class SaOrderRepository(
	Repository[Order, OrderList, OrderTable],
	OrderRepository
):
	entity      = Order
	entity_list = OrderList
	table       = OrderTable

	def _list_q(self,
		user_ids    : list[int],
		product_ids : list[int],
		limit       : Optional[int],
		offset      : Optional[int]
	):
		q = self.select_q
		if len(user_ids):
			q = q.where(
				self.table.user_id.in_(user_ids)
			)
		if len(product_ids):
			q = q.where(
				self.table.product_id.in_(product_ids)
			)
		return self.paginate_q(q, limit, offset)

	async def get_list(self,
		user_ids    : list[int],
		product_ids : list[int],
		limit       : Optional[int],
		offset      : Optional[int]
	) -> OrderList:
		return self.entity_list.model_validate(
			await self.fetch_many(
				self._list_q(
					user_ids,
					product_ids,
					limit,
					offset
				)
			)
		)

	async def get_list_of_completed(self,
		user_ids    : list[int],
		product_ids : list[int],
		limit       : Optional[int],
		offset      : Optional[int]
	) -> OrderList:
		return self.entity_list.model_validate(
			await self.fetch_many(
				self._list_q(
					user_ids,
					product_ids,
					limit,
					offset
				).where(self.table.status == OrderStatus.COMPLETED)
			)
		)

	async def update_many_by_product_id_and_status(self,
		product_id : int,
		status     : OrderStatus,
		to_update  : dict
	) -> None:
		await self.execute(
			update(self.table)
				.values(**to_update)
				.where(and_(
					self.table.product_id == product_id,
					self.table.status     == status
				))
		)

	async def delete_many_by_product_id(self, product_id: int) -> None:
		await self.execute(
			delete(self.table)
				.where(self.table.product_id == product_id)
		)
