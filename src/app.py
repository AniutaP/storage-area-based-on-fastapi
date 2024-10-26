from fastapi import FastAPI
from src.routing.routes import get_all_routes


app = FastAPI()
app.include_router(get_all_routes())


@app.get("/")
def root():
    return {"FastApi": "STORAGE AREA MANAGEMENT APPLICATION"}
