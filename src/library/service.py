from typing          import Generic

from .entity         import EntityT, EntityListT
from .repository_abc import RepositoryABC_T


class Service(Generic[EntityT, EntityListT, RepositoryABC_T]):
	def __init__(self, repo: RepositoryABC_T):
		self.repo = repo

	async def create(self, entity: EntityT) -> EntityT:
		return await self.repo.create(entity)

	async def get_all(self) -> EntityListT:
		return await self.repo.get_all()
