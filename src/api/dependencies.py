from fastapi             import Depends, HTTPException, Request, status

# from src.api.schemas     import GetOrderSchema
from src.api.validators  import CategoryValidator
from src.constants       import OrderStatus
from src.dependencies    import get_order_service, get_product_service
from src.domain.entities import Order, Product

__product_service = get_product_service()
__order_service   = get_order_service()

validate_category = Depends(CategoryValidator())

async def get_product(request: Request) -> Product:
	if request.method in ['POST', 'PUT', 'PATCH']:
		body       = await request.json()
		product_id = body.get('product_id')
	else:
		product_id = int(request.query_params.get('product_id'))

	if product := await __product_service.get_by_id(product_id):
		return product
	raise HTTPException(status.HTTP_404_NOT_FOUND, 'Product not found')

# async def get_order(request: GetOrderSchema) -> Order:
# 	if order := await __order_service.get_by_id(request.order_id):
# 		return order
# 	raise HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
#
# async def get_reserved_order(order: Order = Depends(get_order)) -> Order:
# 	if order.status == OrderStatus.RESERVED:
# 		return order
# 	raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Order status must be "RESERVED"')
