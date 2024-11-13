from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.products import ProductModel
from src.dto.products import ProductDTO
from src.utils import model_to_dict


class ProductRepository:

    async def create(self, product: ProductDTO, db_session: AsyncSession) -> ProductDTO:
        new_product = ProductModel(**asdict(product))
        db_session.add(new_product)
        await db_session.flush()
        await db_session.commit()
        return ProductDTO(**model_to_dict(new_product))

    async def get_all(self, db_session: AsyncSession) -> list[ProductDTO]:
        query = select(ProductModel)
        result = await db_session.scalars(query)
        if not result:
            return []
        products_to_dto = [
            ProductDTO(**model_to_dict(product)) for product in result.all()
        ]
        return products_to_dto

    async def get_by_id(self, id: int, db_session: AsyncSession) -> ProductDTO | None:
        product = await db_session.get(ProductModel, id)
        if not product:
            return None
        return ProductDTO(**model_to_dict(product))

    async def get_by_name(self, name: str, db_session: AsyncSession) -> ProductDTO | None:
        query = select(ProductModel).where(ProductModel.name == name)
        product = await db_session.scalar(query)
        if not product:
            return None
        return ProductDTO(**model_to_dict(product))

    async def update_by_id(
            self, product: ProductDTO, db_session: AsyncSession
    ) -> ProductDTO | None:
        product_data = asdict(product)
        product_to_update = await db_session.get(ProductModel, product.id)
        for field, value in product_data.items():
            if value:
                setattr(product_to_update, field, product_data[field])
        db_session.add(product_to_update)
        await db_session.commit()
        await db_session.refresh(product_to_update)
        return ProductDTO(**model_to_dict(product_to_update))

    async def delete_by_id(self, id: int, db_session: AsyncSession) -> None:
        product_to_delete = await db_session.get(ProductModel, id)
        await db_session.delete(product_to_delete)
        await db_session.commit()
