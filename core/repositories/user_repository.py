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
        return self.db.query(User).filter(User.email == email).first()
    
    def create_token(self, user: LoginUser):
        # user_obj = LoginUser.from_orm(user)
        # user_dict = user_obj.dict()
        # is_authenticated_user = self.authenticate_user(user_obj.email, user_obj.password,
        #                                                 self.auth_handler.get_password_hash(user_obj.password
        # ))
        # if not is_authenticated_user:
        #     raise HTTPException(status_code=400, detail="Invalid credentials")

        # token = self.auth_handler.encode_token(user_dict)

        # return dict(access_token=token, token_type="bearer")
        return signJWT(user.email)
    

    def authenticate_user(self, email: str, password: str, hashed_password: str):
        user = self.get_user_by_email(email=email)

        if not user:
            return False
        
        if not self.auth_handler.verify_password(password, hashed_password):
            return False

        return True