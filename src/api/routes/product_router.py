from fastapi              import APIRouter, HTTPException, status

from src.api.schemas      import (
	CategoryFilter,
	ProductCreate,
	ProductResponse,
	ProductListResponse
)
from src.api.dependencies import validate_category
from src.dependencies     import get_product_service
from src.domain.entities  import Product

CATEGORY_ERROR_RESPONSES = {
	status.HTTP_400_BAD_REQUEST : {'description'  : 'Subcategory does not match for category'},
	status.HTTP_404_NOT_FOUND   : {'description'  : 'Category or subcategory does not exists'},
}


class ProductRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service = get_product_service()
		self.add_api_route(
			'/create',
			self.create,
			methods      = ['POST'],
			dependencies = [validate_category],
			responses    = {
				status.HTTP_201_CREATED: {
					'model'       : ProductResponse,
					'description' : 'Product created'
				},
				status.HTTP_409_CONFLICT: {'description': 'Product already exists'},
				**CATEGORY_ERROR_RESPONSES
			},
		)
		self.add_api_route(
			'/list',
			self.get_list,
			methods      = ['GET'],
			dependencies = [validate_category],
			responses    = {
				status.HTTP_200_OK: {'model': ProductListResponse},
				**CATEGORY_ERROR_RESPONSES
			}
		)

	async def create(self, product: ProductCreate) -> ProductResponse:
		if await self.service.exists_name(product.name):
			raise HTTPException(status.HTTP_409_CONFLICT,'Product already exists')

		new_product = await self.service.create(Product(**product.model_dump()))
		return ProductResponse.model_validate(new_product.model_dump())

	async def get_list(self, filters: CategoryFilter) -> ProductListResponse:
		...

	async def update_count(self):
		...

	async def update_price(self):
		...

	async def update_discount(self):
		...

	async def delete_product(self):
		...

router = ProductRouter()
