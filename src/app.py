from fastapi import FastAPI
from src.routing.routes import get_all_routes
from fastapi.responses import HTMLResponse


app = FastAPI()
app.include_router(get_all_routes())


@app.get("/")
def root():
    return HTMLResponse("<h1>FastAPI: STORAGE AREA MANAGEMENT APPLICATION</h1>")