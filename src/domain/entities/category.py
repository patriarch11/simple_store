from src.library import Entity, EntityList


class Category(Entity):
	name : str


class CategoryList(EntityList[Category]):
	...
