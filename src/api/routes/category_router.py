from fastapi             import APIRouter, HTTPException, status

from src.api.schemas     import (
	CategoryCreateSchema,
	CategorySchema,
	CategoryListSchema
)
from src.dependencies    import get_category_service
from src.domain.entities import Category


class CategoryRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service = get_category_service()
		self.add_api_route(
			'/create',
			self.create,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED: {
					'model'       : CategorySchema,
					'description' : 'Category created successfully'
				},
				status.HTTP_409_CONFLICT: {'description': 'Category already exists'}
			}
		)
		self.add_api_route(
			'/list',
			self.get_all,
			methods   = ['GET'],
			responses = {
				status.HTTP_200_OK : {
					'model'       : CategoryListSchema,
					'description' : 'List of categories'
				}
			}
		)

	async def create(self, category : CategoryCreateSchema) -> CategorySchema:
		if await self.service.exists_name(category.name):
			raise HTTPException(status.HTTP_409_CONFLICT, 'Category already exists')

		new_category = await self.service.create(Category(**category.model_dump()))
		return CategorySchema(**new_category.model_dump())

	async def get_all(self) -> CategoryListSchema:
		categories = await self.service.get_all()
		return CategoryListSchema.model_validate(categories.model_dump())

router = CategoryRouter()
