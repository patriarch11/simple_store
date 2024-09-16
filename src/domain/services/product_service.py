from typing                  import Optional, Type

from fastapi                 import HTTPException, status
from sqlalchemy.ext.asyncio  import AsyncSession

from src.domain.entities     import Product, ProductList
from src.domain.repositories import (
	ProductRepository,
	OrderRepository,
	CategoryRepository,
	SubcategoryRepository
)
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	def __init__(self,
	    repo             : Type[ProductRepository],
	    order_repo       : Type[OrderRepository],
	    category_repo    : Type[CategoryRepository],
	    subcategory_repo : Type[SubcategoryRepository]
	):
		super().__init__(repo)
		self.order_repo       = order_repo
		self.category_repo    = category_repo
		self.subcategory_repo = subcategory_repo

	async def create(self, s: AsyncSession, product: Product) -> Product:
		category = await self.category_repo.get_or_none(s, id=product.category_id)
		if not category:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Category does not exist')
		subcategory = await self.subcategory_repo.get_or_none(s, id=product.subcategory_id)
		if not subcategory:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Subcategory does not exist')

		if subcategory.category_id != category.id:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Subcategory and category do not match')

		if await self.exists_name(s, product.name):
			raise HTTPException(status.HTTP_409_CONFLICT, 'Product name already exists')
		return await super().create(s, product)

	async def get_list_of_available(self,
	    s               : AsyncSession,
        category_ids    : list[int],
        subcategory_ids : list[int],
        limit           : Optional[int],
        offset          : Optional[int]
	) -> ProductList:
		return await self.repo.get_list_of_available(
			s, category_ids, subcategory_ids, limit, offset
		)

	async def get_by_id(self, s: AsyncSession, product_id: int) -> Product:
		product = await super().get_by_id(s, product_id)
		if not product:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Product not found')
		return product

	async def update_price(self, s: AsyncSession, product_id: int, price: float) -> Product:
		if price < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Price cannot be negative')
		product = await self.repo.update(s, product_id, {
			'price': price
		})
		await self.order_repo.update_reserved_by_product_id(s, product_id, {'product_price': price})
		await self.order_repo.update_reserved_amount_by_product_id(s, product_id)
		return product

	async def update_discount(self, s: AsyncSession, product_id: int, discount: float) -> Product:
		if discount < 0 or discount > 100:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Discount must be between 0 and 100')
		product = await self.repo.update(s, product_id, {
			'discount_pct': discount
		})
		await self.order_repo.update_reserved_by_product_id(s, product_id, {'product_discount_pct': discount})
		await self.order_repo.update_reserved_amount_by_product_id(s, product_id)
		return product

	async def update_reserved_count(self, s: AsyncSession, product: Product, difference: int) -> Product:
		reserved_count = product.reserved_count + difference
		if reserved_count < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Product reserved count cannot be negative')

		if reserved_count > product.free_count:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Insufficient free quantity of the product')

		return await self.repo.update(s, product.id, {
			'reserved_count': reserved_count
		})

	async def update_total_count(self, s: AsyncSession, product: Product, difference: int, count: int = None) -> Product:
		if count is not None:
			difference = count - product.total_count

		total_count = product.total_count + difference
		if total_count < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Product total count cannot be negative')

		if total_count < product.reserved_count:
			# here can be additional logic by with order cancellation
			raise HTTPException(
				status.HTTP_400_BAD_REQUEST,
			    'Product total count cannot be less than reserved count'
			)

		return await self.repo.update(s, product.id, {
			'total_count': total_count
		})

	async def delete(self, s: AsyncSession, product_id: int):
		if not await self.exists_id(s, product_id):
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Product not found')
		await self.order_repo.delete_many_by_product_id(s, product_id)
		await self.repo.delete(s, product_id)
