from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProductBase(BaseModel):
    """Базовая схема продукта"""
    title: str
    price: float
    count: int
    description: str

class ProductCreate(ProductBase):
    """Схема для создания продукта"""
    pass

class ProductResponse(ProductBase):
    """Схема для ответа с продуктом"""
    id: int
    model_config = {"from_attributes": True}

class User(BaseModel):
    """Схема для валидации пользователя"""
    username: str
    age: int = Field(gt=18)
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

class UserIn(BaseModel):
    """Схема для входящих данных пользователя"""
    username: str
    age: int

class UserOut(BaseModel):
    """Схема для ответа с пользователем"""
    id: int
    username: str
    age: int

class ErrorResponse(BaseModel):
    """Схема для ответа с ошибкой"""
    detail: str
    type: str