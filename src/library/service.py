from typing                 import Generic, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from .entity                import EntityT, EntityListT
from .repository_abc        import RepositoryABC_T


class Service(Generic[EntityT, EntityListT, RepositoryABC_T]):
	def __init__(self, repo: Type[RepositoryABC_T]):
		self.repo = repo

	async def create(self, s: AsyncSession, entity: EntityT) -> EntityT:
		return await self.repo.create(s, entity)

	async def get_by_id(self, s: AsyncSession, id: int) -> Optional[EntityT]:
		return await self.repo.get_or_none(s, id=id)

	async def get_all(self, s: AsyncSession) -> EntityListT:
		return await self.repo.get_all(s)

	async def exists_id(self, s: AsyncSession, id: int) -> bool:
		return await self.repo.exists(s, id=id)

	async def exists_name(self, s: AsyncSession, name: str) -> bool:
		return await self.repo.exists(s, name=name)
