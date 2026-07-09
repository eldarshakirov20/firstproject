"""
Скрипт для очистки базы данных
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, engine
from app.db.models import Book, Category

def clean_database():
    db = SessionLocal()
    try:
        # Удаляем все книги
        deleted_books = db.query(Book).delete()
        print(f"Удалено книг: {deleted_books}")
        
        # Удаляем все категории
        deleted_categories = db.query(Category).delete()
        print(f"Удалено категорий: {deleted_categories}")
        
        db.commit()
        print("База данных очищена!")
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()
