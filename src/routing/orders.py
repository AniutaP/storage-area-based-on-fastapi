from fastapi import APIRouter, Depends
from src.services.orders import OrderService
from src.schemas.orders import OrderAddSchema, OrderSchema,OrderStatusUpdateSchema
from src.depends.depends import get_order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=OrderSchema)
async def create_order(
    order: OrderAddSchema = Depends(),
    order_service: OrderService = Depends(get_order_service),
):
    data = order.model_dump()
    new_order = await order_service.create(data)
    return OrderSchema.model_validate(new_order)


@router.get("/", response_model=list[OrderSchema])
async def get_all_orders(
        order_service: OrderService = Depends(get_order_service)
):
    orders = await order_service.get_all()
    return [OrderSchema.model_validate(order) for order in orders]


@router.get("/{id}", response_model=OrderSchema)
async def get_by_id(
        id: str, order_service: OrderService = Depends(get_order_service)
):
    order = await order_service.get_by_id(id=id)
    return OrderSchema.model_validate(order)


@router.patch("{id}/status", response_model=OrderStatusUpdateSchema)
async def update_by_id(
    id: str,
    order: OrderStatusUpdateSchema = Depends(),
    order_service: OrderService = Depends(get_order_service),
):
    data = order.model_dump()
    order_to_update = await order_service.update_by_id(id=id, data=data)
    return OrderStatusUpdateSchema.model_validate(order_to_update)
