from sqlalchemy                 import (
    Column,
    Integer,
    Float,
    ForeignKey,
	Enum,

	update,
	delete,

	and_,
	case,
)
from sqlalchemy.ext.asyncio       import AsyncSession

from src.constants                import OrderStatus
from src.domain.entities          import Order, OrderList
from src.domain.repositories      import OrderRepository
from src.infrastructure.database  import Base
from src.library                  import Repository, Table


class OrderTable(Base, Table):
	__tablename__ = 'orders'

	id                   = Column(Integer, primary_key=True)
	user_id              = Column(Integer, nullable=False)
	product_id           = Column(Integer, ForeignKey('products.id'), nullable=False)
	product_price        = Column(Float,   nullable=False)
	product_discount_pct = Column(Float,   nullable=False)
	quantity             = Column(Integer, nullable=False)
	amount               = Column(Float,   nullable=False)
	status               = Column(Enum(OrderStatus), nullable=False)


class SaOrderRepository(
	Repository[Order, OrderList, OrderTable],
	OrderRepository
):
	entity      = Order
	entity_list = OrderList
	table       = OrderTable

	# def _list_q(self,
	# 	user_ids    : list[int],
	# 	product_ids : list[int],
	# 	limit       : Optional[int],
	# 	offset      : Optional[int]
	# ):
	# 	q = self.select_q
	# 	if len(user_ids):
	# 		q = q.where(
	# 			self.table.user_id.in_(user_ids)
	# 		)
	# 	if len(product_ids):
	# 		q = q.where(
	# 			self.table.product_id.in_(product_ids)
	# 		)
	# 	return self.paginate_q(q, limit, offset)
	#
	# async def get_list(self,
	# 	user_ids    : list[int],
	# 	product_ids : list[int],
	# 	limit       : Optional[int],
	# 	offset      : Optional[int]
	# ) -> OrderList:
	# 	return self.entity_list.model_validate(
	# 		await self.fetch_many(
	# 			self._list_q(
	# 				user_ids,
	# 				product_ids,
	# 				limit,
	# 				offset
	# 			)
	# 		)
	# 	)
	@classmethod
	async def update_reserved_amount_by_product_id(cls, s: AsyncSession, product_id : int):
		await s.execute(
			update(cls.table)
			.values(
				amount = case(
					(cls.table.product_discount_pct == 0,
					        cls.table.product_price * cls.table.quantity
					 ),
					else_=(
							cls.table.product_price - (cls.table.product_price / 100 * cls.table.product_discount_pct)
					) * cls.table.quantity
				)
			)
			.where(and_(
				cls.table.status     == OrderStatus.RESERVED,
				cls.table.product_id == product_id,
			))
		)

	@classmethod
	async def update_reserved_by_product_id(cls, s: AsyncSession, product_id: int, to_update: dict):
		await s.execute(
			update(cls.table)
				.values(**to_update)
				.where(and_(
					cls.table.status     == OrderStatus.RESERVED,
					cls.table.product_id == product_id,
				))
		)

	@classmethod
	async def delete_many_by_product_id(cls, s: AsyncSession, product_id: int):
		await s.execute(
			delete(cls.table)
				.where(cls.table.product_id == product_id)
		)
