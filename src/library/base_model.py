from datetime import datetime
from typing   import Optional

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
	id         : int
	created_at : datetime
	updated_at : Optional[datetime]
