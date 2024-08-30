from typing     import Any, Optional, Union, Type, TypeVar, Generic

from sqlalchemy import (
	Insert,
	Select,
	Update,
	Delete,

	insert,
	select,
	update,
	delete,

)
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.ext.asyncio   import AsyncSession

from .entity                  import EntityT, EntityListT
from .table                   import TableT


class Repository(Generic[EntityT, EntityListT, TableT]):
	entity      : Type[EntityT]
	entity_list : Type[EntityListT]
	table       : Type[TableT]

	def __init__(self, session : AsyncSession):
		self.session = session

	async def insert_or_update(self, query: Union[Insert, Update]) -> dict[str, Any]:
		async with self.session() as tx:
			async with tx.begin(): # begin transaction and commit to session after executing
				result: CursorResult = await tx.execute(query)
				row = result.mappings().first()
				return dict(row)

	async def fetch_one(self, query: Select) -> Optional[dict[str, Any]]:
		async with self.session() as tx:
			result: CursorResult = await tx.execute(query)
			row = result.mappings().fetchone()
			return dict(row) if row else None

	async def fetch_many(self, query: Select) -> list[dict[str, Any]]:
		async with self.session() as tx:
			result: CursorResult = await tx.execute(query)
			rows = result.mappings().fetchall()
			return [dict(row) for row in rows]

	async def execute(self, query: Union[Insert, Update, Delete]) -> None:
		async with self.session() as tx:
			async with tx.begin():
				await tx.execute(query)

	@property
	def select_q(self) -> Select:
		return select(self.table.__table__.columns)

	def filter_q(self, **filters: Any) -> Select:
		return self.select_q.filter_by(**filters)

	def paginate_q(self,
		q      : Select,
		limit  : Optional[int],
		offset : Optional[int]
	) -> Select:
		if offset is not None:
			q = q.offset(offset)
		if limit is not None:
			q = q.limit(limit)
		return q

	async def create(self, entity: EntityT) -> EntityT:
		data = await self.insert_or_update(
			insert(self.table)
				.values(**entity.to_db())
				.returning(self.table.__table__.columns)
		)
		return self.entity.model_validate(data)

	async def get_or_none(self, **filters: Any) -> Optional[EntityT]:
		data = await self.fetch_one(
			self.filter_q(**filters).limit(1)
		)
		if data:
			return self.entity.model_validate(data)

	async def get_all(self,
		limit  : Optional[int] = None,
		offset : Optional[int] = None
	) -> EntityListT:
		return self.entity_list.model_validate(
			await self.fetch_many(
				self.paginate_q(self.select_q, limit, offset)
			)
		)

	async def filter(self,
		limit  : Optional[int] = None,
		offset : Optional[int] = None,
		**filters: Any
	) -> EntityListT:
		return self.entity_list.model_validate(
			await self.fetch_many(
				self.paginate_q(
					self.filter_q(**filters),
					limit,
					offset
				)
			)
		)

	async def exists(self, **filters: Any) -> bool:
		query = select(self.table).filter_by(**filters)
		async with self.session() as tx:
			result: ScalarResult = await tx.scalars(query)
			row = result.first()
			return bool(row)

	async def update(self, id: int, to_update: dict) -> EntityT:
		data = await self.insert_or_update(
			update(self.table)
				.values(**to_update)
				.where(self.table.id == id)
				.returning(self.table.__table__.columns)
		)
		return self.entity.model_validate(data)

	async def delete(self, id: int):
		await self.execute(
			delete(self.table)
				.where(self.table.id == id)
		)

RepositoryT = TypeVar('RepositoryT', bound=Repository)
