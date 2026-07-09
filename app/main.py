"""
Главный модуль приложения
"""

import sys
import os
import logging

# Отключить логи SQLAlchemy (добавьте эти строки)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

# Добавляем корневую директорию проекта в PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db.models import Book, Category
from app.db.crud import (
    get_categories,
    get_books_by_category,
    get_books,
    search_books_by_price_range
)


def main():
    """
    Главная функция для отображения данных из базы данных
    """
    db = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("БИБЛИОТЕКА КНИГ")
        print("="*70 + "\n")
        
        # Получаем все категории
        categories = get_categories(db)
        
        if not categories:
            print("В базе данных нет категорий")
            print("Запустите app/init_db.py для инициализации базы данных.")
            return
        
        # Считаем общее количество книг
        total_books = 0
        
        print(f"Всего категорий: {len(categories)}")
        print("-" * 70)
        
        for category in categories:
            books = get_books_by_category(db, category.id)
            total_books += len(books)
            
            print(f"\nКАТЕГОРИЯ: {category.title.upper()} (ID: {category.id})")
            print("" + "-" * 50)
            
            if not books:
                print("  В этой категории нет книг")
                continue
            
            print(f"  Книг в категории: {len(books)}")
            print("")
            
            for i, book in enumerate(books, 1):
                print(f"  {i}. {book.title}")
                print(f"     Цена: {book.price:.2f} руб.")
                if book.description:
                    desc = book.description[:100] + "..." if len(book.description) > 100 else book.description
                    print(f"     Описание: {desc}")
                if book.url:
                    print(f"     Ссылка: {book.url}")
                print("     " + "-" * 40)
        
        print("\n" + "="*70)
        print(f"ИТОГО: {total_books} книг в {len(categories)} категориях")
        print("="*70 + "\n")
        
        # Дополнительно: поиск книг по цене
        print("ПОИСК КНИГ В ДИАПАЗОНЕ ЦЕН (500 - 1000 руб.)")
        print("-" * 50)
        
        cheap_books = search_books_by_price_range(db, 500, 1000)
        if cheap_books:
            for book in cheap_books:
                print(f"  {book.title} - {book.price:.2f} руб.")
        else:
            print("  Нет книг в указанном диапазоне цен")
        
        print("\n" + "="*70)
        print("Программа успешно завершена")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
