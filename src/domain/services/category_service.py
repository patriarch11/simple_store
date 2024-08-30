from src.domain.entities     import Category, CategoryList
from src.domain.repositories import CategoryRepository
from src.library             import Service


class CategoryService(Service[Category, CategoryList, CategoryRepository]):
	...
