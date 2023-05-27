from typing import List
from sqlalchemy.orm import Session
from schemas.user import UserCreate, LoginUser
import email_validator as _email_check
from fastapi import HTTPException
from models.user import User
import passlib.hash as _hash
from auth.auth_handler import AuthHandler
import schemas as _schemas
from auth.jwt_auth_handler import signJWT


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.auth_handler = AuthHandler()
    
    def create_user(self, user: UserCreate) -> User:
        try:
            valid = _email_check.validate_email(email=user.email)
            email = valid.email
            user_obj = self.db.query(User).filter(User.email == email).first()
            if user_obj:
                raise HTTPException(status_code=400, detail="User exists")

        except _email_check.EmailNotValidError:
            raise HTTPException(status_code=404, detail="Please enter a valid email")
        

        hashed_password = self.auth_handler.get_password_hash(password=user.password)

        user = user.dict()
        del user['password']
        user['hashed_password'] = hashed_password

        user_obj = User(**user)

        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj    
    
    def get_user_by_email(self, email: str):
        try:
            user_obj = self.db.query(User).filter(User.email == email).first()
        except User.DoesNotExist:
           raise HTTPException(status_code=400, detail="Email is not registered")

        return user_obj
    
    def create_token(self, user: LoginUser):
        user_obj = self.db.query(User).filter(User.email == user.email).first()
        return signJWT(user.email, user_obj.role)
    
    def login_user(self, user: LoginUser):
        is_authenticated = self.authenticate_user(email=user.email, password=user.password)
        if not is_authenticated:
            raise HTTPException(status_code=400, detail="Password is incorrect.")


    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email=email)

        if not user:
            return False
        
        if not self.auth_handler.verify_password(password, user.hashed_password):
            return False

        return True