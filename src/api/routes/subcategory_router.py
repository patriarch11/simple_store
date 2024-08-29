from fastapi             import APIRouter, status, HTTPException

from src.domain.services import SubcategoryService


class SubcategoryRouter(APIRouter):
	def __init__(self, service: SubcategoryService, **kwargs):
		super().__init__(**kwargs)
		self.service = service
