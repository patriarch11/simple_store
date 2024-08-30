from fastapi          import APIRouter, HTTPException, status

from src.dependencies import get_order_service


class OrderRouter(APIRouter):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.service = get_order_service()

	async def reserve_product(self):
		...

	async def cancel_product_reservation(self):
		...

	async def sell(self):
		...

	async def get_sales_report(self):
		...

router = OrderRouter()
