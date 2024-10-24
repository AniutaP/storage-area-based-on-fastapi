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
        self.url: str = url
        self.echo: bool = echo
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def connect(self) -> None:
        self.engine = create_async_engine(url=self.url, echo=self.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.dispose()


def setup_database(url, echo=False):
    return DatabaseEngine(url, echo)
