from fastapi             import APIRouter, status, HTTPException

from src.domain.services import OrderService


class OrderRouter(APIRouter):
	def __init__(self, service: OrderService, **kwargs):
		super().__init__(**kwargs)
		self.service = service
