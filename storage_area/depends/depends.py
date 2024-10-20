from storage_area.repositories.products import ProductRepository
from storage_area.services.products import ProductService
from storage_area.database.database import db_engine


db_session = db_engine.get_db_session
product_repository = ProductRepository(db_session)
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
   return product_service
