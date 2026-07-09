from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.db.models import Book, Category
from typing import Optional, List

# ============ CRUD для Category ============

def create_category(db: Session, title: str) -> Category:
    """Создание новой категории"""
    category = Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int) -> Optional[Category]:
    """Получение категории по ID"""
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_title(db: Session, title: str) -> Optional[Category]:
    """Получение категории по названию"""
    return db.query(Category).filter(Category.title == title).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    """Получение списка всех категорий с пагинацией"""
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, title: str) -> Optional[Category]:
    """Обновление категории"""
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int) -> bool:
    """Удаление категории (вместе со всеми книгами)"""
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False


# ============ CRUD для Book ============

def create_book(
    db: Session,
    title: str,
    description: str,
    price: float,
    category_id: int,
    url: str = ""
) -> Book:
    """Создание новой книги"""
    # Проверяем, существует ли категория
    category = get_category(db, category_id)
    if not category:
        raise ValueError(f"Category with id {category_id} not found")
    
    book = Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Получение книги по ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None
) -> List[Book]:
    """Получение списка книг с фильтрацией и пагинацией"""
    query = db.query(Book)
    
    # Фильтр по категории
    if category_id:
        query = query.filter(Book.category_id == category_id)
    
    # Фильтр по цене
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    
    # Поиск по названию или описанию
    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.description.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).all()

def get_books_by_category(db: Session, category_id: int) -> List[Book]:
    """Получение всех книг по категории"""
    return db.query(Book).filter(Book.category_id == category_id).all()

def update_book(
    db: Session,
    book_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    url: Optional[str] = None,
    category_id: Optional[int] = None
) -> Optional[Book]:
    """Обновление книги"""
    book = get_book(db, book_id)
    if not book:
        return None
    
    if title is not None:
        book.title = title
    if description is not None:
        book.description = description
    if price is not None:
        book.price = price
    if url is not None:
        book.url = url
    if category_id is not None:
        # Проверяем, существует ли категория
        if not get_category(db, category_id):
            raise ValueError(f"Category with id {category_id} not found")
        book.category_id = category_id
    
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int) -> bool:
    """Удаление книги"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False

def count_books(db: Session, category_id: Optional[int] = None) -> int:
    """Подсчет количества книг (опционально по категории)"""
    query = db.query(Book)
    if category_id:
        query = query.filter(Book.category_id == category_id)
    return query.count()

# ============ Дополнительные функции ============

def get_books_with_category(db: Session, skip: int = 0, limit: int = 100) -> List[dict]:
    """Получение книг с информацией о категории (JOIN)"""
    results = db.query(Book, Category.title.label("category_title")).join(Category).offset(skip).limit(limit).all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "price": book.price,
            "url": book.url,
            "category_id": book.category_id,
            "category_title": category_title
        }
        for book, category_title in results
    ]

def search_books_by_price_range(
    db: Session,
    min_price: float,
    max_price: float,
    skip: int = 0,
    limit: int = 100
) -> List[Book]:
    """Поиск книг в диапазоне цен"""
    return db.query(Book).filter(
        and_(Book.price >= min_price, Book.price <= max_price)
    ).offset(skip).limit(limit).all()
