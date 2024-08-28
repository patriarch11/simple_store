from typing     import Any, Optional, Union

from sqlalchemy import (
	Insert,
	Select,
	Update,
	Delete
)
from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def fetch_one(self,
		query: Union[Select, Insert, Update]
	) -> Optional[dict[str, Any]]:
		result = await self.session.execute(query)
		row    = result.fetchone()
		if row:
			return dict(row)
		return None

	async def fetch_many(self,
		query: Union[Select, Insert, Update]
	) -> Optional[list[dict[str, Any]]]:
		result = await self.session.execute(query)
		rows   = result.fetchall()
		if rows:
			return [dict(row) for row in rows]
		return None

	async def fetch_exists(self, query: Select) -> bool:
		result = await self.session.execute(query)
		row    = result.fetchone()
		return row is not None

	async def fetch_count(self, query: Select) -> int:
		result = await self.session.execute(query)
		count  = result.scalar_one_or_none()
		return count if count is not None else 0

	async def execute(self,
		query: Union[Insert, Update, Delete]
	) -> None:
		await self.session.execute(query)
		await self.session.commit()
