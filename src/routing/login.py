from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

from src.core.security import create_access_token
from src.dto.tokens import TokenPayloadDTO
from src.services.login import LoginService
from src.schemas.tokens import TokenSchema
from src.depends.login import get_auth_service
from src.depends.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        login_service: LoginService = Depends(get_auth_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    user = await login_service.authenticate_user(
        email=form_data.username, password=form_data.password, db_session=db_session
    )

    if not user:
        message = 'Incorrect email or password'
        raise HTTPException(401, message)

    token_payload_dto = TokenPayloadDTO(sub=user.email)
    access_token = create_access_token(token_payload_dto)
    return TokenSchema(access_token=access_token, token_type="bearer")
