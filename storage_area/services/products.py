from storage_area.repositories.products import ProductRepository
from dataclasses import dataclass


@dataclass
class ProductService:
    repository: ProductRepository
