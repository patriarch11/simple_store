from typing                  import Optional

from fastapi                 import  HTTPException, status

from src.domain.entities     import Product, ProductList
from src.domain.repositories import ProductRepository, OrderRepository
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	async def update_reserved_count(self, product: Product, difference: int):
		reserved_count = product.reserved_count + difference
		if reserved_count < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Product reserved count cannot be negative')

		if reserved_count > product.free_count:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Insufficient free quantity of the product')

		await self.repo.update(product.id, {
			'reserved_count': reserved_count
		})

	async def update_total_count(self, product: Product, difference: int):
		total_count = product.total_count + difference
		if total_count < 0:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Product total count cannot be negative')

		if total_count < product.free_count:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Insufficient free quantity of the product')

		if total_count < product.reserved_count:
			# here can be additional logic by with order cancellation
			raise HTTPException(
				status.HTTP_400_BAD_REQUEST,
			    'Product total count cannot be less than reserved count'
			)

		await self.repo.update(product.id, {
			'total_count': total_count
		})

# async def get_list(self,
	# 	category_ids    : list[int],
	# 	subcategory_ids : list[int],
	# 	limit           : Optional[int],
	# 	offset          : Optional[int]
	# ) -> ProductList:
	# 	return await self.repo.get_list(category_ids, subcategory_ids, limit, offset)
	#
	#
	# async def get_list_with_free_count(self,
	# 	category_ids    : list[int],
	# 	subcategory_ids : list[int],
	# 	limit           : Optional[int],
	# 	offset          : Optional[int]
	# ) -> ProductList:
	# 	return await self.repo.get_list_with_free_count(category_ids, subcategory_ids, limit, offset)

	# async def increase_free_count(self, product: Product, increment: int):
	# 	free_count = product.reserved_count + increment
	# 	await self.repo.update(product.id, {
	# 		'free_count': free_count
	# 	})
	#
	# async def decrease_free_count(self, product: Product, decrement: int):
	# 	free_count = product.reserved_count - decrement
	# 	await self.repo.update(product.id, {
	# 		'free_count': free_count
	# 	})
	#
	# async def decrease_total_count(self, product: Product, decrement: int):
	# 	total_count = product.total_count - decrement
	# 	await self.repo.update(product.id, {
	# 		'total_count': total_count
	# 	})
