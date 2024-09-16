from fastapi                import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas        import (
	CategoryPaginationFilter,
	ProductCreateSchema,
	ProductCountUpdateSchema,
	ProductPriceUpdateSchema,
	ProductDiscountUpdateSchema,
	ProductSchema,
	ProductListSchema
)
from src.dependencies       import get_product_service, get_session
from src.domain.entities    import Product


class ProductRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service  = get_product_service()
		self.add_api_route(
			'/create',
			self.create,
			methods      = ['POST'],
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

	async def create(self, product: ProductCreateSchema, s: AsyncSession = Depends(get_session)) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.create(
				s,
				Product.model_validate(product.model_dump())
			)
		)

	async def get_list(self,
		f: CategoryPaginationFilter = Depends(CategoryPaginationFilter.as_query),
		s: AsyncSession             = Depends(get_session)
	) -> ProductListSchema:
		product_list = await self.service.get_list_of_available(s, **f.model_dump())
		return ProductListSchema.model_validate(product_list.model_dump())

	async def update_count(self,
	    count_schema : ProductCountUpdateSchema,
	    s            : AsyncSession = Depends(get_session)
	) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_total_count(
				s,
				await self.service.get_by_id(s, count_schema.id),
				None,
				count_schema.count
			)
		)

	async def update_price(self,
	    price_schema : ProductPriceUpdateSchema,
	    s            : AsyncSession = Depends(get_session)
	) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_price(s, price_schema.id, price_schema.price)
		)

	async def update_discount(self,
	    discount_schema : ProductDiscountUpdateSchema,
	    s               : AsyncSession = Depends(get_session)
	) -> ProductSchema:
		return ProductSchema.from_entity(
			await self.service.update_discount(s, discount_schema.id, discount_schema.discount_pct)
		)

	async def delete_product(self,
	    product_id : int          = Query(...),
		s          : AsyncSession = Depends(get_session)
	):
		await self.service.delete(s, product_id)


router = ProductRouter()
