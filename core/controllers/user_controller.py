from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.user import User, UserCreate, LoginUser
from repositories.user_repository import UserRepository
from databases.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post('/create_user', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.create_user(user=user)
    if not user:
        raise HTTPException(status_code=400, detail="Please provide valid body")
    return user

@router.post('/login')
def login(auth_details: LoginUser, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    result = repository.create_token(auth_details)
    if not result:
        raise HTTPException(status_code=400, detail="Auth details are invalid")
    return result

@router.get('/get_user/{email_id}', response_model=User)
def get_user(email_id: str, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    user = repository.get_user_by_email(email_id)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email id or user is not present with this email id")
    return user

