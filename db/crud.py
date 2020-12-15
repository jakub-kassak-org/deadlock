from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_card(db: Session, card: str):
    return db.query(models.User).filter(models.User.card == card).first()


def add_group(db: Session, group: schemas.Group):
    db_group = models.Group(title=group.title)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Group).offset(offset).limit(limit).all()


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()
