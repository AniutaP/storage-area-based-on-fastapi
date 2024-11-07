from fastapi import HTTPException
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import Hasher
from src.database.models import UserModel
from src.middlewares import HTTPErrorCodes
from src.repositories.login import LoginRepository


@dataclass
class LoginService:
    repository: LoginRepository

    async def authenticate_user(
            self, email: str, password: str, db_session: AsyncSession
    ) -> UserModel | None:

        user = await self.repository.get_user_by_email(email=email, db_session=db_session)

        if not Hasher.verify_password(password, user.password):
            return None

        return user
