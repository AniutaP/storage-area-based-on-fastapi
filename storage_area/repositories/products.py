from storage_area.database.models import ProductModel
from storage_area.database.database import new_session
from sqlalchemy import select


class ProductRepository:
    @classmethod
    async def create_product(cls, data: dict) -> ProductModel:
        async with new_session() as session:
            new_product = ProductModel(**data)
            session.add(new_product)
            await session.flush()
            await session.commit()
            return new_product

    @classmethod
    async def get_all_products(cls) -> list[ProductModel]:
        async with new_session() as session:
            query = select(ProductModel)
            result = await session.execute(query)
            products = result.scalars().all()
            return products

    @classmethod
    async def get_product_by_id(cls, id: int) -> ProductModel | None:
        async with new_session() as session:
            product = await session.get(ProductModel, id)
            if product is None:
                return None
            return product

    @classmethod
    async def delete_product_by_id(cls, id: int) -> None:
        async with new_session() as session:
            product_to_delete = await session.get(ProductModel, id)
            print(product_to_delete)
            if product_to_delete:
                await session.delete(product_to_delete)
                await session.commit()

    @classmethod
    async def update_product_by_id(cls, id, data: dict) -> ProductModel:
        async with new_session() as session:
            data = {**data}
            product_to_update = await session.get(ProductModel, id)
            for field, value in data.items():
                if value:
                    setattr(product_to_update, field, data[field])
            session.add(product_to_update)
            await session.commit()
            await session.refresh(product_to_update)
            return product_to_update
