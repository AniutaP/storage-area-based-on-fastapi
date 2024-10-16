import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from storage_area.models import ProductModel
from storage_area.repositories.product_repository import ProductRepository


class TestProduct:
    async def test_create_product(self, db_sessionmaker: async_sessionmaker[AsyncSession])-> None:
        product = await ProductRepository.create_product({"name": "apple", "price": 100, "quantity":10})
        assert isinstance(product, ProductModel)

        async with db_sessionmaker() as session:
            products = list(await session.scalars(select(ProductModel)))

        assert len(products) == 1
        assert products[0].id == product.id
        assert products[0].name == product.name