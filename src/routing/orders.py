from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.settings import hawk
from src.depends.users import get_current_user
from src.domains.orders.service import OrderService
from src.domains.orders.schemas.orders import (
    OrderAddSchema, OrderSchema, OrderStatusUpdateSchema,
    OrderIdSchema, DeleteSchema
)
from src.depends.orders import get_order_service
from src.depends.database import get_db_session
from src.domains.orders.dto.orders import OrderDTO, OrderItemDTO, OrderUpdateDTO
from src.domains.users.dto.users import UserDTO


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=OrderSchema)
async def create_order(
        order: OrderAddSchema = Depends(),
        current_user: UserDTO = Depends(get_current_user),
        order_service: OrderService = Depends(get_order_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user:
        message = "Not authenticated"
        raise HTTPException(401, message)

    data = order.model_dump()
    orderitems = [OrderItemDTO(**item_data) for item_data in data['orderitems']]
    order_dto = OrderDTO(
        status=order.status, user_id=current_user.id, orderitems=orderitems
    )
    new_order = await order_service.create(order=order_dto, db_session=db_session)
    return OrderSchema.model_validate(new_order)


@router.get("/", response_model=list[OrderSchema])
async def get_all_orders(
        order_service: OrderService = Depends(get_order_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    orders = await order_service.get_all(db_session=db_session)
    return [OrderSchema.model_validate(order) for order in orders]


@router.get("/{id}", response_model=OrderSchema)
async def get_by_id(
        order: OrderIdSchema = Depends(),
        order_service: OrderService = Depends(get_order_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    order_id = order.model_dump().get('id')
    order = await order_service.get_by_id(id=order_id, db_session=db_session)
    return OrderSchema.model_validate(order)


@router.patch("/{id}/status", response_model=OrderStatusUpdateSchema)
async def update_status_by_id(
        order: OrderStatusUpdateSchema = Depends(),
        current_user: UserDTO = Depends(get_current_user),
        order_service: OrderService = Depends(get_order_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    data = order.model_dump()
    order_dto = OrderUpdateDTO(**data)
    order_to_update = await order_service.update_status_by_id(
        order=order_dto, db_session=db_session
    )
    return OrderStatusUpdateSchema.model_validate(order_to_update)


@router.delete("/{id}", response_model=DeleteSchema)
async def delete_by_id(
        order: OrderIdSchema = Depends(),
        order_service: OrderService = Depends(get_order_service),
        current_user: UserDTO = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    order_id = order.model_dump().get('id')
    try:
        await order_service.delete_by_id(id=order_id, db_session=db_session)
        return DeleteSchema
    except Exception as exc:
        hawk.send(exc)
        raise exc
