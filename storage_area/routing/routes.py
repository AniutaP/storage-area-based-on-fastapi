from fastapi import APIRouter
from storage_area.routing.products_router import router as products_router

def get_all_routes():
    router = APIRouter()
    router.include_router(products_router)
    return router