from pydantic    import BaseModel, RootModel

from src.library import Schema


class CategoryCreateSchema(BaseModel):
	name: str


class CategorySchema(Schema, CategoryCreateSchema):
	...


class CategoryListSchema(RootModel[list[CategorySchema]]):
	...
