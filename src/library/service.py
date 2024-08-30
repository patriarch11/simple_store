from typing          import Generic, Optional

from .entity         import EntityT, EntityListT
from .repository_abc import RepositoryABC_T


class Service(Generic[EntityT, EntityListT, RepositoryABC_T]):
	def __init__(self, repo: RepositoryABC_T):
		self.repo = repo

	async def create(self, entity: EntityT) -> EntityT:
		return await self.repo.create(entity)

	async def get_by_id(self, id: int) -> Optional[EntityT]:
		return await self.repo.get_or_none(id=id)

	async def get_all(self) -> EntityListT:
		return await self.repo.get_all()

	async def exists_id(self, id: int) -> bool:
		return await self.repo.exists(id=id)

	async def exists_name(self, name: str) -> bool:
		return await self.repo.exists(name=name)
