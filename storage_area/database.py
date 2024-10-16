from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
   async with engine.begin() as conn:
       await conn.run_sync(BaseModel.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(BaseModel.metadata.drop_all)