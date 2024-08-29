from src.api.routes     import (
	CategoryRouter,
	OrderRouter,
	ProductRouter,
	SubcategoryRouter
)
from src.domain.services import (
	CategoryService,
	OrderService,
	ProductService,
	SubcategoryService
)
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

########## ROUTES ##########

def get_category_router() -> CategoryRouter:
	return CategoryRouter(get_category_service())

def get_order_router() -> OrderRouter:
	return OrderRouter(get_order_service())

def get_product_router() -> ProductRouter:
	return ProductRouter(get_product_service())

def get_subcategory_router() -> SubcategoryRouter:
	return SubcategoryRouter(get_subcategory_service())
