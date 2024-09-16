from abc                    import ABC, abstractmethod
from typing                 import Any, Generic, TypeVar, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .entity                import EntityT, EntityListT


RepositoryABC_T = TypeVar('RepositoryABC_T', bound='RepositoryABC')


class RepositoryABC(ABC, Generic[EntityT, EntityListT]):
	@classmethod
	@abstractmethod
	async def create(cls, s: AsyncSession, entity: EntityT) -> EntityT:
		...

	@classmethod
	@abstractmethod
	async def get_or_none(cls, s: AsyncSession, **filters: Any) -> Optional[EntityT]:
		...

	@classmethod
	@abstractmethod
	async def get_all(cls, s: AsyncSession) -> EntityListT:
		...

	@classmethod
	@abstractmethod
	async def filter(cls, s: AsyncSession, **filters: Any) -> EntityListT:
		...

	@classmethod
	@abstractmethod
	async def exists(cls, s: AsyncSession, **filters: Any) -> bool:
		...

	@classmethod
	@abstractmethod
	async def update(cls, s: AsyncSession, id: int, to_update: dict) -> EntityT:
		...

	@classmethod
	@abstractmethod
	async def delete(cls, s: AsyncSession, id: int):
		...
