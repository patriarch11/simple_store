from fastapi                     import APIRouter, HTTPException, status

from src.api.schemas.subcategory import (
	SubcategoryCreateSchema,
	SubcategorySchema,
	SubcategoryListSchema
)
from src.dependencies            import get_category_service, get_subcategory_service
from src.domain.entities         import Subcategory


class SubcategoryRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service          = get_subcategory_service()
		self.category_service = get_category_service()
		self.add_api_route(
			'/create',
			self.create,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED: {
					'model'       : SubcategorySchema,
					'description' : 'Category created'
				},
				status.HTTP_404_NOT_FOUND : {'description': 'Category does not exists'},
				status.HTTP_409_CONFLICT  : {'description': 'Subcategory already exists'}
			}
		)
		self.add_api_route(
			'/list',
			self.get_all,
			methods   = ['GET'],
			responses = {
				status.HTTP_200_OK : {
					'model'       : SubcategoryListSchema,
					'description' : 'List of subcategories'
				}
			}
		)

	async def create(self, subcategory: SubcategoryCreateSchema) -> SubcategorySchema:
		return SubcategorySchema.from_entity(
			await self.service.create(Subcategory(**subcategory.model_dump()))
		)

	async def get_all(self) -> SubcategoryListSchema:
		subcategories = await self.service.get_all()
		return SubcategoryListSchema.model_validate(subcategories.model_dump())

router = SubcategoryRouter()
