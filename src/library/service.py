from typing          import Generic

from .entity         import EntityT
from .repository_abc import RepositoryABC_T


class Service(Generic[EntityT, RepositoryABC_T]):
	def __init__(self, repo: RepositoryABC_T) -> None:
		self.repo = repo

	async def create(self, entity: EntityT) -> EntityT:
		return await self.repo.create(entity)
