import pytest
from src.database.models.sqlalchemy_base import BaseModel
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.routing.routes import get_all_routes
from src.database.database import setup_database
from src.depends.depends import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
import json


load_dotenv()

TEST_URL=os.getenv('TEST_URL')
test_db = setup_database(TEST_URL)
app.include_router(get_all_routes())


def load_data(path):
    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    data_path = os.path.join(fixtures_path, path)
    with open(data_path) as file:
        return json.loads(file.read())


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
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1") as ac:
        yield ac