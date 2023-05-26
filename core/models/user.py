from sqlalchemy import Column, Integer, String, DateTime
from databases.database import Base
import datetime
import sqlalchemy.orm as _orm
import passlib.hash as _hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    
