from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.db import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True, index=True)
    
    # Связь с книгами (один ко многим)
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    url = Column(String(500), nullable=True, default="")
    
    # Внешний ключ на категорию
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    
    # Связь с категорией
    category = relationship("Category", back_populates="books")
    
    # Дата создания (опционально)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
