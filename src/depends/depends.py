from src.repositories.products import ProductRepository
from src.services.products import ProductService
from src.repositories.orders import OrderRepository
from src.services.orders import OrderService
from src.settings import database
from typing import AsyncGenerator


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        yield session
        await session.close()


product_repository = ProductRepository()
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service


order_repository = OrderRepository()
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
    return order_service
