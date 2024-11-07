from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from src.database.models import UserModel
from src.core.security import oauth2_scheme
from src.dto.tokens import TokenPayloadDTO
from src.repositories.users import UserRepository
from src.services.users import UserService
from src.core.settings import database, configs
from src.middlewares import HTTPErrorCodes
from src.depends.database import get_db_session

user_repository = UserRepository()
user_service = UserService(user_repository)


def get_user_service() -> UserService:
    return user_service


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service = Depends(get_user_service),
        db_session = Depends(get_db_session)
) -> UserModel:

    message = "Could not validate credentials"
    error = HTTPErrorCodes(401, message)
    credentials_exception =  HTTPException(error.code, error.message)

    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        print(payload)
        token_payload_dto = TokenPayloadDTO(**payload)
        email = token_payload_dto.sub
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user: UserModel = await user_service.get_by_email(email=email, db_session=db_session)
    if user is None:
        raise credentials_exception
    return user
