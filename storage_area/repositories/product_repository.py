from storage_area.models import ProductModel
from storage_area.database import new_session
from sqlalchemy import select
from storage_area.schemas import SProductAdd, SProduct, SProductId, SProductUpdate


class ProductRepository:
    @classmethod
    async def create_product(cls, product: SProductAdd) -> int:
        async with new_session() as session:
            data = product.model_dump()
            new_product = ProductModel(**data)
            session.add(new_product)
            await session.flush()
            await session.commit()
            return SProductId.model_validate(new_product).id

    @classmethod
    async def get_all_products(cls) -> list[SProduct]:
        async with new_session() as session:
            query = select(ProductModel)
            result = await session.execute(query)
            product_models = result.scalars().all()
            products = [SProduct.model_validate(task_model) for task_model in product_models]
            return products

    @classmethod
    async def get_product_by_id(cls, id_: int) -> SProduct | None:
        async with new_session() as session:
            product = await session.get(ProductModel, id_)
            if product is None:
                return None
            return SProduct.model_validate(product)

    @classmethod
    async def delete_product_by_id(cls, id_: int) -> None:
        async with new_session() as session:
            product_to_delete = await session.get(ProductModel, id_)
            if product_to_delete:
                await session.delete(product_to_delete)
                await session.commit()

    @classmethod
    async def update_product_by_id(cls, id_, product: SProductUpdate) -> SProduct:
        async with new_session() as session:
            data = product.model_dump()
            update_prod = await session.get(ProductModel, id_)
            for field, value in data.items():
                if value:
                    setattr(update_prod, field, data[field])
            session.add(update_prod)
            await session.commit()
            await session.refresh(update_prod)
            return SProduct.model_validate(update_prod)
