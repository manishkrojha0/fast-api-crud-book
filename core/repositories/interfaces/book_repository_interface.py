from abc import ABC, abstractmethod
from typing import List, Optional

from schemas.book import BookCreate, BookUpdate
from models.book import Book



class BookRepositoryInterface(ABC):
    @abstractmethod
    def get_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    def create_book(self, book: BookCreate) -> Book:
        pass

    @abstractmethod
    def update_book(self, book_id: int, book: BookUpdate) -> Optional[Book]:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    def filter_books_by_author_id(self, author_id: int) -> List[Book]:
        pass

