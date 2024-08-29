from src.domain.entities     import Category
from src.domain.repositories import CategoryRepository
from src.library             import Service


class CategoryService(Service[Category, CategoryRepository]):
	async def exists_id(self, id: int) -> bool:
		return await self.repo.exists(id=id)

	async def exists_name(self, name: str) -> bool:
		return await self.repo.exists(name=name)
