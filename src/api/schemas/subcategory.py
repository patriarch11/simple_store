from pydantic    import BaseModel, RootModel

from src.library import Schema


class SubcategoryCreateSchema(BaseModel):
	category_id : int
	name        : str


class SubcategorySchema(Schema, SubcategoryCreateSchema):
	...


class SubcategoryListSchema(RootModel[list[SubcategorySchema]]):
	...
