from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import oauth2_scheme
from src.dto.tokens import TokenPayloadDTO
from src.dto.users import AdminDTO, UserDTO
from src.repositories.users import UserRepository
from src.services.users import UserService
from src.core.admin import configs, admin
from src.depends.database import get_db_session
from src.core.settings import hawk


user_repository = UserRepository()
user_service = UserService(user_repository)


def get_user_service() -> UserService:
    return user_service


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
) -> UserDTO | AdminDTO:

    message = "Could not validate credentials"
    credentials_exception = HTTPException(401, message)

    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        token_payload_dto = TokenPayloadDTO(**payload)
        email = token_payload_dto.sub
        if email is None:
            raise credentials_exception
    except JWTError:
        hawk.send(JWTError("error description"), {"params": "value"})
        raise credentials_exception

    user = await user_service.get_by_email(email=email, db_session=db_session)
    if user is None:
        raise credentials_exception

    if user.email == admin.email:
        user.is_superuser=True
        return user

    return user
