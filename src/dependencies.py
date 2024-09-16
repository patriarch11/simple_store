from src.domain.services             import (
	CategoryService,
	OrderService,
	ProductService,
	SubcategoryService
)
from src.domain.use_cases            import OrderUseCase
from src.infrastructure.database     import DbSession
from src.infrastructure.repositories import (
	SaCategoryRepository,
	SaOrderRepository,
	SaProductRepository,
	SaSubcategoryRepository
)

########## SERVICES ##########

def get_category_service() -> CategoryService:
	return CategoryService(SaCategoryRepository(DbSession))

def get_order_service() -> OrderService:
	return OrderService(SaOrderRepository(DbSession))

def get_product_service() -> ProductService:
	return ProductService(
		SaProductRepository(DbSession),
		SaOrderRepository(DbSession),
		SaCategoryRepository(DbSession),
		SaSubcategoryRepository(DbSession)
	)

def get_subcategory_service() -> SubcategoryService:
	return SubcategoryService(
		SaSubcategoryRepository(DbSession),
		SaCategoryRepository(DbSession)
	)

########## USE CASES ##########

def get_order_use_case() -> OrderUseCase:
	return OrderUseCase(
		get_order_service(),
		get_product_service()
	)
