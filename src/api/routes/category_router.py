from fastapi             import APIRouter, status, HTTPException

from src.api.schemas     import CategoryCreate, CategoryResponse
from src.domain.entities import Category
from src.domain.services import CategoryService


class CategoryRouter(APIRouter):
	def __init__(self, service: CategoryService, **kwargs):
		super().__init__(**kwargs)
		self.service = service
		self.add_api_route(
			'/create',
			self.create,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED: {
					'model'       : CategoryResponse,
					'description' : 'Category created successfully'
				},
				status.HTTP_409_CONFLICT: {
					'description': 'Category already exists'
				}
			}
		)

	async def create(self, category : CategoryCreate) -> CategoryResponse:
		if await self.service.exists_name(category.name):
			raise HTTPException(
				status.HTTP_409_CONFLICT,
				'Category already exists'
			)
		new_category = await self.service.create(
			Category(**category.model_dump())
		)
		return CategoryResponse(**new_category.model_dump())
