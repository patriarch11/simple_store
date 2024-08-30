from fastapi                     import APIRouter, HTTPException, status

from src.api.schemas.subcategory import (
	SubcategoryCreate,
	SubcategoryResponse,
	SubcategoryListResponse
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
					'model'       : SubcategoryResponse,
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
					'model'       : SubcategoryListResponse,
					'description' : 'List of subcategories'
				}
			}
		)

	async def create(self, subcategory: SubcategoryCreate) -> SubcategoryResponse:
		if not await self.category_service.exists_id(subcategory.category_id):
			raise HTTPException(status.HTTP_404_NOT_FOUND,'Category not found')

		if await self.service.exists_name(subcategory.name):
			raise HTTPException(status.HTTP_409_CONFLICT, 'Subcategory already exists')

		new_subcategory = await self.service.create(Subcategory(**subcategory.model_dump()))
		return SubcategoryResponse(**new_subcategory.model_dump())

	async def get_all(self) -> SubcategoryListResponse:
		subcategories = await self.service.get_all()
		return SubcategoryListResponse.model_validate(subcategories.model_dump())

router = SubcategoryRouter()
