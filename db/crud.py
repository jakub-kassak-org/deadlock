from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Tuple, Optional, Set
import logging

from . import models, schemas

root_logger = logging.getLogger('root')
runtime_logger = logging.getLogger('runtime')


def get_users(db: Session, offset: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(offset).limit(limit).all()


def get_user_by_card(db: Session, card: str) -> models.User:
    return db.query(models.User).filter(models.User.card == card).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user_base: schemas.UserBase) -> models.User:
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


def delete_user(db: Session, user_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def update_user(db: Session, user_id: int, data: schemas.UserBase) -> Tuple[bool, str]:
    try:
        db.query(models.User).filter(models.User.id == user_id).update({
            'card': data.card,
            'username': data.username,
            'first_name': data.first_name,
            'last_name': data.last_name,
            'is_staff': data.is_staff
        })
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def create_group(db: Session, group: schemas.GroupCreate) -> models.Group:
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.Group).filter(models.Group.id == group_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def update_group(db: Session, group_id: int, data: schemas.GroupCreate) -> Tuple[bool, str]:
    try:
        db.query(models.Group).filter(models.Group.id == group_id).update({
            'name': data.name,
        })
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def get_groups(db: Session, offset: int = 0, limit: int = 100) -> List[models.Group]:
    return db.query(models.Group).offset(offset).limit(limit).all()


def get_users_from_group(db: Session, group_id: int) -> Optional[List[models.User]]:
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not db_group:
        return None
    users_group = db.query(models.UserGroup).filter(models.UserGroup.group_id == group_id)  # [user_id, group_id] where group_id = group_id
    user_ids = set([x.user_id for x in users_group])
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    return users


def get_group_by_name(db: Session, name: str) -> models.Group:
    return db.query(models.Group).filter(models.Group.name == name).first()


def get_group_by_id(db: Session, group_id: int) -> models.Group:
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups_ids_by_card(db: Session, card: str) -> Set[int]:
    user = db.query(models.User).filter(models.User.card == card).first()
    usergroups = db.query(models.UserGroup).filter(models.UserGroup.user_id == user.id)
    return set([x.group_id for x in usergroups])


def get_groups_by_user_id(db: Session, user_id: int) -> List[models.Group]:
    usergroups = db.query(models.UserGroup).filter(models.UserGroup.user_id == user_id)
    group_ids = set([x.group_id for x in usergroups])
    groups = db.query(models.Group).filter(models.Group.id.in_(group_ids)).all()
    return groups


def set_group_rules_ids(db: Session, group_id: int, rules_ids: List[int]) -> Tuple[bool, str]:
    try:
        db.query(models.GroupRule).filter(models.GroupRule.group_id == group_id).delete()
        for rule_id in rules_ids:
            new_gr = models.GroupRule(
                group_id=group_id,
                rule_id=rule_id
            )
            db.add(new_gr)
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, 'Error on the database side'
    return True, 'success'


def get_usergroup(db: Session, user_id: int, group_id: int) -> models.UserGroup:
    return db.query(models.UserGroup).filter(and_(models.UserGroup.user_id == user_id, models.UserGroup.group_id == group_id)).first()


def add_user_to_group(db: Session, user_id: int, group_id: int) -> models.UserGroup:
    db_usergroup = models.UserGroup(
        user_id=user_id,
        group_id=group_id
    )
    db.add(db_usergroup)
    db.commit()
    return db_usergroup


def delete_user_from_group(db: Session, usergroup_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.UserGroup).filter(models.UserGroup.id == usergroup_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def get_rule_by_name(db: Session, name: str) -> models.Rule:
    return db.query(models.Rule).filter(models.Rule.name == name).first()


def get_rule_by_id(db: Session, rule_id: int) -> models.Rule:
    return db.query(models.Rule).filter(models.Rule.id == rule_id).first()


def get_rules_by_groups_and_ap_type_id(db: Session, group_ids: set, ap_type_id: int) -> List[models.Rule]:
    grouprules = db.query(models.GroupRule).filter(models.GroupRule.group_id.in_(group_ids))
    rule_ids = [x.rule_id for x in grouprules]
    dt = datetime.now()
    # TODO maybe only query for 'priority' and 'allow'
    rules = db.query(models.Rule)\
        .join(models.TimeSpec)\
        .filter(models.Rule.time_spec_id == models.TimeSpec.id)\
        .filter(models.Rule.id.in_(rule_ids))\
        .filter(models.Rule.ap_type_id == ap_type_id)\
        .filter(models.TimeSpec.weekday_mask.op('&')(1 << dt.weekday()) > 0)\
        .filter(models.TimeSpec.date_from <= dt)\
        .filter(models.TimeSpec.date_to >= dt)\
        .filter(models.TimeSpec.time_from <= dt.time())\
        .filter(models.TimeSpec.time_to >= dt.time())
    return rules


def get_rules_by_ap_type_id(db: Session, ap_type_id: int) -> List[models.Rule]:
    rules = db.query(models.Rule).filter(models.Rule.ap_type_id == ap_type_id).all()
    return rules


def create_rule(db: Session, rule: schemas.RuleBase) -> models.Rule:
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


def delete_rule(db: Session, rule_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.Rule).filter(models.Rule.id == rule_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def get_rules_by_ids(db: Session, rules_ids: List[int]) -> List[models.Rule]:
    return db.query(models.Rule).filter(models.Rule.id.in_(rules_ids))


def get_rules_ids_by_group_id(db: Session, group_id: int) -> List[models.Rule]:
    db_grouprules = db.query(models.GroupRule).filter(models.GroupRule.group_id == group_id)
    ids = [gr.rule_id for gr in db_grouprules]
    return ids


def get_aps(db: Session, offset: int = 100, limit: int = 100) -> List[models.AccessPoint]:
    return db.query(models.AccessPoint).offset(offset).limit(limit).all()


def get_aps_by_ap_type(db: Session, aptype_id: int) -> List[models.AccessPoint]:
    db_aps = db.query(models.AccessPoint).filter(models.AccessPoint.type_id == aptype_id).all()
    return db_aps


def create_ap(db: Session, ap_base: schemas.AccessPointBase) -> Optional[schemas.AccessPoint]:
    try:
        new_ap = models.AccessPoint(name=ap_base.name)
        db.add(new_ap)
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return None
    return new_ap


def delete_ap(db: Session, ap_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.AccessPoint).filter(models.AccessPoint.id == ap_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def update_ap(db: Session, ap_id: int, data: schemas.AccessPointBase) -> Tuple[bool, str]:
    try:
        db.query(models.AccessPoint).filter(models.AccessPoint.id == ap_id).update({
            'name': data.name
        })
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def get_aps_by_ids(db: Session, ids: List[int]) -> List[models.AccessPoint]:
    aps = db.query(models.AccessPoint).filter(models.AccessPoint.id.in_(ids))
    return aps


def add_aps_to_aptype(db: Session, aptype_id: int, ap_ids: List[int]) -> bool:
    try:
        for ap_id in ap_ids:
            db.query(models.AccessPoint).filter(models.AccessPoint.id == ap_id).update({'type_id': aptype_id})
        db.commit()
    except Exception:
        return False
    return True


def remove_aps_from_aptype(db: Session, aptype_id: int, ap_ids: List[int]) -> bool:
    try:
        for ap_id in ap_ids:
            db.query(models.AccessPoint).filter(models.AccessPoint.id == ap_id).update({'type_id': None})
        db.commit()
    except Exception:
        return False
    return True


def get_aptypes(db: Session) -> List[models.AccessPointType]:
    return db.query(models.AccessPointType).all()


def get_ap_type_by_id(db: Session, ap_type_id: int) -> models.AccessPointType:
    return db.query(models.AccessPointType).filter(models.AccessPointType.id == ap_type_id).first()


def get_ap_type_by_name(db: Session, ap_type_name: str) -> models.AccessPointType:
    return db.query(models.AccessPointType).filter(models.AccessPointType.name == ap_type_name).first()


def get_ap_type_id_by_ap_id(db, ap_id) -> Optional[int]:
    aptype = db.query(models.AccessPoint).filter(models.AccessPoint.id == ap_id).first()
    if not aptype:
        return None
    return aptype.id


def create_ap_type(db: Session, ap_type: schemas.AccessPointTypeBase) -> models.AccessPointType:
    db_ap_type = models.AccessPointType(
        name=ap_type.name
    )
    db.add(db_ap_type)
    db.commit()
    return db_ap_type


def delete_ap_type(db: Session, ap_type_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.AccessPointType).filter(models.AccessPointType.id == ap_type_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


def get_time_spec_by_id(db: Session, time_spec_id: int) -> models.TimeSpec:
    return db.query(models.TimeSpec).filter(models.TimeSpec.id == time_spec_id).first()


def get_time_spec_by_title(db: Session, time_spec_title: str) -> models.TimeSpec:
    return db.query(models.TimeSpec).filter(models.TimeSpec.title == time_spec_title).first()


def create_time_spec(db: Session, time_spec: schemas.TimeSpecBase) -> models.TimeSpec:
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


def delete_time_spec(db: Session, time_spec_id: int) -> Tuple[bool, str]:
    try:
        db.query(models.TimeSpec).filter(models.TimeSpec.id == time_spec_id).delete()
        db.commit()
    except Exception as e:
        runtime_logger.exception(e)
        return False, str(e)
    return True, 'success'


# Does not take date_from and date_to into account, returns all that match weekday, time_from, time_to
def get_time_spec_by_datetimes(db: Session, weekday: int, time_from: datetime.time, time_to: datetime.time) -> List[dict]:
    time_specs = db.query(models.TimeSpec).filter(
                    and_(
                        models.TimeSpec.weekday_mask.op('&')(1 << weekday) > 0,
                        models.TimeSpec.time_from == time_from,
                        models.TimeSpec.time_to == time_to
                    )
                )
    return [
        {
            'id': ts.id,
            'weekday_mask': ts.weekday_mask,
            'time_from': ts.time_from,
            'time_to': ts.time_to,
            'date_from': ts.date_from,
            'date_to': ts.date_to
        }
        for ts in time_specs
    ]


def get_groups_by_ap_type_and_time_spec(db: Session, ap_type_id: int, time_spec_id: int) -> List[dict]:
    rules = db.query(models.Rule).filter(
                and_(models.Rule.ap_type_id == ap_type_id, models.Rule.time_spec_id == time_spec_id)
            )
    rule_ids = [rule.id for rule in rules]
    grouprules = db.query(models.GroupRule).filter(models.GroupRule.id.in_(rule_ids))
    group_ids = [grouprule.group_id for grouprule in grouprules]
    groups = db.query(models.Group).filter(models.Group.id.in_(group_ids))
    result = [{'id': group.id, 'name': group.name} for group in groups]
    return result
