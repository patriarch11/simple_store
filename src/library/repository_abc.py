from abc     import ABC, abstractmethod
from typing  import Any, Generic, TypeVar

from .entity import EntityT


class RepositoryABC(ABC, Generic[EntityT]):
	@abstractmethod
	async def create(self, entity: EntityT) -> EntityT:
		...

	@abstractmethod
	async def exists(self, **filters: Any) -> bool:
		...

RepositoryABC_T = TypeVar('RepositoryABC_T', bound=RepositoryABC)
