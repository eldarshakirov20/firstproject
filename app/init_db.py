"""
Модуль для инициализации базы данных и заполнения тестовыми данными
"""

import sys
import os

# Добавляем корневую директорию проекта в PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, create_tables
from app.db.models import Book, Category
from app.db.crud import (
    create_category, 
    get_category_by_title,
    create_book,
    get_categories,
    get_books_by_category
)


def init_db():
    """
    Инициализация базы данных и заполнение тестовыми данными
    """
    # Создаем таблицы
    print("Создание таблиц...")
    create_tables()
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        print("Добавление тестовых данных...")
        
        # Создаем категории
        categories_data = [
            {
                "title": "Программирование",
                "books": [
                    {
                        "title": "Python. Изучаем на практике",
                        "description": "Практическое руководство по Python для начинающих и опытных разработчиков.",
                        "price": 2500.00,
                        "url": "https://example.com/python-practice"
                    },
                    {
                        "title": "Чистый код",
                        "description": "Создание, анализ и рефакторинг качественного кода.",
                        "price": 3200.00,
                        "url": "https://example.com/clean-code"
                    },
                    {
                        "title": "Алгоритмы. Построение и анализ",
                        "description": "Фундаментальное руководство по алгоритмам и структурам данных.",
                        "price": 4500.00,
                        "url": "https://example.com/algorithms"
                    },
                    {
                        "title": "JavaScript. Полное руководство",
                        "description": "Исчерпывающее руководство по современному JavaScript.",
                        "price": 3800.00,
                        "url": "https://example.com/javascript-guide"
                    }
                ]
            },
            {
                "title": "Художественная литература",
                "books": [
                    {
                        "title": "Преступление и наказание",
                        "description": "Роман Федора Достоевского о моральных и философских вопросах.",
                        "price": 850.00,
                        "url": "https://example.com/crime-and-punishment"
                    },
                    {
                        "title": "Мастер и Маргарита",
                        "description": "Великий роман Михаила Булгакова о добре и зле.",
                        "price": 920.00,
                        "url": "https://example.com/master-and-margarita"
                    },
                    {
                        "title": "Война и мир",
                        "description": "Эпический роман Льва Толстого о жизни русского общества.",
                        "price": 1500.00,
                        "url": "https://example.com/war-and-peace"
                    }
                ]
            }
        ]
        
        # Добавляем категории и книги
        for category_data in categories_data:
            category_title = category_data["title"]
            print(f"  Добавление категории: {category_title}")
            
            # Проверяем, не существует ли уже такая категория
            existing_category = get_category_by_title(db, category_title)
            if existing_category:
                print(f"    Категория '{category_title}' уже существует, пропускаем")
                category = existing_category
            else:
                category = create_category(db, category_title)
                print(f"    Категория '{category_title}' создана (ID: {category.id})")
            
            # Добавляем книги с проверкой на дубликаты
            for book_data in category_data["books"]:
                print(f"      Добавление книги: {book_data['title']}")
                
                # Проверяем, существует ли уже такая книга в этой категории
                existing_book = db.query(Book).filter(
                    Book.title == book_data["title"],
                    Book.category_id == category.id
                ).first()
                
                if existing_book:
                    print(f"        Книга '{book_data['title']}' уже существует, пропускаем")
                    continue
                
                try:
                    book = create_book(
                        db=db,
                        title=book_data["title"],
                        description=book_data["description"],
                        price=book_data["price"],
                        category_id=category.id,
                        url=book_data["url"]
                    )
                    print(f"        Книга '{book.title}' добавлена (ID: {book.id})")
                except Exception as e:
                    print(f"        Ошибка при добавлении книги: {e}")
        
        print("База данных успешно инициализирована!")
        
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def show_data():
    """
    Функция для отображения данных из базы данных
    """
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("ДАННЫЕ ИЗ БАЗЫ ДАННЫХ")
        print("="*60 + "\n")
        
        # Получаем все категории
        categories = get_categories(db)
        
        if not categories:
            print("В базе данных нет категорий")
            return
        
        print(f"Всего категорий: {len(categories)}")
        print("-" * 60)
        
        for category in categories:
            print(f"\nКАТЕГОРИЯ: {category.title} (ID: {category.id})")
            print("-" * 40)
            
            # Получаем книги для этой категории
            books = get_books_by_category(db, category.id)
            
            if not books:
                print("  В этой категории нет книг")
                continue
            
            print(f"  Книг: {len(books)}")
            for book in books:
                print(f"\n    Название: {book.title}")
                print(f"    Описание: {book.description[:80]}..." if len(book.description) > 80 else f"    Описание: {book.description}")
                print(f"    Цена: {book.price:.2f} руб.")
                print(f"    URL: {book.url or 'Нет ссылки'}")
                print("    " + "-" * 20)
        
        print("\n" + "="*60)
        print("Отображение данных завершено")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("ЗАПУСК ИНИЦИАЛИЗАЦИИ БАЗЫ ДАННЫХ")
    print("="*60 + "\n")
    
    # Инициализируем базу данных
    init_db()
    
    # Показываем данные
    show_data()
