from fastapi import APIRouter, Depends
from src.services.products import ProductService
from src.schemas.products import ProductAddSchema, ProductSchema, ProductUpdateSchema
from src.depends.depends import get_product_service, get_db_session
from src.dto.products import ProductDTO

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductSchema)
async def create(
        product: ProductAddSchema = Depends(),
        product_service: ProductService = Depends(get_product_service),
        db_session = Depends(get_db_session)
):
    data = product.model_dump()
    product_dto = ProductDTO(**data)
    new_product = await product_service.create(product=product_dto, db_session=db_session)
    return ProductSchema.model_validate(new_product)


@router.get("/", response_model=list[ProductSchema])
async def get_all(
        product_service: ProductService = Depends(get_product_service),
        db_session = Depends(get_db_session)
):
    products = await product_service.get_all(db_session=db_session)
    return [ProductSchema.model_validate(product) for product in products]


@router.get("/{id}", response_model=ProductSchema)
async def get_by_id(
        id: str, product_service: ProductService = Depends(get_product_service),
        db_session = Depends(get_db_session)
):
    product = await product_service.get_by_id(id=id, db_session=db_session)
    return ProductSchema.model_validate(product)


@router.put("/{id}", response_model=ProductSchema)
async def update_by_id(
    id: str,
    product: ProductUpdateSchema = Depends(),
    product_service: ProductService = Depends(get_product_service),
    db_session = Depends(get_db_session)
):
    data = product.model_dump()
    product_dto = ProductDTO(**data)
    product_to_update = await product_service.update_by_id(id=id, product=product_dto, db_session=db_session)
    return ProductSchema.model_validate(product_to_update)


@router.delete("/{id}")
async def delete_by_id(
    id: str, product_service: ProductService = Depends(get_product_service),
    db_session = Depends(get_db_session)
):
    await product_service.delete_by_id(id=id, db_session=db_session)
    return {"Done": True}
