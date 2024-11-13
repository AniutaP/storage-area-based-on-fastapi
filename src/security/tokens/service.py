from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Optional

from src.configs.settings import configs
from src.security.tokens.dto.tokens import TokenPayloadDTO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


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
