from typing     import Any, Optional, Union, Type, TypeVar, Generic

from sqlalchemy import (
	Insert,
	Select,
	Update,
	Delete,

	insert,
	select,
	update,
	delete
)
from sqlalchemy.ext.asyncio import AsyncSession

from .entity                import EntityT
from .table                 import TableT


class Repository(Generic[EntityT, TableT]):
	entity : Type[EntityT]
	table  : Type[TableT]

	def __init__(self, session : AsyncSession):
		self.session = session

	async def insert_or_update(self, query: Union[Insert, Update]) -> dict[str, Any]:
		async with self.session() as tx:
			async with tx.begin(): # begin transaction and commit to session after executing
				result = await tx.execute(query)
				row = result.mappings().first()
				return dict(row)

	async def fetch_one(self, query: Select) -> Optional[dict[str, Any]]:
		async with self.session as tx:
			result = await tx.execute(query)
			row = result.mappings().first()
			return dict(row) if row else None

	async def fetch_many(self, query: Select) -> list[dict[str, Any]]:
		async with self.session as tx:
			result = await tx.execute(query)
			rows   = result.mappings().all()
			return [dict(row) for row in rows]

	async def execute(self, query: Union[Insert, Update, Delete]) -> None:
		async with self.session() as tx:
			async with tx.begin():
				await tx.execute(query)

	async def create(self, entity: EntityT) -> EntityT:
		data = await self.insert_or_update(
			insert(self.table)
				.values(**entity.to_db())
				.returning(self.table.__table__.columns)
		)
		return self.entity.model_validate(data)
	
	async def exists(self, **filters: Any) -> bool:
		query = select(self.table).filter_by(**filters)
		async with self.session() as tx:
			result = await tx.execute(query)
			row = result.first()
			return bool(row)

RepositoryT = TypeVar('RepositoryT', bound=Repository)
