from src.domains.products.repository import ProductRepository
from src.domains.products.service import ProductService


product_repository = ProductRepository()
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service
