from pydantic    import BaseModel, RootModel

from src.library import ResponseSchema


class ProductCreate(BaseModel):
	category_id    : int
	subcategory_id : int
	name           : str
	discount_pct   : float = 0.0
	price          : float = 0.0
	total_count    : int   = 0


class ProductResponse(ResponseSchema, ProductCreate):
	free_count: int = 0


class ProductListResponse(RootModel[list[ProductResponse]]):
	...
