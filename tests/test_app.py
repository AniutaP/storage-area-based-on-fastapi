import pytest
from src.database.models.sqlalchemy_base import BaseModel
from src.settings import database as test_database
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.depends.depends import product_service
from src.schemas.products import ProductSchema


async def create_tables():
    async with test_database.engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture(loop_scope="session")
async def async_client():
    await create_tables()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio(loop_scope="session")
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
      "FastApi": "STORAGE AREA MANAGEMENT APPLICATION"
   }

@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(async_client):
    data = {"name": "milk",
        "description": None,
        "price": 10,
        "quantity": 20}
    result = await product_service.create(data)
    res = ProductSchema.model_validate(result).model_dump()

    assert res == {
        "id": 1,
        "name": "milk",
        "description": None,
        "price": 10,
        "quantity": 20}