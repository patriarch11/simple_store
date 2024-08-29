from src.domain.services             import CategoryService
from src.infrastructure.database     import DbSession
from src.infrastructure.repositories import SaCategoryRepository


def get_category_service() -> CategoryService:
	return CategoryService(SaCategoryRepository(DbSession))
