from fastapi import FastAPI
from contextlib import asynccontextmanager
from storage_area.database import create_tables, delete_tables
from storage_area.routing.products_router import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Database is ready")
    yield
    await delete_tables()
    print("Database is clear")


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)


@app.get('/')
async def root():
    return {'text': 'my first fastapi app'}
