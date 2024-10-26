from src.database.models.products_models import ProductModel
from sqlalchemy import select


class ProductRepository:

    def __init__(self, db_session):
        self._session = db_session

    async def create(self, data: dict) -> ProductModel:
        async with self._session() as session:
            new_product = ProductModel(**data)
            session.add(new_product)
            await session.flush()
            await session.commit()
            return new_product

    async def get_all(self) -> list[ProductModel]:
        async with self._session() as session:
            query = select(ProductModel)
            result = await session.scalars(query)
            products = result.all()
            return products

    async def get_by_id(self, id: str) -> ProductModel | None:
        async with self._session() as session:
            product = await session.get(ProductModel, int(id))
            return product

    async def delete_by_id(self, id: str) -> None:
        async with self._session() as session:
            product_to_delete = await session.get(ProductModel, int(id))
            await session.delete(product_to_delete)
            await session.commit()

    async def update_by_id(self, id: str, data: dict) -> ProductModel | None:
        async with self._session() as session:
            data = {**data}
            product_to_update = await session.get(ProductModel, int(id))
            for field, value in data.items():
                if value:
                    setattr(product_to_update, field, data[field])
            session.add(product_to_update)
            await session.commit()
            await session.refresh(product_to_update)
            return product_to_update
