from storage_area.repositories.products import ProductRepository
from storage_area.services.products import ProductService
from storage_area.repositories.orders import OrderRepository
from storage_area.services.orders import OrderService
from storage_area.database.database import db_engine


product_repository = ProductRepository(db_session=db_engine.get_db_session)
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
   return product_service


order_repository = OrderRepository(db_session=db_engine.get_db_session)
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
   return order_service