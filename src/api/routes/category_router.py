from fastapi                import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas        import (
	CategoryCreateSchema,
	CategorySchema,
	CategoryListSchema
)
from src.dependencies       import get_category_service, get_session
from src.domain.entities    import Category


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

	async def create(self,
	    category : CategoryCreateSchema,
		s        : AsyncSession = Depends(get_session)
	) -> CategorySchema:
		return CategorySchema.from_entity(
			await self.service.create(s, Category(**category.model_dump()))
		)

	async def get_all(self, s: AsyncSession = Depends(get_session)) -> CategoryListSchema:
		categories = await self.service.get_all(s)
		return CategoryListSchema.model_validate(categories.model_dump())

router = CategoryRouter()
