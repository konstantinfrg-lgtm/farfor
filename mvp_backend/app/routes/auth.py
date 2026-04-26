from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import Token, UserCreate, UserLogin, UserOut
from app.services.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=400, detail='Email уже используется')
    if db.scalar(select(User).where(User.username == payload.username)):
        raise HTTPException(status_code=400, detail='Имя пользователя уже занято')

    user = User(email=payload.email, username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    return Token(access_token=token, user=UserOut.model_validate(user))


@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный логин или пароль')

    token = create_access_token(str(user.id))
    return Token(access_token=token, user=UserOut.model_validate(user))
