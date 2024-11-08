from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.users import UserModel


class LoginRepository:

    async def get_user_by_email(self, email: str, db_session: AsyncSession) ->  UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        user = await db_session.scalar(query)
        return user
