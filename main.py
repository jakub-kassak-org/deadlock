from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import models, crud
from db.database import SessionLocal, engine
from db.schemas import User, UserBase, Token, TokenData

from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta

import exceptions

import logging
logger = logging.getLogger(__name__)


app = FastAPI()


# to get a string like this run:
# openssl rand -hex 32
# It's for signing JWT tokens
SECRET_KEY = "c16642a0b550d80bf38c54b62280da0ff5405526a2e50eea708f6cce2f3eca27"  # TODO change when deploying
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Send username, password to ./token/


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username)
    if not user:
        return False
    if not user.is_staff or user.disabled:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db, username: str):
    user = crud.get_user_by_username(db, username)
    if user:
        return user
    return None


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def is_user_staff(user: User):
    return user and user.is_staff


@app.get('/')
async def root():
    return {'message': 'response'}


@app.get('/users')
async def get_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not is_user_staff(current_user):
        raise exceptions.NOT_ALLOWED
    users = crud.get_users(db)
    return {'users': users}


@app.post("/users", response_model=User)
def create_user(user: UserBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not is_user_staff(current_user):
        raise exceptions.NOT_ALLOWED
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_card(db=db, card=user.card)
    if db_user:
        raise HTTPException(status_code=400, detail="Card already registered for different user")
    return crud.create_user(db=db, user_base=user)


# TODO implement this
@app.get("/groups")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

