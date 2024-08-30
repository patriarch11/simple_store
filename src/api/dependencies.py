from fastapi            import Depends, HTTPException, Request, status

from src.api.validators  import CategoryValidator
from src.dependencies    import get_product_service
from src.domain.entities import Product

__product_service = get_product_service()

validate_category = Depends(CategoryValidator())

async def get_product(request: Request) -> Product:
	if request.method in ['POST', 'PUT', 'PATCH']:
		body   = await request.json()
		product_id = body.get('product_id')
	else:
		product_id = int(request.query_params.get('product_id'))

	if product := await __product_service.get_by_id(product_id):
		return product
	raise HTTPException(status.HTTP_404_NOT_FOUND, 'Product not found')
