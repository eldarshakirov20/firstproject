"""
FastAPI приложение для управления библиотекой книг
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books_router, categories_router

# Отключаем логи SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Создаем приложение FastAPI
app = FastAPI(
    title="Book Library API",
    description="API для управления библиотекой книг и категорий",
    version="1.0.0"
)

# Настраиваем CORS (для доступа из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(books_router)
app.include_router(categories_router)


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "Book Library API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Проверка работоспособности"""
    return {"status": "ok"}
