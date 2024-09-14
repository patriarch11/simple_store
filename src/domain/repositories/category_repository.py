from abc                 import ABC

from src.domain.entities import Category, CategoryList
from src.library         import RepositoryABC


class CategoryRepository(RepositoryABC[Category, CategoryList], ABC):
	...
