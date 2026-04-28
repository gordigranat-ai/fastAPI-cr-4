import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestUserEndpoints:
    """Тесты для эндпоинтов пользователей"""
    
    def test_create_user_success(self):
        """Тест успешного создания пользователя"""
        response = client.post(
            "/users",
            json={"username": "testuser", "age": 25}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["age"] == 25
        assert "id" in data

    def test_get_existing_user(self):
        """Тест получения существующего пользователя"""
        create_resp = client.post("/users", json={"username": "testuser", "age": 25})
        user_id = create_resp.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    def test_get_nonexistent_user(self):
        """Тест получения несуществующего пользователя"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_existing_user(self):
        """Тест удаления существующего пользователя"""
        create_resp = client.post("/users", json={"username": "testuser", "age": 25})
        user_id = create_resp.json()["id"]
        
        delete_resp = client.delete(f"/users/{user_id}")
        assert delete_resp.status_code == 204
        
        get_resp = client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_user(self):
        """Тест удаления несуществующего пользователя"""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestValidation:
    """Тесты для валидации данных"""
    
    def test_valid_user_data(self):
        """Тест с корректными данными пользователя"""
        response = client.post(
            "/validate-user/",
            json={
                "username": "testuser",
                "age": 25,
                "email": "test@example.com",
                "password": "password123",
                "phone": "+1234567890"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "User data is valid"

    def test_invalid_age_too_young(self):
        """Тест с возрастом меньше 18"""
        response = client.post(
            "/validate-user/",
            json={
                "username": "testuser",
                "age": 15,
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 422

    def test_invalid_email(self):
        """Тест с некорректным email"""
        response = client.post(
            "/validate-user/",
            json={
                "username": "testuser",
                "age": 25,
                "email": "invalid-email",
                "password": "password123"
            }
        )
        assert response.status_code == 422


class TestCustomExceptions:
    """Тесты для пользовательских исключений"""
    
    def test_custom_exception_a(self):
        """Тест CustomExceptionA (статус 400)"""
        response = client.get("/custom-exception-a/")
        assert response.status_code == 400
        data = response.json()
        assert data["type"] == "CustomExceptionA"

    def test_custom_exception_b(self):
        """Тест CustomExceptionB (статус 404)"""
        response = client.get("/custom-exception-b/")
        assert response.status_code == 404
        data = response.json()
        assert data["type"] == "CustomExceptionB"