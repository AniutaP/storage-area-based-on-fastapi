from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserAddSchema(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=5)

    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserAddSchema):
    id: int


class UserUpdateSchema(BaseModel):
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: int | None = Field(default=None, min_length=5)

    model_config = ConfigDict(from_attributes=True)
