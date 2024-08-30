from src.domain.services             import (
	CategoryService,
	OrderService,
	ProductService,
	SubcategoryService
)
from src.domain.use_cases            import ProductUseCase
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
	return ProductService(SaProductRepository(DbSession))

def get_subcategory_service() -> SubcategoryService:
	return SubcategoryService(SaSubcategoryRepository(DbSession))

########## USE CASES ##########

def get_product_use_case() -> ProductUseCase:
	return ProductUseCase(
		SaProductRepository(DbSession),
		get_order_service()
	)
