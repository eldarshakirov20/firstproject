from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    search: Optional[str] = Query(None, description="Поиск по названию или описанию"),
    db: Session = Depends(get_db)
):
    """Получить список книг с фильтрацией"""
    return crud.get_books(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        search=search
    )


@router.get("/{book_id}", response_model=schemas.BookWithCategoryResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Получить книгу по ID с категорией"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    """Создать новую книгу"""
    # Проверяем, существует ли категория
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this ID does not exist"
        )
    
    return crud.create_book(
        db,
        title=book.title,
        description=book.description or "",
        price=book.price,
        category_id=book.category_id,
        url=book.url or ""
    )


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    """Обновить книгу"""
    # Проверяем, существует ли книга
    existing = crud.get_book(db, book_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Если меняется категория, проверяем её существование
    if book_update.category_id is not None:
        category = crud.get_category(db, book_update.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this ID does not exist"
            )
    
    updated = crud.update_book(
        db,
        book_id,
        title=book_update.title,
        description=book_update.description,
        price=book_update.price,
        url=book_update.url,
        category_id=book_update.category_id
    )
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Удалить книгу"""
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return None
