from typing           import Any, Optional
from fastapi          import Request, status, HTTPException

from src.dependencies import get_category_service, get_subcategory_service

# here is placed validators,
# that uses in api routers with fastapi.Depends


class CategoryValidator:
	@staticmethod
	def _validate_type(id: Any) -> int:
		if not isinstance(id, int):
			try:
				return int(id)
			except ValueError:
				raise HTTPException(
					status.HTTP_422_UNPROCESSABLE_ENTITY,
					f'Id mus be a valid integer, got {id}'
				)
		return id

	def __init__(self):
		self.category_service    = get_category_service()
		self.subcategory_service = get_subcategory_service()

	async def __call__(self, request: Request):
		if request.method in ['POST', 'PUT', 'PATCH']:
			body           = await request.json()
			category_id    = body.get('category_id')
			subcategory_id = body.get('subcategory_id')
		else:
			category_id    = request.query_params.get('category_id')
			subcategory_id = request.query_params.get('subcategory_id')

		if category_id is not None:
			category_id = self._validate_type(category_id)
			await self._validate_category(category_id)

		if subcategory_id is not None:
			subcategory_id = self._validate_type(subcategory_id)
			await self._validate_subcategory(subcategory_id, category_id)

	async def _validate_category(self, category_id: int):
		if not await self.category_service.exists_id(category_id):
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Caregory does not exists')

	async def _validate_subcategory(self,
		subcategory_id : int,
		category_id    : Optional[int]
	):
		subcategory = await self.subcategory_service.get_by_id(subcategory_id)
		if not subcategory:
			raise HTTPException(status.HTTP_404_NOT_FOUND, 'Subcategory does not exists')
		if category_id and subcategory.category_id != category_id:
			raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Subcategory does not match for category')
