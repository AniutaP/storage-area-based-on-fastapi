from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.settings import hawk
from src.domains.users.dto.users import UserDTO, UserWithOrdersDTO
from src.domains.users.repository import UserRepository
from src.security.hasher.hasher import Hasher
from src.domains.orders.service import OrderService
from dataclasses import asdict


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def authenticate_user(
            self, email: str, password: str, db_session: AsyncSession
    ) -> UserDTO | None:
        user = await self.repository.get_by_email(email=email, db_session=db_session)

        if not user:
            return None
        if not Hasher.verify_password(password, user.password):
            return None

        return user

    async def create(self, user: UserDTO, db_session: AsyncSession):
        user_check = await self.get_by_email(email=user.email, db_session=db_session)
        if user_check:
            raise HTTPException(400, "User already registered")

        user.password = Hasher.get_password_hash(user.password)
        return await self.repository.create(user, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: int, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'User with id {id} not found'
            hawk.send(HTTPException(404, message))
            raise HTTPException(404, message)

        return result

    async def get_by_id_with_orders(
            self, id: int, order_service: OrderService, db_session: AsyncSession
    ):
        user = await self.get_by_id(id, db_session)
        orders = await order_service.get_all(db_session, user_id=id)
        user_data = asdict(user)
        user = UserWithOrdersDTO(**user_data)
        user.orders = orders
        return user

    async def get_by_email(self, email: str, db_session: AsyncSession):
        return await self.repository.get_by_email(email, db_session)

    async def update_by_id(self, user: UserDTO, db_session: AsyncSession):
        await self.get_by_id(user.id, db_session)
        return await self.repository.update_by_id(user, db_session)

    async def delete_by_id(self, id: int, db_session: AsyncSession):
        to_delete_dto = await self.get_by_id(id, db_session)
        await self.repository.delete_by_id(to_delete_dto, db_session)
