from sqlalchemy import (
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

	id           = Column(Integer, primary_key=True)
	user_id      = Column(Integer, nullable=False)
	product_id   = Column(Integer, ForeignKey('products.id'), nullable=False)
	discount_pct = Column(Float,   nullable=False, default=0.0)
	amount       = Column(Float,   nullable=False, default=0.0)
	status       = Column(Enum(OrderStatus), nullable=False)


class SaOrderRepository(
	Repository[Order, OrderList, OrderTable],
	OrderRepository
):
	entity      = Order
	entity_list = OrderList
	table       = OrderTable

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
