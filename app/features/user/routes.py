from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.hashing import Hash
from app.core.database import get_db
from .schemas import ShowUser
from app.features.user.schemas import CreateUser
from app.features.user.models import User

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post('/create', response_model=ShowUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = Hash.bcrypt(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/all", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return User.get_by_id(db, user_id)


