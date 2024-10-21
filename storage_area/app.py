from fastapi import FastAPI
from contextlib import asynccontextmanager
from storage_area.routing.routes import get_all_routes
from storage_area.database.database import db_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_engine.create_tables()
    yield
    await db_engine.delete_tables()


app = FastAPI(lifespan=lifespan)
app.include_router(get_all_routes())


@app.get("/")
def root():
    return {"FastApi": "STORAGE AREA MANAGEMENT APPLICATION"}