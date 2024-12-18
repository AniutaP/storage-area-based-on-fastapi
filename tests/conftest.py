import pytest
from src.core.database.models.sqlalchemy_base import BaseModel
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app
from src.depends.users import get_current_user
from src.routing import get_all_routes
from src.core.database.database import setup_database
from src.depends.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.users.dto.users import UserDTO
import os
from dotenv import load_dotenv
import json


load_dotenv()

TEST_URL=os.getenv('TEST_URL')
test_db = setup_database(TEST_URL, echo=False)
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


@pytest.fixture(scope="session")
def override_get_current_user():
    def _override_get_current_user():
        user = UserDTO(
            id=1, email=os.getenv('ADMIN_EMAIL'), password=os.getenv('ADMIN_PASSWORD'), is_superuser=True
        )
        return user
    return _override_get_current_user


@pytest_asyncio.fixture(loop_scope="session")
async def async_client(override_get_db_session, override_get_current_user):
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1") as ac:
        yield ac