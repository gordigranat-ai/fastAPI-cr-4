import pytest
from app.main import db_users

@pytest.fixture(autouse=True)
def clear_storage():
    """
    Очищает in-memory хранилище перед каждым тестом
    """
    db_users.clear()
    yield
    db_users.clear()