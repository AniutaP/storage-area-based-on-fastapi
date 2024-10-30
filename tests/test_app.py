import pytest
from src.depends.depends import product_service
from src.schemas.products import ProductSchema
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import load_data
from src.dto.products import ProductDTO


test_data = load_data('product.json')


@pytest.mark.asyncio(loop_scope="session")
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.content == b"<h2>FastApi: STORAGE AREA MANAGEMENT APPLICATION</h2>"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(db_session: AsyncSession):
    product = ProductDTO(**test_data['input_data'])
    result = await product_service.create(product, db_session)
    res = ProductSchema.model_validate(result).model_dump()
    assert res == test_data['create_example']


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_product(async_client, db_session: AsyncSession):
    response = await async_client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [test_data['create_example']]

    results = await product_service.get_all(db_session)
    res = [ProductSchema.model_validate(result).model_dump() for result in results]
    assert res == [test_data['create_example']]