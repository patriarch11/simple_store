from src.domain.entities     import Product, ProductList
from src.domain.repositories import ProductRepository
from src.library             import Service


class ProductService(Service[Product, ProductList, ProductRepository]):
	...
