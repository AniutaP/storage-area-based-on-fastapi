from fastapi import APIRouter
from storage_area.routing.products import router as products_router
from storage_area.routing.orders import router as order_router


def get_all_routes():
    router = APIRouter()
    router.include_router(products_router)
    router.include_router(order_router)
    return router
