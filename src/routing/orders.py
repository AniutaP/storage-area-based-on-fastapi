from fastapi import APIRouter, Depends
from src.services.orders import OrderService
from src.schemas.orders import OrderAddSchema, OrderSchema,OrderStatusUpdateSchema
from src.depends.depends import get_order_service, get_db_session
from src.dto.orders import OrderDTO


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=OrderSchema)
async def create_order(
    order: OrderAddSchema = Depends(),
    order_service: OrderService = Depends(get_order_service),
    db_session = Depends(get_db_session)
):
    data = order.model_dump()
    order_data = OrderDTO(**data)
    new_order = await order_service.create(data=order_data, db_session=db_session)
    return OrderSchema.model_validate(new_order)


@router.get("/", response_model=list[OrderSchema])
async def get_all_orders(
        order_service: OrderService = Depends(get_order_service),
        db_session = Depends(get_db_session)
):
    orders = await order_service.get_all(db_session=db_session)
    return [OrderSchema.model_validate(order) for order in orders]


@router.get("/{id}", response_model=OrderSchema)
async def get_by_id(
        id: str, order_service: OrderService = Depends(get_order_service),
        db_session = Depends(get_db_session)
):
    order = await order_service.get_by_id(id=id, db_session=db_session)
    return OrderSchema.model_validate(order)


@router.patch("{id}/status", response_model=OrderStatusUpdateSchema)
async def update_by_id(
    id: str,
    order: OrderStatusUpdateSchema = Depends(),
    order_service: OrderService = Depends(get_order_service),
    db_session = Depends(get_db_session)
):
    data = order.model_dump()
    print(data)
    order_data = OrderDTO(**data)
    print(order_data)
    order_to_update = await order_service.update_by_id(id=id, data=order_data, db_session=db_session)
    return OrderStatusUpdateSchema.model_validate(order_to_update)