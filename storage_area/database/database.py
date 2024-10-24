from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from storage_area.database.sqlalchemy_base import BaseModel
from contextlib import asynccontextmanager
from storage_area.config import config
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class DatabaseEngine:

    def __init__(self, url, echo=False):
        self.url: str = url
        self.echo: bool = echo
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        self.engine = create_async_engine(url=self.url, echo=self.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def disconnect(self) -> None:
        if self.engine:
            async with self.engine.begin() as conn:
                await conn.run_sync(BaseModel.metadata.drop_all)
            await self.engine.dispose()


def setup_database(url=DATABASE_URL):
    return DatabaseEngine(url)


# database = setup_database(url=config.database.url_create())
database = setup_database()