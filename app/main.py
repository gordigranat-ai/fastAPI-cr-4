from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from itertools import count
from threading import Lock
from typing import Dict

from app.database import get_db, engine, Base
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, User, UserIn, UserOut
from app.exceptions import CustomExceptionA, CustomExceptionB

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Контрольная работа №4", version="1.0.0")

db_users: Dict[int, dict] = {}
_id_seq = count(start=1) 
_id_lock = Lock()  

def next_user_id() -> int:
    """Генерирует следующий ID пользователя (потокобезопасно)"""
    with _id_lock:
        return next(_id_seq)

# Обработчики исключений 

@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    """Обработчик для CustomExceptionA"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "CustomExceptionA"
        }
    )

@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    """Обработчик для CustomExceptionB"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "type": "CustomExceptionB"
        }
    )

#  Эндпоинты для работы с продуктами (БД) 

@app.post("/products/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Создание нового продукта
    """
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получение продукта по ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise CustomExceptionB(detail=f"Product with id {product_id} not found")
    return product

@app.get("/products/")
def list_products(db: Session = Depends(get_db)):
    """
    Получение списка всех продуктов
    """
    products = db.query(Product).all()
    if not products:
        raise CustomExceptionA(detail="No products found in database")
    return products

#  Эндпоинты для работы с пользователями (in-memory) 

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    """
    Создание нового пользователя (в памяти)
    """
    user_id = next_user_id()
    db_users[user_id] = user.model_dump()
    return {"id": user_id, **db_users[user_id]}

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """
    Получение пользователя по ID
    """
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db_users[user_id]}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    """
    Удаление пользователя
    """
    if db_users.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)

# Эндпоинты для демонстрации валидации и исключений 

@app.post("/validate-user/")
def validate_user(user: User):
    """
    Валидация данных пользователя
    """
    return {
        "message": "User data is valid",
        "user": user.model_dump()
    }

@app.get("/custom-exception-a/")
def trigger_exception_a():
    """
    Вызов CustomExceptionA (Bad Request)
    """
    raise CustomExceptionA(detail="This is a custom error A - условие не выполнено")

@app.get("/custom-exception-b/")
def trigger_exception_b():
    """
    Вызов CustomExceptionB (Not Found)
    """
    raise CustomExceptionB(detail="Custom resource not found")