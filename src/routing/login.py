from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

from src.depends.users import get_user_service
from src.domains.users.service import UserService
from src.security.tokens.dto.tokens import TokenPayloadDTO
from src.security.tokens.schemas.tokens import TokenSchema
from src.depends.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.security.tokens.service import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/token", response_model=TokenSchema)
async def authenticate_user(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    user = await user_service.authenticate_user(
        email=form_data.username, password=form_data.password, db_session=db_session
    )

    if not user:
        message = 'Incorrect email or password'
        raise HTTPException(401, message)

    token_payload_dto = TokenPayloadDTO(sub=user.email)
    access_token = create_access_token(token_payload_dto)
    response.set_cookie(key='user_token', value=access_token, httponly=True)
    return TokenSchema(access_token=access_token, token_type="bearer")
