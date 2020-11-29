from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import models, crud
from db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def root():
    return {'message': 'response'}


@app.get('/users')
async def get_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users
