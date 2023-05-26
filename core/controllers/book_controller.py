from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.book import BookCreate, BookUpdate, BookInResponse, Book
from repositories.book_repository import BookRepository
from databases.database import get_db
from models.user import User
from schemas.user import User
import fastapi.security as _security
import sqlalchemy.orm as _orm
from auth.auth_handler import AuthHandler
from auth.auth_bearer import JWTBearer



router = APIRouter()
auth_handler = AuthHandler()

def has_role(required_role: str = None):
    def _has_role(token: str = Depends(auth_handler.oauth2_scheme)):
        user = auth_handler.decode_token(token)
        if not user or user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return _has_role


@router.get("/books", dependencies=[Depends(JWTBearer())], response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    books = repository.get_books(skip=skip, limit=limit)
    return books


@router.get("/books/{book_id}", dependencies=[Depends(JWTBearer())], response_model=Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    book = repository.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books", status_code=201,dependencies=[Depends(JWTBearer()), Depends(has_role('admin'))] , response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    created_book = repository.create_book(book)
    return created_book


@router.put("/books/{book_id}",dependencies=[Depends(JWTBearer()), Depends(has_role('admin'))], response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    updated_book = repository.update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/books/{book_id}",dependencies=[Depends(JWTBearer()), Depends(has_role('admin'))], status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    deleted_book = repository.delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book


# adding filtering logic and endpoints
@router.get('books/{author_id}',dependencies=[Depends(JWTBearer())], status_code=200)
def filter_by_author_id(author_id: int, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    filtered_books = repository.filter_books_by_author_id(author_id=author_id)
    if not filtered_books:
        raise HTTPException(status_code=400, detail="Please Try with the valid author id.")

    return filtered_books


@router.get('books/{search_terms}/{value}', status_code=200,dependencies=[Depends(JWTBearer())], response_model=List[Book])
def search_books(search_terms: str, value: str, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    filtered_books = repository.search_books(search_terms=search_terms, value=value)
    if not filtered_books:
        raise HTTPException(status_code=400, detail="Please search with valid search terms")

    return filtered_books


@router.get('/books/{sort_by}', status_code=200,dependencies=[Depends(JWTBearer())], response_model=List[Book])
def sort_books(sort_by: str, db: Session = Depends(get_db)):
    repository = BookRepository(db)
    ordered_books = repository.sort_books(sort_by=sort_by)
    if not ordered_books:
        raise HTTPException(status_code=400, detail="Please sort with valid sorting terms")

    return ordered_books
