from datetime                import datetime, timezone
from typing                  import Type, Optional

from sqlalchemy.ext.asyncio  import AsyncSession

from src.constants import SalesReportOrder, SortOrder, OrderStatus
from src.domain.entities     import SalesReportItem, SalesReport
from src.domain.repositories import (
	CategoryRepository,
	OrderRepository,
	ProductRepository,
	SubcategoryRepository
)


class ReportService:
	def __init__(self,
		category_repo    : Type[CategoryRepository],
	    subcategory_repo : Type[SubcategoryRepository],
	    order_repo       : Type[OrderRepository],
	    product_repo     : Type[ProductRepository],
	):
		self.category_repo    = category_repo
		self.subcategory_repo = subcategory_repo
		self.order_repo       = order_repo
		self.product_repo     = product_repo

	async def get_sales_report(self,
	    s                  : AsyncSession,
		category_ids       : Optional[list[int]]        = None,
	    subcategory_ids    : Optional[list[int]]        = None,
	    user_ids           : Optional[list[int]]        = None,
		product_ids        : Optional[list[int]]        = None,
	    status             : Optional[OrderStatus]      = None,
	    product_price_from : Optional[float]            = None,
	    product_price_to   : Optional[float]            = None,
	    amount_from        : Optional[float]            = None,
	    amount_to          : Optional[float]            = None,
	    order_by           : Optional[SalesReportOrder] = None,
	    sort_by            : Optional[SortOrder]        = None,

	) -> SalesReport:
		products = await self.product_repo.get_list_by_filters(
			s, product_ids, category_ids, subcategory_ids
		)
		product_id_to_product = {p.id: p for p in products.root}
		product_ids           = set(product_id_to_product.keys())
		orders = await self.order_repo.get_list_by_filters(
			s,
			status,
			user_ids,
			list(product_ids),
			product_price_from,
			product_price_to,
			amount_from,
			amount_to,
			order_by,
			sort_by
		)

		report = [
			SalesReportItem(order=o, product=product_id_to_product[o.product_id])
			for o in orders.root
		]
		return SalesReport(
			report     = report,
			created_at = datetime.now(timezone.utc),
		)
