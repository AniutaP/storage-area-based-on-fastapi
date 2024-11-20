import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.routing import get_all_routes

app = FastAPI()

logging.basicConfig(
    filename='info.log',
    level=logging.INFO,
    filemode='w',
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S'

)

app.include_router(get_all_routes())


@app.get("/")
def root():
    return HTMLResponse(
        "<h1>FastAPI: STORAGE AREA MANAGEMENT APPLICATION</h1>"
    )
