from pydantic    import model_validator

from src.library import Entity, EntityList


class Product(Entity):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : float = 0.0
	price          : float = 0.0
	total_count    : int   = 0
	free_count     : int   = 0

	@model_validator(mode='after')
	def validate_free_count(self):
		if self.free_count > self.total_count:
			raise ValueError('Free count can not be greater than total count')
		return self

class ProductList(EntityList[Product]):
	...
