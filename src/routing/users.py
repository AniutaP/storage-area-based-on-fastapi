from fastapi import APIRouter, Depends
from src.services.users import UserService
from src.schemas.users import UserAddSchema, UserSchema, UserUpdateSchema
from src.depends.users import get_user_service
from src.depends.database import get_db_session
from src.dto.users import UserDTO

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserSchema)
async def create(
        user: UserAddSchema = Depends(),
        user_service: UserService = Depends(get_user_service),
        db_session = Depends(get_db_session)
):
    data = user.model_dump()
    user_dto = UserDTO(**data)
    new_user = await user_service.create(user=user_dto, db_session=db_session)
    return UserSchema.model_validate(new_user)


@router.get("/", response_model=list[UserSchema])
async def get_all(
        user_service: UserService = Depends(get_user_service),
        db_session = Depends(get_db_session)
):
    users = await user_service.get_all(db_session=db_session)
    return [UserSchema.model_validate(user) for user in users]


@router.get("/{id}", response_model=UserSchema)
async def get_by_id(
        id: str, user_service: UserService = Depends(get_user_service),
        db_session = Depends(get_db_session)
):
    user = await user_service.get_by_id(id=id, db_session=db_session)
    return UserSchema.model_validate(user)


@router.put("/{id}", response_model=UserSchema)
async def update_by_id(
    id: str,
    user: UserUpdateSchema = Depends(),
    user_service: UserService = Depends(get_user_service),
    db_session = Depends(get_db_session)
):
    data = user.model_dump()
    user_dto = UserDTO(**data)
    user_to_update = await user_service.update_by_id(id=id, user=user_dto, db_session=db_session)
    return UserSchema.model_validate(user_to_update)


@router.delete("/{id}")
async def delete_by_id(
    id: str, user_service: UserService = Depends(get_user_service),
    db_session = Depends(get_db_session)
):
    await user_service.delete_by_id(id=id, db_session=db_session)
    return {"Done": True}
