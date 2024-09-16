from fastapi                 import HTTPException, status
from sqlalchemy.ext.asyncio  import AsyncSession

from src.domain.entities     import Category, CategoryList
from src.domain.repositories import CategoryRepository
from src.library             import Service


class CategoryService(Service[Category, CategoryList, CategoryRepository]):
	async def create(self, s: AsyncSession, category: Category) -> Category:
		if await self.exists_name(s, category.name):
			raise HTTPException(status.HTTP_409_CONFLICT, 'Category already exists')
		return await super().create(s, category)
