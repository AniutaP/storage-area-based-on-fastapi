from pydantic import BaseModel, ConfigDict
from fastapi.security import OAuth2PasswordBearer

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
