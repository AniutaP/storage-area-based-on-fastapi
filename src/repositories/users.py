from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import Hasher
from src.database.models.users import UserModel
from src.dto.users import UserDTO


class UserRepository:

    async def create(self, user: UserDTO, db_session: AsyncSession) -> UserModel:
        user.password = Hasher.get_password_hash(user.password)
        user_data = asdict(user)
        new_user = UserModel(**user_data)
        db_session.add(new_user)
        await db_session.flush()
        await db_session.commit()
        return new_user

    async def get_all(self, db_session: AsyncSession) -> list[UserModel]:
        query = select(UserModel)
        result = await db_session.scalars(query)
        users = result.all()
        return users

    async def get_by_id(self, id: str, db_session: AsyncSession) -> UserModel | None:
        user = await db_session.get(UserModel, int(id))
        return user

    async def get_by_email(self, email: str, db_session: AsyncSession) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        user = await db_session.scalar(query)
        return user


    async def update_by_id(self, id: str, user: UserDTO, db_session: AsyncSession) -> UserModel | None:
        user_data = asdict(user)
        user_to_update = await db_session.get(UserModel, int(id))
        for field, value in user_data.items():
            if value:
                setattr(user_to_update, field, user_data[field])
        db_session.add(user_to_update)
        await db_session.commit()
        await db_session.refresh(user_to_update)
        return user_to_update


    async def delete_by_id(self, id: str, db_session: AsyncSession) -> None:
        user_to_delete = await db_session.get(UserModel, int(id))
        await db_session.delete(user_to_delete)
        await db_session.commit()
