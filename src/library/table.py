from typing     import TypeVar
from datetime   import datetime, timezone

from sqlalchemy import Column, Integer, TIMESTAMP


class Table:
	id         = Column(Integer, primary_key=True)
	created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
	updated_at = Column(TIMESTAMP(timezone=True), onupdate=lambda: datetime.now(timezone.utc))
	
TableT = TypeVar('TableT', bound=Table)
