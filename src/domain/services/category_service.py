from src.domain.entities     import Category
from src.domain.repositories import CategoryRepository


class CategoryService:
	def __init__(self, repo: CategoryRepository):
		self.repo = repo

	async def create(self, category: Category) -> Category:
		return await self.repo.create(category)

	async def exists_name(self, name: str) -> bool:
		return await self.repo.exists(name=name)
	
