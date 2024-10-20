from storage_area.repositories.products import ProductRepository
from storage_area.services.products import ProductService


product_repository = ProductRepository()
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
   return product_service