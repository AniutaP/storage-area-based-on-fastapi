from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.products import ProductModel
from src.dto.products import ProductDTO


class ProductRepository:

    async def create(self, product: ProductDTO, db_session: AsyncSession) -> ProductModel:
        product_data = asdict(product)
        new_product = ProductModel(**product_data)
        db_session.add(new_product)
        await db_session.flush()
        await db_session.commit()
        return new_product

    async def get_all(self, db_session: AsyncSession) -> list[ProductModel]:
        query = select(ProductModel)
        result = await db_session.scalars(query)
        print(result)
        products = result.all()
        return products

    async def get_by_id(self, id: str, db_session: AsyncSession) -> ProductModel | None:
        product = await db_session.get(ProductModel, int(id))
        return product

    async def get_by_name(self, name: str, db_session: AsyncSession) -> ProductModel | None:
        query = select(ProductModel).where(ProductModel.name == name)
        product = await db_session.scalar(query)
        return product

    async def update_by_id(self, id: str, product: ProductDTO, db_session: AsyncSession) -> ProductModel | None:
        product_data = asdict(product)
        product_to_update = await db_session.get(ProductModel, int(id))
        for field, value in product_data.items():
            if value:
                setattr(product_to_update, field, product_data[field])
        db_session.add(product_to_update)
        await db_session.commit()
        await db_session.refresh(product_to_update)
        return product_to_update

    async def delete_by_id(self, id: str, db_session: AsyncSession) -> None:
        product_to_delete = await db_session.get(ProductModel, int(id))
        await db_session.delete(product_to_delete)
        await db_session.commit()
