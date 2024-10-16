from fastapi import APIRouter, Depends
from storage_area.repositories.product_repository import ProductRepository
from storage_area.schemas import SProduct, SProductAdd, SProductId, SProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("")
async def create_product(product: SProductAdd = Depends()) -> int:
   new_product_id = await ProductRepository.create_product(product)
   return new_product_id


@router.get("")
async def get_all_products() -> list[SProduct]:
   products = await ProductRepository.get_all_products()
   return products


@router.get("/<int:id>")
async def get_product_by_id(id) -> SProduct:
    product = await ProductRepository.get_product_by_id(id_=id)
    return product

@router.put("/<int:id>")
async def update_product_by_id(id, product: SProductUpdate = Depends()) -> SProduct:
    update_prod = await ProductRepository.update_product_by_id(id_=id, product=product)
    return update_prod


@router.delete("/<int:id>")
async def delete_product_by_id(id) -> None:
    await ProductRepository.delete_product_by_id(id_=id)