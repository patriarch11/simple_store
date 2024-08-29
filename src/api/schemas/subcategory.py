from pydantic    import BaseModel

from src.library import ResponseSchema


class SubcategoryCreate(BaseModel):
	category_id : int
	name        : str


class SubcategoryResponse(ResponseSchema, SubcategoryCreate):
	...
