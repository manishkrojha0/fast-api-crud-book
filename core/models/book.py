"""Model file for books"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index, Date
from sqlalchemy.orm import relationship
from databases.database import Base


class Book(Base):
    """Model class for book."""

    __tablename__ = 'books'

    # here adding indexing to the book id.
    __table_args__ = (
        Index('ix_books_id', 'id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    author_id = Column(Integer, ForeignKey('authors.id'))
    description = Column(String(500), nullable=True, default='')
    publication_date = Column(String, nullable=True, default='')
    price = Column(Integer)

    author = relationship("Author", back_populates="books", cascade="all")