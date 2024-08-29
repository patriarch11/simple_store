from abc                 import ABC, abstractmethod
from typing              import Any, Optional

from src.domain.entities import Category


class CategoryRepository(ABC):
	@abstractmethod
	async def create(self, category: Category) -> Category:
		...
	
	@abstractmethod
	async def exists(self, **filters: Any) -> bool:
		...
		