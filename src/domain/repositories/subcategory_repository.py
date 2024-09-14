from abc                 import ABC

from src.domain.entities import Subcategory, SubcategoryList
from src.library         import RepositoryABC


class SubcategoryRepository(RepositoryABC[Subcategory, SubcategoryList], ABC):
	...
