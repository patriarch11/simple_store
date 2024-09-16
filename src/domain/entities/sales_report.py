from pydantic import BaseModel

from .order   import  Order
from .product import Product


class SalesReportItem(BaseModel):
	order   : Order
	product : Product


class SalesReport(BaseModel):