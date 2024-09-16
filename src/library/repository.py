from typing    import (
	Optional,
	Union,
	Type,
	TypeVar,
	Generic,
	Any
)

from sqlalchemy import (
	Insert,
	Select,
	Update,

	insert,
	select,
	update,
	delete,

)
from sqlalchemy.ext.asyncio   import AsyncSession


from .entity                  import EntityT, EntityListT
from .table                   import TableT


class Repository(Generic[EntityT, EntityListT, TableT]):
	entity      : Type[EntityT]
	entity_list : Type[EntityListT]
	table       : Type[TableT]

	@classmethod
	async def insert_or_update(cls, s: AsyncSession, query: Union[Insert, Update]) -> dict[str, Any]:
		result = await s.execute(query)
		return dict(result.mappings().first())

	@classmethod
	async def fetch_one(cls, s: AsyncSession, query: Select) -> Optional[dict[str, Any]]:
		result = await s.execute(query)
		row = result.mappings().fetchone()
		return dict(row) if row else None

	@classmethod
	async def fetch_many(cls, s: AsyncSession, query: Select) -> list[dict[str, Any]]:
		result = await s.execute(query)
		rows = result.mappings().fetchall()
		return [dict(row) for row in rows]

	@classmethod
	def select_q(cls) -> Select:
		return select(cls.table.__table__.columns)

	@classmethod
	def filter_q(cls, **filters: Any) -> Select:
		return cls.select_q().filter_by(**filters)

	@classmethod
	def paginate_q(cls,
		q      : Select,
		limit  : Optional[int],
		offset : Optional[int]
	) -> Select:
		if offset is not None:
			q = q.offset(offset)
		if limit is not None:
			q = q.limit(limit)
		return q

	@classmethod
	async def create(cls, s: AsyncSession, entity: EntityT) -> EntityT:
		data = await cls.insert_or_update(
			s,
			insert(cls.table)
				.values(**entity.to_db())
				.returning(cls.table.__table__.columns)
		)
		return cls.entity.model_validate(data)

	@classmethod
	async def get_or_none(cls, s: AsyncSession, **filters: Any) -> Optional[EntityT]:
		data = await cls.fetch_one(
			s,
			cls.filter_q(**filters).limit(1)
		)
		if data:
			return cls.entity.model_validate(data)

	@classmethod
	async def get_all(cls,
	    s      : AsyncSession,
		limit  : Optional[int] = None,
		offset : Optional[int] = None
	) -> EntityListT:
		return cls.entity_list.model_validate(
			await cls.fetch_many(
				s,
				cls.paginate_q(cls.select_q(), limit, offset)
			)
		)

	@classmethod
	async def filter(cls,
	    s      : AsyncSession,
		limit  : Optional[int] = None,
		offset : Optional[int] = None,
		**filters: Any
	) -> EntityListT:
		return cls.entity_list.model_validate(
			await cls.fetch_many(
				s,
				cls.paginate_q(
					cls.filter_q(**filters),
					limit,
					offset
				)
			)
		)

	@classmethod
	async def exists(cls, s: AsyncSession, **filters: Any) -> bool:
		result = await s.scalars(
			select(cls.table)
				.filter_by(**filters)
		)
		row = result.first()
		return bool(row)

	@classmethod
	async def update(cls, s: AsyncSession, id: int, to_update: dict) -> EntityT:
		data = await cls.insert_or_update(
			s,
			update(cls.table)
				.values(**to_update)
				.where(cls.table.id == id)
				.returning(cls.table.__table__.columns)
		)
		return cls.entity.model_validate(data)

	@classmethod
	async def delete(cls, s: AsyncSession, id: int):
		await s.execute(
			delete(cls.table)
				.where(cls.table.id == id)
		)

RepositoryT = TypeVar('RepositoryT', bound='Repository')