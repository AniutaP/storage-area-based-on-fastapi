from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from contextlib import asynccontextmanager


class DatabaseEngine:

    def __init__(self, url: str, echo: bool):
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


def setup_database(url, echo=True):
    return DatabaseEngine(url, echo)
