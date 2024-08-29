from pydantic    import BaseModel, RootModel

from src.library import ResponseSchema


class CategoryCreate(BaseModel):
	name: str


class CategoryResponse(ResponseSchema, CategoryCreate):
	...


class CategoryListResponse(RootModel[list[CategoryResponse]]):
	...
