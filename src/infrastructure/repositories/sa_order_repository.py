from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
	Enum
)

from src.constants                import OrderStatus
from src.domain.entities          import Order, OrderList
from src.domain.repositories      import OrderRepository
from src.infrastructure.database  import Base
from src.library                  import Repository, Table


class OrderTable(Base, Table):
	__tablename__ = 'orders'

	id         = Column(Integer, primary_key=True)
	user_id    = Column(Integer, nullable=False)
	product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
	status     = Column(Enum(OrderStatus), nullable=False)


class SaOrderRepository(
	Repository[Order, OrderList, OrderTable],
	OrderRepository
):
	entity      = Order
	entity_list = OrderList
	table       = OrderTable
