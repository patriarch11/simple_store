from fastapi                     import APIRouter, status, HTTPException

from src.api.schemas.subcategory import (
	SubcategoryCreate,
	SubcategoryResponse,
	SubcategoryListResponse
)
from src.domain.entities         import Subcategory
from src.domain.services         import CategoryService, SubcategoryService


class SubcategoryRouter(APIRouter):
	def __init__(self,
		service          : SubcategoryService,
		category_service : CategoryService,
		**kwargs
	):
		super().__init__(**kwargs)
		self.service          = service
		self.category_service = category_service
		self.add_api_route(
			'/create',
			self.create,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED: {
					'model'       : SubcategoryResponse,
					'description' : 'Category created'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Category does not exists'
				},
				status.HTTP_409_CONFLICT: {
					'description': 'Subcategory already exists'
				}
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
			raise HTTPException(
				status.HTTP_404_NOT_FOUND,
				'Category not found'
			)
		if await self.service.exists_name(subcategory.name):
			raise HTTPException(
				status.HTTP_409_CONFLICT,
				'Subcategory already exists'
			)
		new_subcategory = await self.service.create(
			Subcategory(**subcategory.model_dump())
		)

		return SubcategoryResponse(**new_subcategory.model_dump())

	async def get_all(self) -> SubcategoryListResponse:
		subcategories = await self.service.get_all()
		return SubcategoryListResponse.model_validate(
			subcategories.model_dump()
		)
