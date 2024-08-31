from fastapi              import APIRouter, Depends, HTTPException, Query, status

from src.api.schemas      import (
	CategoryPaginationFilter,
	OrderResponse,
	ProductCreate,
	ProductCountUpdate,
	ProductPriceUpdate,
	ProductDiscountUpdate,
	ProductReserve,
	ProductResponse,
	ProductListResponse
)
from src.api.dependencies import validate_category, get_reserved_order, get_product
from src.dependencies     import get_product_service, get_product_use_case
from src.domain.entities  import Order, Product


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
		self.add_api_route(
			'/reserve',
			self.reserve,
			methods   = ['POST'],
			responses = {
				status.HTTP_201_CREATED:  {
					'model'       : OrderResponse,
					'description' : 'Product reserved, order created'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Invalid quantity'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Prdocut not found'
				}
			}
		)
		self.add_api_route(
			'/cancel_reservation',
			self.cancel_reservation,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK:  {
					'model'       : OrderResponse,
					'description' : 'Product reservation canceled'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Order status must be "RESERVED"'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Order not found'
				}
			}
		)
		self.add_api_route(
			'/sell',
			self.sell,
			methods   = ['PATCH'],
			responses = {
				status.HTTP_200_OK:  {
					'model'       : OrderResponse,
					'description' : 'Product selled'
				},
				status.HTTP_400_BAD_REQUEST : {
					'description': 'Order status must be "RESERVED"'
				},
				status.HTTP_404_NOT_FOUND: {
					'description': 'Order not found'
				}
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
		product_list = await self.service.get_list_with_free_count(**filter.model_dump())
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


	async def reserve(self,
		reservation : ProductReserve,
		product     : Product = Depends(get_product)
	) -> OrderResponse:
		if reservation.quantity > product.free_count:
			raise HTTPException(
				status.HTTP_400_BAD_REQUEST,
				'Quantity must be less or equal to free product count'
			)
		if reservation.quantity <= 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Quantity can\'t be less or equal to 0')
		order = await self.use_case.reserve(product, reservation.user_id, reservation.quantity)
		return OrderResponse.model_validate(order.model_dump())

	async def cancel_reservation(self, order: Order = Depends(get_reserved_order)) -> OrderResponse:
		order = await self.use_case.cancel_reservation(order)
		return OrderResponse.model_validate(order.model_dump())

	async def sell(self, order: Order = Depends(get_reserved_order)) -> OrderResponse:
		order = await self.use_case.sell(order)
		return OrderResponse.model_validate(order.model_dump())

router = ProductRouter()
