from fastapi              import APIRouter, Depends, HTTPException, Query, status

from src.api.schemas      import (
	CategoryPaginationFilter,
	ProductCreate,
	ProductCountUpdate,
	ProductPriceUpdate,
	ProductDiscountUpdate,
	ProductResponse,
	ProductListResponse
)
from src.api.dependencies import validate_category, get_product
from src.dependencies     import get_product_service, get_product_use_case
from src.domain.entities  import Product


class ProductRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service  = get_product_service()
		self.use_case = get_product_use_case()
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
				status.HTTP_400_BAD_REQUEST : {'description': 'Subcategory does not match for category'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Category or subcategory does not exists'},
				status.HTTP_409_CONFLICT    : {'description': 'Product already exists'},
			},
		)
		self.add_api_route(
			'/list',
			self.get_list,
			methods      = ['GET'],
			responses    = {
				status.HTTP_200_OK: {'model': ProductListResponse},
			}
		)
		self.add_api_route(
			'/update/count',
			self.update_count,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK: {
					'model'       : ProductResponse,
					'description' : 'Product count updated'
				},
				status.HTTP_400_BAD_REQUEST : {'description': 'Count can\'t be less than 0'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)
		self.add_api_route(
			'/update/price',
			self.update_price,
			methods      = ['PATCH'],
			dependencies = [Depends(get_product)],
			responses = {
				status.HTTP_200_OK: {
					'model'       : ProductResponse,
					'description' : 'Product price updated'
				},
				status.HTTP_400_BAD_REQUEST : {'description': 'Price can\'t be less than 0'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)
		self.add_api_route(
			'/update/discount',
			self.update_discount,
			methods      = ['PATCH'],
			dependencies = [Depends(get_product)],
			responses    = {
				status.HTTP_200_OK: {
					'model'       : ProductResponse,
					'description' : 'Product discount updated'
				},
				status.HTTP_400_BAD_REQUEST : {'description': 'Discount must be between 0 and 100'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)
		self.add_api_route(
			'/delete',
			self.delete_product,
			methods      = ['DELETE'],
			dependencies = [Depends(get_product)],
			responses    = {
				status.HTTP_200_OK          : {'description': 'Product deleted'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)


	async def create(self, product: ProductCreate) -> ProductResponse:
		if await self.service.exists_name(product.name):
			raise HTTPException(status.HTTP_409_CONFLICT,'Product already exists')

		new_product = await self.service.create(Product(**product.model_dump()))
		return ProductResponse.model_validate(new_product.model_dump())

	async def get_list(self,
		filter: CategoryPaginationFilter = Depends(CategoryPaginationFilter.as_query)
	) -> ProductListResponse:
		product_list = await self.service.get_list(**filter.model_dump())
		return ProductListResponse.model_validate(product_list.model_dump())

	async def update_count(self,
		request: ProductCountUpdate,
		product: Product = Depends(get_product)
	) -> ProductResponse:
		if request.count < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Count can\'t be less than 0')

		updated_product = await self.use_case.update_count(product, request.count)
		return ProductResponse.model_validate(updated_product.model_dump())

	async def update_price(self, request: ProductPriceUpdate) -> ProductResponse:
		if request.price < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Price can\'t be less than 0')

		updated_product = await self.use_case.update_price(
			request.product_id,
			request.price
		)
		return ProductResponse.model_validate(updated_product.model_dump())

	async def update_discount(self, request: ProductDiscountUpdate) -> ProductResponse:
		if request.discount_pct < 0.0 or request.discount_pct > 100.0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Discount must be between 0 and 100')

		updated_product = await self.use_case.update_discount(
			request.product_id,
			request.discount_pct
		)
		return ProductResponse.model_validate(updated_product.model_dump())

	async def delete_product(self, product_id: int = Query(...)):
		await self.use_case.delete(product_id)

router = ProductRouter()
