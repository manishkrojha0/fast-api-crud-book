from typing import List, Optional
from models.book import Book
from schemas.book import BookCreate, BookUpdate
from models.book import Book
from models.author import Author
from sqlalchemy.orm import Session
from repositories.interfaces.book_repository_interface import BookRepositoryInterface
from sqlalchemy import asc, desc
import email_validator as _email_check
from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate, User as user
import passlib.hash as _hash
import jwt as _jwt
from configs.config import settings



class BookRepository(BookRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.db.query(Book).offset(skip).limit(limit).all()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def create_book(self, book: BookCreate) -> Book:
        author = self.db.query(Author).filter(Author.name == book.author_name).first()
        if not author:
            author = Author(name=book.author_name)
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)

        book_data = book.dict(exclude={"author_name"})
        book_data["author_id"] = author.id
        db_book = Book(**book_data)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update_book(self, book_id: int, book: BookUpdate) -> Optional[Book]:
        db_book = self.get_book_by_id(book_id)
        if db_book:
            for key, value in book.dict(exclude_unset=True).items():
                setattr(db_book, key, value)
            self.db.commit()
            self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int) -> Optional[Book]:
        db_book = self.db.query(Book).filter(Book.id == book_id)
        if db_book:
            db_book.delete(synchronize_session=False)
            self.db.commit()
        return db_book.exists
    
    def filter_books_by_author_id(self, author_id: int) -> List[Book]:
        books = self.db.query(Book).filter(Book.author_id == author_id).all()
        return books
    
    def filter_books_by_price(self, price: int) -> List[Book]:
        books = self.db.query(Book).filter(Book.price == price).all()
        return books
    
    def filter_by_published_date(self, published_date: str) -> List[Book]:
        books = self.db.query(Book).filter(Book.publication_date == published_date)
        return books
    
    def search_books(self, search_terms: int, value: str) -> List[Book]:
        if search_terms not in ['author_id', 'price', 'published_date']:
            return None
        if search_terms == 'author_id':
            author_id = int(value)
            return self.filter_books_by_author_id(author_id=author_id)
        elif search_terms == 'price':
            price = int(value)
            return self.filter_books_by_price(price=price)
        else:
            published_data = value
            return self.filter_by_published_date(published_date=published_data)
    

    def sort_books(self, sort_by: str = None) -> List[Book]:
        query = self.db.query(Book) 
        # Apply sorting based on the provided field
        if sort_by:
            if sort_by == "title":
                query = query.order_by(asc(Book.title))
            elif sort_by == "author":
                query = query.order_by(asc(Book.author))
            elif sort_by == "publication_date":
                query = query.order_by(desc(Book.publication_date))
            elif sort_by == "price":
                query = query.order_by(asc(Book.price))
        
        books = query.all()
        return books
    
    # def create_user(self, user: UserCreate):
    #     try:
    #         valid = _email_check.validate_email(email=user.email)

    #         email = valid.email
    #     except _email_check.EmailNotValidError:
    #         raise HTTPException(status_code=404, detail="Please enter a valid email")

    #     user_obj = User(email=email, hashed_password=_hash.bcrypt.hash(user.password))

    #     self.db.add(user_obj)
    #     self.db.commit()
    #     self.db.refresh(user_obj)
    #     return user_obj
    
    # def get_user_by_email(self, email: str):
    #     return self.db.query(User).filter(User.email == email).first()
    
    # def authenticate_user(self, email: str, password: str):
    #     user = self.get_user_by_email(email=email)

    #     if not user:
    #         return False
        
    #     if not user.verify_password(password):
    #         return False

    #     return 
    
    # async def create_token(user: User):
    #     user_obj = user.from_orm(user)

    #     user_dict = user_obj.dict()
    #     del user_dict["date_created"]

    #     token = _jwt.encode(user_dict, settings.)

    #     return dict(access_token=token, token_type="bearer")


