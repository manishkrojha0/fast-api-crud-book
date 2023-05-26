"""Model file for author"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from databases.database import Base


class Author(Base):
    """Model class for Author"""

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    books = relationship("Book", back_populates="author", cascade="all, delete")