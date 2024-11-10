from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.users import UserDTO
from src.repositories.users import UserRepository
from src.core.security import Hasher


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user: UserDTO, db_session: AsyncSession):
        user_check = await self.get_by_email(email=user.email, db_session=db_session)
        if user_check:
            raise HTTPException(400, "User already registered")

        user.password = Hasher.get_password_hash(user.password)
        return await self.repository.create(user, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: str, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'User with id {id} not found'
            raise HTTPException(404, message)

        return result

    async def get_by_email(self, email: str, db_session: AsyncSession):
        return await self.repository.get_by_email(email, db_session)

    async def update_by_id(self, id: str, user: UserDTO, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.update_by_id(id, user, db_session)

    async def delete_by_id(self, id: str, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.delete_by_id(id, db_session)
