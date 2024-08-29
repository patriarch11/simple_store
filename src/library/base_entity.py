from datetime import datetime
from typing   import Any, Optional

from pydantic import BaseModel


class BaseEntity(BaseModel):
	id         : Optional[int]      = None
	created_at : Optional[datetime] = None
	updated_at : Optional[datetime] = None

	def to_db(self) -> dict[str, Any]:
		data = self.model_dump()
		skip_fields = ['id', 'created_at', 'updated_at']
		for field in skip_fields:
			del data[field]
		return data
