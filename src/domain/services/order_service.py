from src.domain.entities     import Order
from src.domain.repositories import OrderRepository
from src.library             import Service


class OrderService(Service[Order, OrderRepository]):
	...
