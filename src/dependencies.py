from typing                          import Callable, TypeVar, Awaitable

from loguru                          import logger
from sqlalchemy.ext.asyncio          import AsyncSession

from src.domain.services             import (
	CategoryService,
	OrderService,
	ProductService,
	SubcategoryService
)
from src.domain.use_cases            import OrderUseCase
from src.infrastructure.database     import SessionFactory
from src.infrastructure.repositories import (
	SaCategoryRepository,
	SaOrderRepository,
	SaProductRepository,
	SaSubcategoryRepository
)

########## DB SESSION ##########

FuncWithSession = TypeVar('FuncWithSession', bound=Callable[..., Awaitable])

async def get_session() -> AsyncSession:
	session: AsyncSession = SessionFactory()
	try:
		async with session.begin():
			yield session
	except Exception as e:
		await session.rollback()
		logger.debug(f'the transaction was rolled back due to an error: {e}')
		raise e from e
	finally:
		await session.close()

########## SERVICES ##########

def get_category_service() -> CategoryService:
	return CategoryService(SaCategoryRepository)

def get_order_service() -> OrderService:
	return OrderService(SaOrderRepository)

def get_product_service() -> ProductService:
	return ProductService(
		SaProductRepository,
		SaOrderRepository,
		SaCategoryRepository,
		SaSubcategoryRepository
	)

def get_subcategory_service() -> SubcategoryService:
	return SubcategoryService(
		SaSubcategoryRepository,
		SaCategoryRepository
	)

########## USE CASES ##########

def get_order_use_case() -> OrderUseCase:
	return OrderUseCase(
		get_order_service(),
		get_product_service()
	)
