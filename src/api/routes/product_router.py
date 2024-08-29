from fastapi             import APIRouter, status, HTTPException

from src.domain.services import ProductService


class ProductRouter(APIRouter):
	def __init__(self, service: ProductService, **kwargs):
		super().__init__(**kwargs)
		self.service = service
