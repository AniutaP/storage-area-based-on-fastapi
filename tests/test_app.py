import pytest
from src.database.models.sqlalchemy_base import BaseModel
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.depends.depends import product_service
from src.schemas.products import ProductSchema
from src.database.database import setup_database
from src.depends.depends import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()
TEST_URL=os.getenv('TEST_URL')
test_db = setup_database(TEST_URL)


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncSession:
    async with test_db.engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)

        async with test_db.session_factory() as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(scope="session")
def override_get_db_session(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture(loop_scope="session")
async def async_client(override_get_db_session):
    app.dependency_overrides[get_db_session] = override_get_db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio(loop_scope="session")
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
      "FastApi": "STORAGE AREA MANAGEMENT APPLICATION"
   }

@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(db_session: AsyncSession):
    data = {"name": "milk",
        "description": None,
        "price": 10,
        "quantity": 20}
    result = await product_service.create(data, db_session)
    res = ProductSchema.model_validate(result).model_dump()

    assert res == {
        "id": 1,
        "name": "milk",
        "description": None,
        "price": 10,
        "quantity": 20}