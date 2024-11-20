import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.settings import hawk
from src.domains.products.service import ProductService
from src.domains.products.schemas.products import (
    ProductAddSchema, ProductSchema, ProductIdSchema
)
from src.domains.products.schemas.products import DeleteSchema
from src.depends.products import get_product_service
from src.depends.database import get_db_session
from src.depends.users import get_current_user
from src.domains.products.dto.products import ProductDTO
from src.domains.users.dto.users import UserDTO


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductSchema)
async def create(
        product: ProductAddSchema = Depends(),
        product_service: ProductService = Depends(get_product_service),
        current_user: UserDTO = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    data = product.model_dump()
    product_dto = ProductDTO(**data)
    new_product = await product_service.create(product=product_dto, db_session=db_session)
    return ProductSchema.model_validate(new_product)


@router.get("/", response_model=list[ProductSchema])
async def get_all(
        product_service: ProductService = Depends(get_product_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    products = await product_service.get_all(db_session=db_session)
    return [ProductSchema.model_validate(product) for product in products]


@router.get("/{id}", response_model=ProductSchema)
async def get_by_id(
        product: ProductIdSchema = Depends(),
        product_service: ProductService = Depends(get_product_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    product_id = product.model_dump().get('id')
    product = await product_service.get_by_id(id=product_id, db_session=db_session)
    return ProductSchema.model_validate(product)


@router.put("/{id}", response_model=ProductSchema)
async def update_by_id(
        product: ProductSchema = Depends(),
        current_user: UserDTO = Depends(get_current_user),
        product_service: ProductService = Depends(get_product_service),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    data = product.model_dump()
    product_dto = ProductDTO(**data)
    product_to_update = await product_service.update_by_id(
        product=product_dto, db_session=db_session
    )
    return ProductSchema.model_validate(product_to_update)


@router.delete("/{id}", response_model=DeleteSchema)
async def delete_by_id(
        product: ProductIdSchema = Depends(),
        product_service: ProductService = Depends(get_product_service),
        current_user: UserDTO = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_db_session)
):
    if not current_user.is_superuser:
        message = "Forbidden: You do not have permission to perform this action"
        raise HTTPException(403, message)

    product_id = product.model_dump().get('id')
    try:
        await product_service.delete_by_id(id=product_id, db_session=db_session)
        return DeleteSchema
    except Exception as exc:
        logging.exception(exc)
        hawk.send(exc)
        raise exc
