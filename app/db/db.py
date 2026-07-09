import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем параметры подключения из .env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'octagon_db')
DB_USER = os.getenv('DB_USER', 'octagon')
DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')

# Создаем URL для подключения к PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем engine для подключения к БД
engine = create_engine(
    DATABASE_URL,
    echo=False,  # <- Изменено с True на False
    pool_size=5,
    max_overflow=10
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для создания таблиц
def create_tables():
    Base.metadata.create_all(bind=engine)

# Функция для удаления таблиц (осторожно!)
def drop_tables():
    Base.metadata.drop_all(bind=engine)
