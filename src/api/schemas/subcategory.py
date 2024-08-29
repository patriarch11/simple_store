from pydantic    import BaseModel, RootModel

from src.library import ResponseSchema


class SubcategoryCreate(BaseModel):
	category_id : int
	name        : str


class SubcategoryResponse(ResponseSchema, SubcategoryCreate):
	...


class SubcategoryListResponse(RootModel[list[SubcategoryResponse]]):
	...
