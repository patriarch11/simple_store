from pydantic    import BaseModel, RootModel

from src.library import Schema


class ProductCreateSchema(BaseModel):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : float = 0.0
	price          : float = 0.0
	reserved_count : int   = 0


class ProductCountUpdateSchema(BaseModel):
	product_id : int
	count      : int


class ProductPriceUpdateSchema(BaseModel):
	product_id : int
	price      : float


class ProductDiscountUpdateSchema(BaseModel):
	product_id   : int
	discount_pct : float


class ProductSchema(Schema, ProductCreateSchema):
	reserved_count: int = 0


class ProductListSchema(RootModel[list[ProductSchema]]):
	...
