from abc     import ABC, abstractmethod
from typing  import Any, Generic, TypeVar

from .entity import EntityT, EntityListT


class RepositoryABC(ABC, Generic[EntityT, EntityListT]):
	@abstractmethod
	async def create(self, entity: EntityT) -> EntityT:
		...

	@abstractmethod
	async def get_all(self) -> EntityListT:
		...

	@abstractmethod
	async def exists(self, **filters: Any) -> bool:
		...

RepositoryABC_T = TypeVar('RepositoryABC_T', bound=RepositoryABC)
