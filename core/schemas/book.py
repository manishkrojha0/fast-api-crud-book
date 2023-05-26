from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    publication_date: str | None
    description: Optional[str]
    price: int | None


class BookCreate(BookBase):
    author_name: str


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class BookPagination(BaseModel):
    total: int
    items: List[Book]

class BookInResponse(BaseModel):
    title: str
    description: Optional[str]
    author_name: str

