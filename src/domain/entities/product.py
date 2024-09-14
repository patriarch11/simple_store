from pydantic    import model_validator

from src.library import Entity, EntityList


class Product(Entity):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : float = 0.0
	price          : float = 0.0
	total_count    : int   = 0
	reserved_count : int   = 0

	@model_validator(mode='after')
	def validate_reserved_count(self):
		if self.reserved_count > self.total_count:
			raise ValueError('Reserved count can not be greater than total count')
		return self

	@property
	def free_count(self) -> int:
		return self.total_count - self.reserved_count

class ProductList(EntityList[Product]):
	...
