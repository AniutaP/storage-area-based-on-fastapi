import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from storage_area.models import ProductModel


@pytest.fixture
async def product_1(db_sessionmaker: async_sessionmaker[AsyncSession]) -> ProductModel:
    new_product = ProductModel(name="apple", price=100, quantity=10)
    async with db_sessionmaker() as session:
        session.add(new_product)
        await session.flush()
        await session.commit()
    return new_product


@pytest.fixture
async def product_2(db_sessionmaker: async_sessionmaker[AsyncSession]) -> ProductModel:
    new_product = ProductModel(name="orange", price=200, quantity=5)
    async with db_sessionmaker() as session:
        session.add(new_product)
        await session.flush()
        await session.commit()
    return new_product