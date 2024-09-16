from typing                  import Type

from fastapi                 import HTTPException, status

from sqlalchemy.ext.asyncio  import AsyncSession

from src.domain.entities     import Subcategory, SubcategoryList
from src.domain.repositories import CategoryRepository, SubcategoryRepository
from src.library             import Service


class SubcategoryService(Service[Subcategory, SubcategoryList, SubcategoryRepository]):
	def __init__(self, repo: Type[SubcategoryRepository], category_repo: Type[CategoryRepository]):
		super().__init__(repo)
		self.category_repo = category_repo

	async def create(self, s: AsyncSession, subcategory: Subcategory) -> Subcategory:
		if not await self.category_repo.exists(s, id=subcategory.category_id):
			raise HTTPException(status.HTTP_404_NOT_FOUND,'Category not found')
		if await self.exists_name(s, subcategory.name):
			raise HTTPException(status.HTTP_409_CONFLICT, 'Subcategory already exists')
		return await super().create(s, subcategory)
