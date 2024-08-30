from abc     import ABC, abstractmethod
from typing  import Any, Generic, TypeVar, Optional

from .entity import EntityT, EntityListT


class RepositoryABC(ABC, Generic[EntityT, EntityListT]):
	@abstractmethod
	async def create(self, entity: EntityT) -> EntityT:
		...

	@abstractmethod
	async def get_or_none(self, **filters: Any) -> Optional[EntityT]:
		...

	@abstractmethod
	async def get_all(self) -> EntityListT:
		...

	@abstractmethod
	async def filter(self, **filters: Any) -> EntityListT:
		...

	@abstractmethod
	async def exists(self, **filters: Any) -> bool:
		...

	@abstractmethod
	async def update(self, id: int, to_update: dict) -> EntityT:
		...

	@abstractmethod
	async def delete(self, id: int):
		...

RepositoryABC_T = TypeVar('RepositoryABC_T', bound=RepositoryABC)
