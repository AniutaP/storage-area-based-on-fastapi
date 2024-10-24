from fastapi import APIRouter, Depends
from storage_area.services.orders import OrderService
from storage_area.schemas.orders import SOrderAdd, SOrder, SOrderStatusUpdate
from storage_area.depends.depends import get_order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=SOrder)
async def create_order(
        order: SOrderAdd = Depends(),
        order_service: OrderService = Depends(get_order_service)
):
    data = order.model_dump()
    new_order = await order_service.create(data)
    return SOrder.model_validate(new_order)


@router.get("/", response_model=list[SOrder])
async def get_all_orders(order_service: OrderService = Depends(get_order_service)):
   orders = await order_service.get_all()
   return [SOrder.model_validate(order) for order in orders]


@router.get("/{id}", response_model=SOrder)
async def get_by_id(id, order_service: OrderService = Depends(get_order_service)):
    order = await order_service.get_by_id(id=id)
    return SOrder.model_validate(order)


@router.patch("{id}/status", response_model=SOrderStatusUpdate)
async def update_by_id(
        id,
        order: SOrderStatusUpdate = Depends(),
        order_service: OrderService = Depends(get_order_service)
):
    data = order.model_dump()
    order_to_update = await order_service.update_by_id(id=id, data=data)
    return SOrderStatusUpdate.model_validate(order_to_update)
