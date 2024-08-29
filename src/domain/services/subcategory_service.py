from src.domain.entities     import Subcategory
from src.domain.repositories import SubcategoryRepository
from src.library             import Service


class SubcategoryService(Service[Subcategory, SubcategoryRepository]):
	async def exists_name(self, name: str) -> bool:
		return await self.repo.exists(name=name)
