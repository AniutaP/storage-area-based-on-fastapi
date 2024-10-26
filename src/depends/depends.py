from src.repositories.products import ProductRepository
from src.services.products import ProductService
from src.repositories.orders import OrderRepository
from src.services.orders import OrderService
from src.settings import database


def get_database_session():
    return database.get_db_session()


product_repository = ProductRepository(db_session=get_database_session)
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service


order_repository = OrderRepository(db_session=get_database_session)
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
    return order_service
