from datetime import datetime
from typing   import Optional

from pydantic import BaseModel


class Schema(BaseModel):
	id         : int
	created_at : datetime
	updated_at : Optional[datetime]

	@classmethod
	def from_entity(cls, entity: BaseModel) -> 'Schema':
		return cls.model_validate(entity.model_dump())
