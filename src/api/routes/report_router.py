from fastapi          import APIRouter, Depends, status

from src.api.schemas  import (
	SalesReportPaginationFilter,
	OrderListSchema
)

class OrderRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.add_api_route(
			'/report/sales',
			self.get_sales_report,
			methods   = ['GET'],
			responses = {
				status.HTTP_200_OK: {'model': OrderListSchema}
			}
		)
	# async def get_sales_report(self,
# 	filter: SalesReportPaginationFilter = Depends(SalesReportPaginationFilter.as_query)
# ) -> OrderListResponse:
# 	report = await self.use_case.get_list_of_completed(**filter.model_dump())
# 	return OrderListResponse.model_validate(report.model_dump())