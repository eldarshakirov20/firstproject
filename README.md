Book Library API

REST API для управления библиотекой книг и категорий. Проект разработан на **FastAPI** с использованием **PostgreSQL** и **SQLAlchemy**.

---

Содержание

- [Технологии]
- [Установка и запуск]
- [API Эндпоинты]
- [Примеры запросов]

---

Технологии

- **Python 3.10+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM (Object-Relational Mapping)
- **PostgreSQL** — реляционная база данных
- **Uvicorn** — ASGI сервер
- **Pydantic** — валидация данных и сериализация
- **python-dotenv** — управление переменными окружения

---

Установка и запуск

1. Клонировать репозиторий

git clone https://github.com/eldarshakirov20/firstproject.git
cd firstproject

---

2. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux / WSL
# или для Windows:
# venv\Scripts\activate

---

3. Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

---

4. Настроить базу данных PostgreSQL
Убедитесь, что PostgreSQL запущен:

bash
sudo service postgresql start  # Linux / WSL
Создайте базу данных и пользователя:

CREATE USER octagon WITH PASSWORD '12345';
CREATE DATABASE octagon_db OWNER octagon;
GRANT ALL PRIVILEGES ON DATABASE octagon_db TO octagon;
ALTER USER octagon CREATEDB;

---

5. Создать файл .env

DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345

---

6. Инициализировать базу данных
Создать таблицы и заполнить тестовыми данными:

python app/init_db.py

---

7. Запустить сервер

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

---

8. Открыть документацию
После запуска сервера откройте в браузере:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Health Check: http://localhost:8000/health

---

API Эндпоинты

Категории (/categories)

Метод	Эндпоинт	Описание	Код ответа
GET	/categories/	Получить список всех категорий	200
GET	/categories/{id}	Получить категорию по ID с книгами	200 / 404
POST	/categories/	Создать новую категорию	201 / 400
PUT	/categories/{id}	Обновить категорию	200 / 404 / 400
DELETE	/categories/{id}	Удалить категорию (каскадно удаляет книги)	204 / 404

Книги (/books)
Метод	Эндпоинт	Описание	Код ответа
GET	/books/	Получить список книг (с фильтрацией)	200
GET	/books/{id}	Получить книгу по ID с категорией	200 / 404
POST	/books/	Создать новую книгу	201 / 400
PUT	/books/{id}	Обновить книгу	200 / 404 / 400
DELETE	/books/{id}	Удалить книгу	204 / 404

Фильтрация книг (GET /books/)
Параметр	Тип	Описание
category_id	int	Фильтр по ID категории
min_price	float	Минимальная цена
max_price	float	Максимальная цена
search	string	Поиск по названию или описанию
skip	int	Пагинация (пропустить N записей)
limit	int	Пагинация (максимум записей)

---

Примеры запросов через curl

1. Создать категорию

curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Научная фантастика"}'

Ответ:

{"title": "Научная фантастика", "id": 1}

---

2. Создать книгу

curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "description": "Роман-антиутопия о тоталитарном обществе",
    "price": 1200.00,
    "category_id": 1,
    "url": "https://example.com/1984"
  }'

Ответ:

{
  "id": 1,
  "title": "1984",
  "description": "Роман-антиутопия о тоталитарном обществе",
  "price": 1200.0,
  "url": "https://example.com/1984",
  "category_id": 1,
  "created_at": "2026-07-13T16:51:25.564804",
  "updated_at": null
}

---

3. Получить все книги

curl -X GET "http://localhost:8000/books/"

---

4. Фильтр по категории

curl -X GET "http://localhost:8000/books/?category_id=1"

---

5. Фильтр по цене

curl -X GET "http://localhost:8000/books/?min_price=500&max_price=1000"

---


6. Поиск по названию

curl -X GET "http://localhost:8000/books/?search=Python"

---

7. Обновить книгу

curl -X PUT "http://localhost:8000/books/1" \
  -H "Content-Type: application/json" \

  -d '{"price": 1500.00}'

---

8. Удалить книгу

curl -X DELETE "http://localhost:8000/books/1"

---

9. Получить все категории

curl -X GET "http://localhost:8000/categories/"

---

Автор GitHub: eldarshakirov20
