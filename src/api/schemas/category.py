from datetime import datetime
from typing   import Optional

from pydantic import BaseModel

class CategoryCreate(BaseModel):
	name: str


class CategoryResponse(CategoryCreate):
	id         : int
	created_at : datetime
	updated_at : Optional[datetime]
