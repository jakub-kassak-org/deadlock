from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()


def get_user_by_card(db: Session, card: str):
    return db.query(models.User).filter(models.User.card == card).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_base: schemas.UserBase):
    user = models.User(
        card=user_base.card,
        username=user_base.username,
        first_name=user_base.first_name,
        last_name=user_base.last_name,
        is_staff=user_base.is_staff
    )
    db.add(user)
    db.commit()
    return user


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Group).offset(offset).limit(limit).all()


def get_users_from_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not db_group:
        return None
    users_group = db.query(models.UserGroup).filter(models.UserGroup.group_id == group_id)  # [user_id, group_id] where group_id = group_id
    user_ids = set([x.user_id for x in users_group])
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    return users


def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()


def get_group_by_id(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_usergroup(db: Session, user_id: int, group_id: int):
    return db.query(models.UserGroup).filter(and_(models.UserGroup.user_id == user_id, models.UserGroup.group_id == group_id)).first()


def add_user_to_group(db: Session, user_id: int, group_id: int):
    db_usergroup = models.UserGroup(
        user_id=user_id,
        group_id=group_id
    )
    db.add(db_usergroup)
    db.commit()
    return db_usergroup


def get_rule_by_name(db: Session, name: str):
    return db.query(models.Rule).filter(models.Rule.name == name).first()


def create_rule(db: Session, rule: schemas.RuleBase):
    db_rule = models.Rule(
        name=rule.name,
        allow=rule.allow,
        ap_type_id=rule.ap_type_id,
        time_spec_id=rule.time_spec_id,
        priority=rule.priority
    )
    db.add(db_rule)
    db.commit()
    return db_rule


def get_ap_type_by_id(db: Session, ap_type_id: int):
    return db.query(models.AccessPointType).filter(models.AccessPointType.id == ap_type_id).first()


def get_time_spec_by_id(db: Session, time_spec_id: int):
    return db.query(models.TimeSpec).filter(models.TimeSpec.id == time_spec_id).first()


def get_time_spec_by_title(db: Session, time_spec_title: str):
    return db.query(models.TimeSpec).filter(models.TimeSpec.title == time_spec_title).first()


def create_time_spec(db: Session, time_spec: schemas.TimeSpecBase):
    db_time_spec = models.TimeSpec(
        title=time_spec.title,
        weekday_mask=time_spec.weekday_mask,
        time_from=time_spec.time_from,
        time_to=time_spec.time_to,
        date_from=time_spec.date_from,
        date_to=time_spec.date_to
    )
    db.add(db_time_spec)
    db.commit()
    return db_time_spec
