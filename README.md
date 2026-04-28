# Контрольная работа №4

Технологии разработки серверных приложений. FastAPI + Alembic + Pytest.

## Описание проекта

Приложение FastAPI с миграциями базы данных Alembic, пользовательской обработкой ошибок, валидацией данных и модульными тестами.

### Выполненные задания

- Задание 9.1: Настройка Alembic, создание модели Product, миграции базы данных
- Задание 10.1: Пользовательские исключения CustomExceptionA и CustomExceptionB
- Задание 10.2: Валидация данных с Pydantic, обработка ошибок валидации
- Задание 11.1: Модульные тесты с pytest и TestClient
- Задание 11.2: Асинхронные тесты с httpx, Faker и изоляцией состояния

## Установка и запуск

### 1. Клонирование репозитория

git clone <url-репозитория>
cd fastapi-cr4

### 2. Создание виртуального окружения

Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Настройка переменных окружения

Windows:
copy .env.example .env

Linux/Mac:
cp .env.example .env

### 5. Инициализация и применение миграций

python -m alembic init alembic
python -m alembic revision --autogenerate -m "Initial migration"
python -m alembic upgrade head

### 6. Запуск приложения

python -m uvicorn app.main:app --reload

Приложение доступно по адресу: http://localhost:8000
Документация API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Проверка функциональности

### Создание продукта

curl -X POST http://localhost:8000/products/ -H "Content-Type: application/json" -d "{\"title\":\"Ноутбук\",\"price\":50000,\"count\":10,\"description\":\"Игровой ноутбук\"}"

### Получение списка продуктов

curl http://localhost:8000/products/

### Получение продукта по ID

curl http://localhost:8000/products/1

### Создание пользователя

curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d "{\"username\":\"Иван\",\"age\":25}"

### Получение пользователя

curl http://localhost:8000/users/1

### Удаление пользователя

curl -X DELETE http://localhost:8000/users/1

### Валидация данных

curl -X POST http://localhost:8000/validate-user/ -H "Content-Type: application/json" -d "{\"username\":\"user\",\"age\":25,\"email\":\"test@example.com\",\"password\":\"password123\"}"

### Проверка исключений

curl http://localhost:8000/custom-exception-a/
curl http://localhost:8000/custom-exception-b/

## Тестирование

### Запуск всех тестов

python -m pytest -v

### Запуск обычных тестов

python -m pytest tests/test_main.py -v

### Запуск асинхронных тестов

python -m pytest tests/test_async.py -v

## Миграции базы данных

### Проверка текущей версии

python -m alembic current

### Просмотр истории миграций

python -m alembic history

## Переменные окружения

DATABASE_URL - URL подключения к БД (по умолчанию sqlite:///./products.db)

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Pytest
- HTTPX
- Faker

## Примечания

- Приложение использует SQLite по умолчанию
- Все тесты изолированы и не влияют друг на друга
- In-memory хранилище очищается перед каждым тестом
- Файл .env добавлен в .gitignore и не публикуется
