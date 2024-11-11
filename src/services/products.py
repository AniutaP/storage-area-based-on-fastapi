from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import hawk
from src.dto.products import ProductDTO
from src.repositories.products import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create(self, product: ProductDTO, db_session: AsyncSession):
        product_check = await self.get_by_name(name=product.name, db_session=db_session)
        if product_check:
            hawk.send(HTTPException(400, "Already exist"))
            raise HTTPException(400, "Already exist")

        return await self.repository.create(product, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: int, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'Object with id {id} not found'
            hawk.send(HTTPException(404, message))
            raise HTTPException(404, message)

        return result

    async def get_by_name(self, name: str, db_session: AsyncSession):
        result = await self.repository.get_by_name(name, db_session)
        return result

    async def update_by_id(self, product: ProductDTO, db_session: AsyncSession):
        await self.get_by_id(product.id, db_session)
        return await self.repository.update_by_id(product, db_session)

    async def delete_by_id(self, id: int, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.delete_by_id(id, db_session)
