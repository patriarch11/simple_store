from fastapi                import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.schemas       import (
	SalesReportFilter,
	SalesReportSchema
)
from src.dependencies       import get_report_service, get_session


class ReportRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service = get_report_service()
		self.add_api_route(
			'/sales',
			self.get_sales_report,
			methods   = ['GET'],
			responses = {
				status.HTTP_200_OK: {'model': SalesReportSchema}
			}
		)
	async def get_sales_report(self,
	    f : SalesReportFilter = Depends(SalesReportFilter.as_query),
		s : AsyncSession      = Depends(get_session)
	) -> SalesReportSchema:
		report = await self.service.get_sales_report(s, **f.model_dump())
		return SalesReportSchema.model_validate(report.model_dump())

router = ReportRouter()
