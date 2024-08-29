from src.library import Entity, EntityList


class Product(Entity):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : int
	price          : int
	total_count    : int
	free_count     : int


class ProductList(EntityList[Product]):
	...
