from sqlalchemy import (
    Column,
    Integer,
	String,
	ForeignKey
)

from src.infrastructure.database import Base
from src.library                 import Table


class SubcategoryTable(Base, Table):
	__tablename__ = 'subcategories'

	id          = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'), nullable=False, index=True)
	name        = Column(String(255), nullable=False, unique=True)
