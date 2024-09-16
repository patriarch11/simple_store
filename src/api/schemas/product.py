from pydantic    import BaseModel, RootModel

from src.library import Schema


class ProductCreateSchema(BaseModel):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : float = 0.0
	price          : float = 0.0
	total_count     : int   = 0


class ProductCountUpdateSchema(BaseModel):
	id    : int
	count : int


class ProductPriceUpdateSchema(BaseModel):
	id    : int
	price : float


class ProductDiscountUpdateSchema(BaseModel):
	id           : int
	discount_pct : float


class ProductSchema(Schema, ProductCreateSchema):
	...


class ProductListSchema(RootModel[list[ProductSchema]]):
	...
