from src.library import BaseModel


class Product(BaseModel):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : int
	price          : int
	total_count    : int
	free_count     : int

