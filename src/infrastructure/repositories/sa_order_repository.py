from typing import Optional

from sqlalchemy import (
	Column,
	Integer,
	Float,
	ForeignKey,
	Enum,

	select,
	update,
	delete,

	and_,
	case,
)
from sqlalchemy.ext.asyncio       import AsyncSession

from src.constants                import OrderStatus, SalesReportOrder, SortOrder
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

ORDER_TO_COLUMNS = {
	SalesReportOrder.AMOUNT           : OrderTable.amount,
	SalesReportOrder.DATE             : OrderTable.created_at,
	SalesReportOrder.QUANTITY         : OrderTable.quantity,
	SalesReportOrder.PRODUCT_PRICE    : OrderTable.product_price,
	SalesReportOrder.PRODUCT_DISCOUNT : OrderTable.product_discount_pct
}

class SaOrderRepository(
	Repository[Order, OrderList, OrderTable],
	OrderRepository
):
	entity      = Order
	entity_list = OrderList
	table       = OrderTable

	@classmethod
	async def get_list_by_filters(cls,
	    s                  : AsyncSession,
	    status             : OrderStatus,
	    user_ids           : Optional[list[int]],
	    product_ids        : Optional[list[int]],
	    product_price_from : Optional[float],
	    product_price_to   : Optional[float],
	    amount_from        : Optional[float],
	    amount_to          : Optional[float],
	    order_by           : Optional[SalesReportOrder],
	    sort_by            : Optional[SortOrder] = SortOrder.ASCENDING,
	) -> OrderList:
		and_clauses = []
		if status:
			and_clauses.append(cls.table.status == status)
		if user_ids and len(user_ids):
			and_clauses.append(cls.table.user_id.in_(user_ids))
		if product_ids and len(product_ids):
			and_clauses.append(cls.table.product_id.in_(product_ids))
		if product_price_from:
			and_clauses.append(cls.table.product_price >= product_price_from)
		if product_price_to:
			and_clauses.append(cls.table.product_price <= product_price_from)
		if amount_from:
			and_clauses.append(cls.table.amount >= amount_from)
		if amount_to:
			and_clauses.append(cls.table.amount <= amount_to)
		q = select(cls.table)
		if len(and_clauses):
			q = q.where(and_(*and_clauses))
		if order_by:
			column = ORDER_TO_COLUMNS.get(order_by)
			match sort_by:
				case SortOrder.ASCENDING:
					q = q.order_by(column.asc())
				case SortOrder.DESCENDING:
					q = q.order_by(column.desc())
		res  = await s.execute(q)
		rows = res.fetchall()
		return cls.entity_list.model_validate(
			[r[0].__dict__ for r in rows]
		)

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
