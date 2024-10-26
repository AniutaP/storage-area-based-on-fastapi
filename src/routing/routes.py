from fastapi import APIRouter
from src.routing.products import router as products_router
from src.routing.orders import router as order_router


def get_all_routes():
    router = APIRouter()
    router.include_router(products_router)
    router.include_router(order_router)
    return router
