import pytest
from src.depends.products import product_service
from src.depends.orders import order_service
from src.dto.orders import OrderDTO, OrderItemDTO
from src.dto.users import UserDTO
from src.schemas.orders import OrderSchema
from src.schemas.products import ProductSchema
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import load_data
from src.dto.products import ProductDTO


test_data_products = load_data('products.json')
test_data_orders = load_data('orders.json')

@pytest.mark.asyncio(loop_scope="session")
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.content == b"<h1>FastAPI: STORAGE AREA MANAGEMENT APPLICATION</h1>"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(db_session: AsyncSession):
    product = ProductDTO(**test_data_products['input_data_create'])
    result = await product_service.create(product, db_session)
    res = ProductSchema.model_validate(result).model_dump()
    assert res == test_data_products['create_example']


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_bad_price(async_client: AsyncClient, db_session: AsyncSession):
    data = test_data_products['input_data_create_bad_price']
    response = await async_client.post("/products/", params=data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be greater than or equal to 0'


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_product(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [test_data_products['create_example']]
    results = await product_service.get_all(db_session)
    res = [ProductSchema.model_validate(result).model_dump() for result in results]
    assert res == [test_data_products['create_example']]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_id(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/products/1")
    assert response.status_code == 200
    result = await product_service.get_by_id(1, db_session)
    res = ProductSchema.model_validate(result).model_dump()
    assert res == test_data_products['create_example']


@pytest.mark.asyncio(loop_scope="session")
async def test_create_order(async_client: AsyncClient, db_session: AsyncSession):
    test_data = test_data_orders['input_data_create']
    orderitems = [OrderItemDTO(**item_data) for item_data in test_data['orderitems']]
    order_dto = OrderDTO(status=test_data['status'], user_id=test_data['user_id'], orderitems=orderitems)
    result = await order_service.create(order_dto, db_session)
    res = OrderSchema.model_validate(result).model_dump()
    assert res == test_data_orders['create_example']


@pytest.mark.asyncio(loop_scope="session")
async def test_create_order_bad_quantity(async_client: AsyncClient, db_session: AsyncSession):
    data = test_data_orders['input_bad_quantity']
    response = await async_client.post("/orders/", params=data["params"], json=data['orderitems'])
    assert response.status_code == 422
    assert response.json()['detail'] == 'Quantity product with id: 1 exceeds stock availability'
