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
            product_models = result.scalars().all()
            return product_models

    @classmethod
    async def get_product_by_id(cls, id_: int) -> ProductModel | None:
        async with new_session() as session:
            product = await session.get(ProductModel, id_)
            if product is None:
                return None
            return product

    @classmethod
    async def delete_product_by_id(cls, id_: int) -> None:
        async with new_session() as session:
            product_to_delete = await session.get(ProductModel, id_)
            if product_to_delete:
                await session.delete(product_to_delete)
                await session.commit()

    @classmethod
    async def update_product_by_id(cls, id_, data: dict) -> ProductModel:
        async with new_session() as session:
            data = {**data}
            prod_to_update = await session.get(ProductModel, id_)
            for field, value in data.items():
                if value:
                    setattr(prod_to_update, field, data[field])
            session.add(prod_to_update)
            await session.commit()
            await session.refresh(prod_to_update)
            return prod_to_update
