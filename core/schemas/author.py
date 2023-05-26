from pydantic import BaseModel
from typing import List
from models.book import Book

class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book]

    class Config:
        orm_mode = True