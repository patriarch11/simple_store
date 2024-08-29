from datetime import datetime
from typing   import Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):
	id         : int
	created_at : datetime
	updated_at : Optional[datetime]
