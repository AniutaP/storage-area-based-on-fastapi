from fastapi import APIRouter, Depends
from storage_area.services.products import ProductService
from storage_area.schemas.products import SProduct, SProductAdd, SProductUpdate
from storage_area.depends.depends import get_product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=SProduct)
async def create(product: SProductAdd = Depends(), product_service: ProductService = Depends(get_product_service)):
    data = product.model_dump()
    new_product = await product_service.create(data)
    return SProduct.model_validate(new_product)


@router.get("/", response_model=list[SProduct])
async def get_all(product_service: ProductService = Depends(get_product_service)):
   products = await product_service.get_all()
   return [SProduct.model_validate(product) for product in products]


@router.get("{id}", response_model=SProduct)
async def get_by_id(id, product_service: ProductService = Depends(get_product_service)):
    product = await product_service.get_by_id(id=id)
    return SProduct.model_validate(product)


@router.put("{id}", response_model=SProduct)
async def update_by_id(id, product: SProductUpdate = Depends(), product_service: ProductService = Depends(get_product_service)):
    data = product.model_dump()
    product_to_update = await product_service.update_by_id(id=id, data=data)
    return SProduct.model_validate(product_to_update)


@router.delete("{id}")
async def delete_by_id(id, product_service: ProductService = Depends(get_product_service)):
    await product_service.delete_by_id(id=id)
    return {"Done": True}