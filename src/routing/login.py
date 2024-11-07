from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

from src.core.security import create_access_token
from src.dto.tokens import TokenPayloadDTO
from src.middlewares import HTTPErrorCodes
from src.services.login import LoginService
from src.schemas.tokens import TokenSchema
from src.depends.login import get_auth_service
from src.depends.database import get_db_session


router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        login_service: LoginService = Depends(get_auth_service),
        db_session = Depends(get_db_session)
):
    user = await login_service.authenticate_user(
        email=form_data.username, password=form_data.password, db_session=db_session
    )

    if not user:
        message = 'Incorrect username or password'
        error = HTTPErrorCodes(401, message)
        raise HTTPException(error.code, error.message)

    token_payload_dto = TokenPayloadDTO(sub=user.email)

    access_token = create_access_token(token_payload_dto)
    return {"access_token": access_token, "token_type": "bearer"}
