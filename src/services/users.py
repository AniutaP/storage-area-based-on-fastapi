from dataclasses import dataclass
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.users import UserDTO
from src.repositories.users import UserRepository
from src.middlewares import HTTPErrorCodes


@dataclass
class UserService:
    repository: UserRepository

    async def create(self, user: UserDTO, db_session: AsyncSession):
        return await self.repository.create(user, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: str, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'User with id {id} not found'
            error = HTTPErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def get_by_email(self, email: str, db_session: AsyncSession):
        result = await self.repository.get_by_email(email, db_session)
        if result is None:
            message = f'User with email {email} not found'
            error = HTTPErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def update_by_id(self, id: str, user: UserDTO, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.update_by_id(id, user, db_session)

    async def delete_by_id(self, id: str, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.delete_by_id(id, db_session)
