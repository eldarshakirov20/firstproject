from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# === Схемы для Category ===

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True


# === Схемы для Book ===

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    url: Optional[str] = None
    category_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    url: Optional[str] = None
    category_id: Optional[int] = None

class BookResponse(BookBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# === Расширенные ответы с вложенными данными ===

class BookWithCategoryResponse(BookResponse):
    category: Optional[CategoryResponse] = None

class CategoryWithBooksResponse(CategoryResponse):
    books: list[BookResponse] = []
