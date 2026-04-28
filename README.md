Вот готовый `README.md` в соответствии со всеми требованиями:

```markdown
# Контрольная работа №4

Технологии разработки серверных приложений. FastAPI + Alembic + Pytest.

## Описание проекта

Приложение FastAPI с миграциями базы данных Alembic, пользовательской обработкой ошибок, валидацией данных и модульными тестами.

### Выполненные задания

- **Задание 9.1** — Настройка Alembic, создание модели Product, миграции базы данных
- **Задание 10.1** — Пользовательские исключения CustomExceptionA и CustomExceptionB
- **Задание 10.2** — Валидация данных с Pydantic, обработка ошибок валидации
- **Задание 11.1** — Модульные тесты с pytest и TestClient
- **Задание 11.2** — Асинхронные тесты с httpx, Faker и изоляцией состояния

## Структура проекта

```
├── app/                    # Исходный код приложения
│   ├── __init__.py
│   ├── main.py            # Точка входа, эндпоинты API
│   ├── models.py          # Модели SQLAlchemy
│   ├── database.py        # Подключение к БД
│   ├── schemas.py         # Pydantic схемы валидации
│   └── exceptions.py      # Пользовательские исключения
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_main.py        # Обычные тесты (TestClient)
│   └── test_async.py      # Асинхронные тесты (httpx + Faker)
├── alembic/                # Миграции базы данных
│   ├── versions/           # Файлы миграций
│   ├── env.py             # Конфигурация Alembic
│   └── script.py.mako     # Шаблон миграции
├── alembic.ini             # Настройки Alembic
├── requirements.txt        # Зависимости проекта
├── .env.example           # Пример переменных окружения
├── .gitignore             # Исключения Git
└── README.md              # Документация
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd fastapi-cr4
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

По умолчанию используется SQLite (`sqlite:///./products.db`).

### 5. Инициализация и применение миграций

```bash
# Инициализация Alembic (если папка отсутствует)
python -m alembic init alembic

# Создание миграции
python -m alembic revision --autogenerate -m "Initial migration"

# Применение миграции
python -m alembic upgrade head
```

### 6. Запуск приложения

```bash
python -m uvicorn app.main:app --reload
```

Приложение доступно по адресу: **http://localhost:8000**

Документация API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Проверка функциональности

### Работа с продуктами

**Создание продукта:**
```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Ноутбук","price":50000,"count":10,"description":"Игровой ноутбук"}'
```

**Получение списка продуктов:**
```bash
curl http://localhost:8000/products/
```

**Получение продукта по ID:**
```bash
curl http://localhost:8000/products/1
```

**Получение несуществующего продукта (ошибка 404):**
```bash
curl http://localhost:8000/products/999
```

### Работа с пользователями (in-memory)

**Создание пользователя:**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"Иван","age":25}'
```

**Получение пользователя:**
```bash
curl http://localhost:8000/users/1
```

**Удаление пользователя:**
```bash
curl -X DELETE http://localhost:8000/users/1
```

### Валидация данных

**Валидные данные:**
```bash
curl -X POST http://localhost:8000/validate-user/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","age":25,"email":"test@example.com","password":"password123"}'
```

**Невалидный возраст (ошибка 422):**
```bash
curl -X POST http://localhost:8000/validate-user/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","age":15,"email":"test@example.com","password":"password123"}'
```

**Невалидный email (ошибка 422):**
```bash
curl -X POST http://localhost:8000/validate-user/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","age":25,"email":"invalid-email","password":"password123"}'
```

### Пользовательские исключения

**CustomExceptionA (400 Bad Request):**
```bash
curl http://localhost:8000/custom-exception-a/
```

**CustomExceptionB (404 Not Found):**
```bash
curl http://localhost:8000/custom-exception-b/
```

## Тестирование

### Запуск всех тестов

```bash
python -m pytest -v
```

### Запуск обычных тестов

```bash
python -m pytest tests/test_main.py -v
```

### Запуск асинхронных тестов

```bash
python -m pytest tests/test_async.py -v
```

### Запуск конкретного теста

```bash
python -m pytest tests/test_main.py::TestUserEndpoints::test_create_user_success -v
```

### Ожидаемый результат

Все тесты должны завершиться со статусом **PASSED**:

```
tests/test_main.py::TestUserEndpoints::test_create_user_success PASSED
tests/test_main.py::TestUserEndpoints::test_get_existing_user PASSED
tests/test_main.py::TestUserEndpoints::test_get_nonexistent_user PASSED
tests/test_main.py::TestUserEndpoints::test_delete_existing_user PASSED
tests/test_main.py::TestUserEndpoints::test_delete_nonexistent_user PASSED
tests/test_main.py::TestValidation::test_valid_user_data PASSED
tests/test_main.py::TestValidation::test_invalid_age_too_young PASSED
tests/test_main.py::TestValidation::test_invalid_email PASSED
tests/test_main.py::TestCustomExceptions::test_custom_exception_a PASSED
tests/test_main.py::TestCustomExceptions::test_custom_exception_b PASSED
tests/test_async.py::test_create_user_async PASSED
tests/test_async.py::test_get_existing_user_async PASSED
tests/test_async.py::test_get_nonexistent_user_async PASSED
tests/test_async.py::test_delete_user_async PASSED
tests/test_async.py::test_delete_nonexistent_user_async PASSED
```

## Миграции базы данных

**Проверка текущей версии:**
```bash
python -m alembic current
```

**Просмотр истории миграций:**
```bash
python -m alembic history
```

**Откат миграции:**
```bash
python -m alembic downgrade -1
```

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `DATABASE_URL` | URL подключения к БД | `sqlite:///./products.db` |

## Технологии

- **Python 3.12+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции базы данных
- **Pydantic** — валидация данных
- **Pytest** — тестирование
- **HTTPX** — асинхронный HTTP-клиент для тестов
- **Faker** — генерация тестовых данных

## Примечания

- Приложение использует SQLite по умолчанию, не требует установки дополнительных СУБД
- Все тесты изолированы и не влияют друг на друга
- In-memory хранилище очищается перед каждым тестом
- Файл `.env` добавлен в `.gitignore` и не публикуется
- Реальные секреты не хранятся в репозитории
```