from src.domain.entities     import Order, OrderList
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[Order, OrderList, OrderRepository]):
	...
