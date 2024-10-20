from fastapi import APIRouter, Depends, Body
from storage_area.services.products import ProductService
from storage_area.schemas.products import SProduct, SProductAdd, SProductUpdate
from storage_area.depends.depends import get_product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=SProduct)
async def create_product(product: SProductAdd = Depends(), product_service: ProductService = Depends(get_product_service)):
    data = product.model_dump()
    new_product = await product_service.repository.create_product(data)
    return SProduct.model_validate(new_product)


@router.get("/", response_model=list[SProduct])
async def get_all_products(product_service: ProductService = Depends(get_product_service)):
   products = await product_service.repository.get_all_products()
   return [SProduct.model_validate(product) for product in products]


@router.get("{id}", response_model=SProduct)
async def get_product_by_id(id, product_service: ProductService = Depends(get_product_service)):
    product = await product_service.repository.get_product_by_id(id_=id)
    return SProduct.model_validate(product)

@router.put("{id}", response_model=SProduct)
async def update_product_by_id(id, product: SProductUpdate = Depends(), product_service: ProductService = Depends(get_product_service)):
    data = product.model_dump()
    prod_to_update = await product_service.repository.update_product_by_id(id_=id, data=data)
    return SProduct.model_validate(prod_to_update)


@router.delete("{id}")
async def delete_product_by_id(id, product_service: ProductService = Depends(get_product_service)) -> None:
    await product_service.repository.delete_product_by_id(id_=id)