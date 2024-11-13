from src.domains.orders.repository import OrderRepository
from src.domains.orders.service import OrderService


order_repository = OrderRepository()
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
    return order_service
