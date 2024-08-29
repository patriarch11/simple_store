from src.library import Entity, EntityList


class Subcategory(Entity):
	category_id : int
	name        : str


class SubcategoryList(EntityList[Subcategory]):
	...
