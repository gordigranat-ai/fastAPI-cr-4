import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from app.main import app, db_users

fake = Faker()

@pytest.fixture(autouse=True)
def clear_storage():
    """Очищает in-memory хранилище перед каждым тестом"""
    db_users.clear()
    yield
    db_users.clear()

@pytest.mark.asyncio
async def test_create_user_async():
    """Тест успешного создания пользователя с данными от Faker"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80)
        }
        response = await client.post("/users", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["age"] == user_data["age"]
        assert "id" in data

@pytest.mark.asyncio
async def test_get_existing_user_async():
    """Тест получения существующего пользователя"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80)
        }
        create_resp = await client.post("/users", json=user_data)
        user_id = create_resp.json()["id"]
        
        get_resp = await client.get(f"/users/{user_id}")
        assert get_resp.status_code == 200

@pytest.mark.asyncio
async def test_get_nonexistent_user_async():
    """Тест получения несуществующего пользователя"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/users/9999")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_async():
    """Тест удаления существующего пользователя"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_data = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=80)
        }
        create_resp = await client.post("/users", json=user_data)
        user_id = create_resp.json()["id"]
        
        delete_resp = await client.delete(f"/users/{user_id}")
        assert delete_resp.status_code == 204
        
        get_resp = await client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_user_async():
    """Тест удаления несуществующего пользователя"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/users/9999")
        assert response.status_code == 404