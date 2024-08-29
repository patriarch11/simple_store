from pydantic    import BaseModel

from src.library import ResponseSchema


class CategoryCreate(BaseModel):
	name: str


class CategoryResponse(ResponseSchema, CategoryCreate):
	...
