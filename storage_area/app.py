from fastapi import FastAPI
from contextlib import asynccontextmanager
from storage_area.routing.routes import get_all_routes
from storage_area.database.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(get_all_routes())


@app.get("/")
def root():
    return {"FastApi": "STORAGE AREA MANAGEMENT APPLICATION"}