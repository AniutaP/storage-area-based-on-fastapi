from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,  AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import exc
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class BaseModel(DeclarativeBase):
    pass


class DatabaseEngine:

    def __init__(self, db_url: str):
        self.engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_db_session(self):
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_tables(self):
       async with self.engine.begin() as conn:
           await conn.run_sync(BaseModel.metadata.create_all)

    async def delete_tables(self):
       async with self.engine.begin() as conn:
           await conn.run_sync(BaseModel.metadata.drop_all)


db_engine = DatabaseEngine(DATABASE_URL)