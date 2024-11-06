from fastapi import APIRouter
from src.routing.products import router as products_router
from src.routing.orders import router as order_router
from src.routing.login import router as auth_router
from src.routing.users import router as user_router


def get_all_routes():
    router = APIRouter()
    router.include_router(auth_router)
    router.include_router(user_router)
    router.include_router(products_router)
    router.include_router(order_router)

    return router
