from fastapi.security import OAuth2PasswordBearer
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from typing import Optional
from src.core.settings import configs
from src.dto.tokens import TokenPayloadDTO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


def create_access_token(
        token_payload_dto: TokenPayloadDTO,
        expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    token_payload_dto.exp = expire
    to_encode = asdict(token_payload_dto)
    encoded_jwt = jwt.encode(
        to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM
    )
    return encoded_jwt
