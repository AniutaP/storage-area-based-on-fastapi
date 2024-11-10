from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.depends.orders import get_order_service
from src.services.orders import OrderService
from src.services.users import UserService
from src.schemas.users import UserAddSchema, UserSchema, UserUpdateSchema, UserWithOrdersSchema
from src.schemas.commons import DeleteSchema
from src.depends.users import get_user_service, get_current_user
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
        db_session: AsyncSession = Depends(get_db_session)
):
    data = user.model_dump()
    user_dto = UserDTO(**data)
    new_user = await user_service.create(user=user_dto, db_session=db_session)
    return UserSchema.model_validate(new_user)


@router.get("/", response_model=list[UserSchema])
async def get_all(
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    users = await user_service.get_all(db_session=db_session)
    return [UserSchema.model_validate(user) for user in users]


@router.get("/{id}", response_model=UserSchema)
async def get_by_id(
        id: str,
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    user = await user_service.get_by_id(id=id, db_session=db_session)
    return UserSchema.model_validate(user)


@router.get("/{id}/orders", response_model=UserWithOrdersSchema)
async def get_by_id_with_orders(
        id: str,
        user_service: UserService = Depends(get_user_service),
        order_service: OrderService = Depends(get_order_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    user = await user_service.get_by_id_with_orders(id=id, order_service=order_service, db_session=db_session)
    return UserWithOrdersSchema.model_validate(user)


@router.put("/{id}", response_model=UserSchema)
async def update_by_id(
        id: str,
        user: UserUpdateSchema = Depends(),
        current_user: UserDTO = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    if current_user.id != int(id) or not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)
    data = user.model_dump()
    user_dto = UserDTO(**data)
    user_to_update = await user_service.update_by_id(id=id, user=user_dto, db_session=db_session)
    return UserSchema.model_validate(user_to_update)


@router.delete("/{id}", response_model=DeleteSchema)
async def delete_by_id(
        id: str, user_service: UserService = Depends(get_user_service),
        current_user: UserDTO = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_db_session)
):
    if current_user.id != int(id) or not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    await user_service.delete_by_id(id=id, db_session=db_session)
    return DeleteSchema
