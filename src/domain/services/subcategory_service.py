from src.domain.entities     import Subcategory, SubcategoryList
from src.domain.repositories import SubcategoryRepository
from src.library             import Service


class SubcategoryService(Service[Subcategory, SubcategoryList, SubcategoryRepository]):
	...
