from fastapi              import APIRouter, Depends, HTTPException, Query, status

from src.api.schemas      import (
	CategoryPaginationFilter,
	ProductCreateSchema,
	ProductCountUpdateSchema,
	ProductPriceUpdateSchema,
	ProductDiscountUpdateSchema,
	ProductSchema,
	ProductListSchema
)
from src.api.validators   import CategoryValidator
from src.dependencies     import get_product_service
from src.domain.entities  import Product


class ProductRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service  = get_product_service()
		self.add_api_route(
			'/create',
			self.create,
			methods      = ['POST'],
			dependencies = [Depends(CategoryValidator())],
			responses    = {
				status.HTTP_201_CREATED: {
					'model'       : ProductSchema,
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
				status.HTTP_200_OK: {'model': ProductListSchema},
			}
		)
		self.add_api_route(
			'/update/count',
			self.update_count,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK: {
					'model'       : ProductSchema,
					'description' : 'Product count updated'
				},
				status.HTTP_400_BAD_REQUEST : {'description': 'Invalid count'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)
		self.add_api_route(
			'/update/price',
			self.update_price,
			methods      = ['PATCH'],
			responses = {
				status.HTTP_200_OK: {
					'model'       : ProductSchema,
					'description' : 'Product price updated'
				},
				status.HTTP_400_BAD_REQUEST : {'description': 'Price cannot be negative'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)
		self.add_api_route(
			'/update/discount',
			self.update_discount,
			methods      = ['PATCH'],
			responses    = {
				status.HTTP_200_OK: {
					'model'       : ProductSchema,
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
			responses    = {
				status.HTTP_200_OK          : {'description': 'Product deleted'},
				status.HTTP_404_NOT_FOUND   : {'description': 'Product not found'},
			}
		)

	async def create(self, product: ProductCreateSchema) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.create(
				Product.model_validate(product.model_dump())
			)
		)

	async def get_list(self,
		f: CategoryPaginationFilter = Depends(CategoryPaginationFilter.as_query)
	) -> ProductListSchema:
		product_list = await self.service.get_list_of_available(**f.model_dump())
		return ProductListSchema.model_validate(product_list.model_dump())

	async def update_count(self, count_schema: ProductCountUpdateSchema) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_total_count(
				await self.service.get_by_id(count_schema.id),
				None,
				count_schema.count
			)
		)

	async def update_price(self, price_schema: ProductPriceUpdateSchema) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_price(price_schema.id, price_schema.price)
		)

	async def update_discount(self, discount_schema: ProductDiscountUpdateSchema) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_discount(discount_schema.id, discount_schema.discount_pct)
		)

	async def delete_product(self, product_id: int = Query(...)):
		await self.service.delete(product_id)


router = ProductRouter()
