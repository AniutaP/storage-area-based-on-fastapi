from src.repositories.orders import OrderRepository
from src.services.orders import OrderService


order_repository = OrderRepository()
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
    return order_service
