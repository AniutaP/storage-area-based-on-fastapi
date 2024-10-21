from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class BaseModel(DeclarativeBase):
    pass


class DatabaseEngine:

    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def create_tables(self):
       async with self.engine.begin() as conn:
           await conn.run_sync(BaseModel.metadata.create_all)

    async def delete_tables(self):
       async with self.engine.begin() as conn:
           await conn.run_sync(BaseModel.metadata.drop_all)


db_engine = DatabaseEngine(url=DATABASE_URL,echo=False)