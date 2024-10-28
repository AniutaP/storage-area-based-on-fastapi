from src.repositories.products import ProductRepository
from dataclasses import dataclass
from fastapi import HTTPException
from src.middlewares import HTTPErrorCodes
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.products import ProductDTO


@dataclass
class ProductService:
    repository: ProductRepository

    async def create(self, data: ProductDTO, db_session: AsyncSession):
        return await self.repository.create(data, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: str, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'Object with id {id} not found'
            error = HTTPErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def update_by_id(self, id: str, data: ProductDTO, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.update_by_id(id, data, db_session)

    async def delete_by_id(self, id: str, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.delete_by_id(id, db_session)
