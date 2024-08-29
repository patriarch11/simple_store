from src.domain.entities     import Subcategory, SubcategoryList
from src.domain.repositories import SubcategoryRepository
from src.library             import Service


class SubcategoryService(Service[Subcategory, SubcategoryList, SubcategoryRepository]):
	async def exists_name(self, name: str) -> bool:
		return await self.repo.exists(name=name)
