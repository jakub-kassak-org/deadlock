import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import conint

from db import models, crud
from db.database import SessionLocal, engine
from db.schemas import *

from typing import Optional, List

from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta, time

from loggers import access_logger, runtime_logger
import log_messages


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
        runtime_logger.error('JWTError: main.py/get_current_user')
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        runtime_logger.error('user is None: main.py/get_current_user')
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        runtime_logger.error('current_user.disabled: main.py/get_current_active_user')
        raise HTTPException(status_code=400, detail="Inactive user.")
    return current_user


def is_user_staff(user: User):
    return user and user.is_staff


@app.get('/')
async def root():
    return {'message': 'response'}


@app.get('/users/', response_model=List[UserOut])
async def get_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users


@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/{user_id}/get_groups/", response_model=List[GroupBase])
def get_groups_of_user(user_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    groups = crud.get_groups_by_user_id(db=db, user_id=user_id)
    return groups


@app.post("/users/", response_model=User)
def create_user(user: UserBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    db_user = crud.get_user_by_card(db=db, card=user.card)
    if db_user:
        raise HTTPException(status_code=400, detail="Card already registered for different user.")
    return crud.create_user(db=db, user_base=user)


@app.delete("/users/delete/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400,
                            detail=f"User with id {user_id} does not exist, therefore can't be deleted.")
    deleted, detail = crud.delete_user(db=db, user_id=user_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': user_id
    }


@app.put("/users/update/{user_id}/")
def update_user(user_id: int, updated_user: UserBase, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with id {user_id} does not exist.")
    updated, detail = crud.update_user(db=db, user_id=user_id, data=updated_user)
    return {
        'was_updated': updated,
        'detail': detail,
        'id': user_id
    }


@app.post("/users/{user_id}/assign_ap_type/")
def assign_ap_type_to_user(user_id: int, ap_type_id: int, timespec: TimeSpecBaseAnonymous,
                           db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with id={user_id} does not exist.")
    db_ap_type = crud.get_ap_type_by_id(db=db, ap_type_id=ap_type_id)
    if not db_ap_type:
        raise HTTPException(status_code=400, detail=f"Access point type with id={ap_type_id} does not exist.")
    success = True
    try:
        timespec_named = TimeSpecBase(
            weekday_mask=timespec.weekday_mask,
            date_from=timespec.date_from,
            date_to=timespec.date_to,
            time_from=timespec.time_from,
            time_to=timespec.time_to,
            title=f'{timespec.weekday_mask}-{timespec.time_from}-{timespec.time_to}-{timespec.date_from}-'
            f'{timespec.date_to}-{hash(str(datetime.now()))}'
        )
        db_time_spec = crud.create_time_spec(db=db, time_spec=timespec_named)
        gc = GroupCreate(name=f'{user_id}-{ap_type_id}-{db_time_spec.id}')
        new_group = crud.create_group(db=db, group=gc)
        crud.add_user_to_group(db=db, user_id=user_id, group_id=new_group.id)
        rb = RuleBase(
            name=f'{ap_type_id}-{db_time_spec.id}-{new_group.id}',
            allow=True,
            time_spec_id=db_time_spec.id,
            ap_type_id=ap_type_id,
            priority=1
        )
        new_rule = crud.create_rule(db=db, rule=rb)
        crud.set_group_rules_ids(db=db, group_id=new_group.id, rules_ids=[new_rule.id])
    except Exception as e:
        runtime_logger.exception(e)
        success = False
    return {'success': success}


@app.get("/groups/by_ap_type_and_time_spec/")
def get_groups_by_ap_type_and_time_spec(ap_type_id: int, time_spec_id: int, db: Session = Depends(get_db),
                                        current_user: User = Depends(get_current_active_user)):
    db_groups = crud.get_groups_by_ap_type_and_time_spec(db=db, ap_type_id=ap_type_id, time_spec_id=time_spec_id)
    return {'groups': db_groups}


@app.get("/groups/")
async def get_groups(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    groups = crud.get_groups(db, offset=offset, limit=limit)
    return {'groups': groups}


# Returns list of users from this group
@app.get("/groups/{group_id}/")
async def get_group(group_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    users_in_group = crud.get_users_from_group(db=db, group_id=group_id)
    return {
        'group_id': group_id,
        'users': users_in_group
    }


@app.post("/groups/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)):
    db_group = crud.get_group_by_name(db=db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group with this name already registered.")
    return crud.create_group(db=db, group=group)


@app.delete("/groups/delete/{group_id}/")
def delete_group(group_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_group = crud.get_group_by_id(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=400,
                            detail=f"Group with id {group_id} does not exist, therefore can't be deleted.")
    deleted, detail = crud.delete_group(db=db, group_id=group_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': group_id,
    }


@app.put("/groups/update/{group_id}/")
def update_group(group_id: int, updated_group: GroupCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)):
    db_group = crud.get_group_by_id(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=400,
                            detail=f"Group with id {group_id} does not exist, therefore can't be updated.")
    updated, detail = crud.update_group(db=db, group_id=group_id, data=updated_group)
    return {
        'was_updated': updated,
        'detail': detail,
        'id': group_id
    }


@app.post("/groups/{group_id}/change_ruleset/")
def change_ruleset_of_group(group_id: int, include_rules_ids: List[int], exclude_rules_ids: List[int],
                            db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    include_rules_cnt = crud.get_rules_by_ids(db=db, rules_ids=include_rules_ids).count()
    if include_rules_cnt != len(include_rules_ids):
        raise HTTPException(status_code=400,
                            detail="At least one rule id in include_rules_ids does not exist in the database.")
    exclude_rules_cnt = crud.get_rules_by_ids(db=db, rules_ids=exclude_rules_ids).count()
    if exclude_rules_cnt != len(exclude_rules_ids):
        raise HTTPException(status_code=400,
                            detail="At least one rule id in exclude_rules_ids does not exist in the database.")
    curr_group_rules_ids = set(crud.get_rules_ids_by_group_id(db=db, group_id=group_id))
    updated_group_rules_ids = curr_group_rules_ids.union(set(include_rules_ids)) - set(exclude_rules_ids)
    updated, detail = crud.set_group_rules_ids(db=db, group_id=group_id, rules_ids=updated_group_rules_ids)
    return {
        'updated': updated,
        'detail': detail,
        'id': group_id
    }


def exists_group(db: Session, group_id: int):
    if not crud.get_group_by_id(db, group_id):
        raise HTTPException(status_code=400, detail=f"Group with id {group_id} does not exists.")


@app.get("/groups/{group_id}/topics/")
def get_topics_of_group(group_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    exists_group(db, group_id)
    return {
        'id': group_id,
        'topics': crud.get_topics_of_group(db, group_id)
    }


@app.post("/groups/{group_id}/topics/")
def add_topics_of_group(group_id: int, topics: List[str], db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    exists_group(db, group_id)
    if not crud.exists_all_topics(db, topics):
        raise HTTPException(status_code=400, detail=f"Not all topics exists.")
    current_topics = crud.get_topics_of_group(db, group_id)
    topics = list(set(topics) - set(current_topics))
    updated = crud.add_topics_of_group(db, group_id, list(topics))
    return {
        'updated': updated,
        'added_topics': topics if updated else [],
        'id': group_id
    }


@app.delete("/groups/{group_id}/topics/")
def delete_topics_of_group(group_id: int, topics: List[str], db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    exists_group(db, group_id)
    current_topics = crud.get_topics_of_group(db, group_id)
    difference = set(topics) - set(current_topics)
    if difference:
        raise HTTPException(status_code=400, detail=f"Topics {difference} are not assigned to group {group_id}.")
    return {
        "success": crud.remove_topics_of_group(db, group_id, topics),
        "id": group_id
    }


@app.post("/usergroup/add/", response_model=UserGroup)
def add_user_to_group(user_id: int, group_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with id {user_id} not found.")
    db_group = crud.get_group_by_id(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail=f"Group with id {group_id} not found.")
    db_usergroup = crud.get_usergroup(db=db, user_id=user_id, group_id=group_id)
    if db_usergroup:
        raise HTTPException(status_code=400, detail=f"User with id {user_id} is already in a group with id {group_id}.")
    return crud.add_user_to_group(db=db, user_id=user_id, group_id=group_id)


@app.delete("/usergroup/delete/{user_id}/{group_id}/", response_model=UserGroupDelete)
def delete_user_from_group(user_id: int, group_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"User with id {user_id} not found.")
    db_group = crud.get_group_by_id(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail=f"Group with id {group_id} not found.")
    db_usergroup = crud.get_usergroup(db=db, user_id=user_id, group_id=group_id)
    if not db_usergroup:
        raise HTTPException(status_code=400,
                            detail=f"User with id {user_id} is not in the group with id {group_id}, nothing to delete")
    deleted, detail = crud.delete_user_from_group(db=db, usergroup_id=db_usergroup.id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': db_usergroup.id,
        'user_id': user_id,
        'group_id': group_id
    }


@app.post("/rules/add/", response_model=Rule)
def create_rule(rule: RuleBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_rule = crud.get_rule_by_name(db=db, name=rule.name)
    if db_rule:
        raise HTTPException(status_code=400, detail=f"Rule with name {rule.name} already exists.")
    db_ap_type = crud.get_ap_type_by_id(db=db, ap_type_id=rule.ap_type_id)
    if not db_ap_type:
        raise HTTPException(status_code=400, detail=f"AccesspointType with id {rule.ap_type_id} does not exist.")
    db_time_spec = crud.get_time_spec_by_id(db=db, time_spec_id=rule.time_spec_id)
    if not db_time_spec:
        raise HTTPException(status_code=400, detail=f"TimeSpec with id {rule.time_spec_id} does not exist.")
    return crud.create_rule(db=db, rule=rule)


@app.delete("/rules/delete/{rule_id}/")
def delete_rule(rule_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_rule = crud.get_rule_by_id(db=db, rule_id=rule_id)
    if not db_rule:
        raise HTTPException(status_code=400, detail=f"Rule with id {rule_id} does not exist, nothing to delete.")
    deleted, detail = crud.delete_rule(db=db, rule_id=rule_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': rule_id
    }


def evaluate_entry(card: str, ap_type_id: int, db: Session):
    group_ids = crud.get_groups_ids_by_card(db=db, card=card)
    if len(group_ids) == 0:
        access_logger.info(
            f'({card}, {ap_type_id}) - {log_messages.DENY}: {log_messages.MSG_USR_NOT_IN_ANY_GROUP}')
        return {'allow': False}  # This user is not in any group, therefore there are no rules for him -> Deny
    rules = crud.get_rules_by_groups_and_ap_type_id(db=db, group_ids=group_ids, ap_type_id=ap_type_id)
    # Highest priority first, if any rule of highest priority is deny, then deny. TODO decide whether this is good
    priority_and_result = [(x.priority, x.allow) for x in rules]
    priority_and_result.sort(key=lambda x: x[0] - x[1] * 0.5, reverse=True)
    if len(priority_and_result) == 0:
        access_logger.info(f'({card}, {ap_type_id}) - {log_messages.DENY}: {log_messages.MSG_NO_RULES_FOR_USER}')
        return {'allow': False}
    access_logger.info(
        f'({card}, {ap_type_id}) - {(log_messages.ALLOW if priority_and_result[0][1] else log_messages.DENY)}: Decided by a rule'
    )
    return {'allow': priority_and_result[0][1]}


@app.get("/entry/eval/ip_addr/{card}/{ip_addr}/")
def evaluate_entry_by_access_point_ip_addr(card: str, ip_addr: str, db: Session = Depends(get_db),
                                           current_user: User = Depends(get_current_active_user)):
    db_ap = crud.get_ap_by_ip_addr(db, ip_addr)
    if not db_ap:
        access_logger.error(
            f'({card}, {ip_addr}) - {log_messages.DENY}: {log_messages.MSG_NO_AP_FOR_THIS_IP_ADDR}')
        return {"allow": False}
    return evaluate_entry(card, db_ap.type_id, db)


# Allows or denies
@app.post("/entry/eval/")
def evaluate_entry_by_access_point_id(card: str, ap_id: int, db: Session = Depends(get_db),
                                      current_user: User = Depends(get_current_active_user)):
    ap_type_id = crud.get_ap_type_id_by_ap_id(db=db, ap_id=ap_id)
    if not ap_type_id:
        # No ap_type for this ap
        access_logger.error(
            f'({card}, {ap_id}) - {log_messages.DENY}: {log_messages.MSG_NO_AP_TYPE_FOR_THIS_AP}')
        return {'allow': False}
    return evaluate_entry(card, ap_type_id, db)


@app.post("/timespec/add/", response_model=TimeSpec)
def create_timespec(timespec: TimeSpecBase, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    db_timespec = crud.get_time_spec_by_title(db=db, time_spec_title=timespec.title)
    if db_timespec:
        raise HTTPException(status_code=400, detail=f"TimeSpec with title {timespec.title} already exists.")
    return crud.create_time_spec(db=db, time_spec=timespec)


@app.delete("/timespec/delete/{time_spec_id}/")
def delete_timespec(time_spec_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    db_timespec = crud.get_time_spec_by_id(db=db, time_spec_id=time_spec_id)
    if not db_timespec:
        raise HTTPException(status_code=400, detail=f"TimeSpec with id {time_spec_id} does not exist.")
    deleted, detail = crud.delete_time_spec(db=db, time_spec_id=time_spec_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': time_spec_id
    }


@app.get("/timespec/get_ids/")
def get_timespec_ids(weekday: int, time_from: str, time_to: str, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    hour_minutes: List[List[int, int], List[int, int]] = [[int(x) for x in t.split(':')] for t in [time_from, time_to]]
    for i in range(2):
        if not 0 <= hour_minutes[i][0] <= 23:
            raise HTTPException(status_code=400, detail=f"Hour has to be from range [0, 23].")
        elif not 0 <= hour_minutes[i][1] <= 59:
            raise HTTPException(status_code=400, detail=f"Minute has to be from range[0, 59].")
    t_from = time(hour=hour_minutes[0][0], minute=hour_minutes[0][1])
    t_to = time(hour=hour_minutes[1][0], minute=hour_minutes[1][1])
    timespec_ids = crud.get_time_spec_by_datetimes(db=db, weekday=weekday, time_from=t_from, time_to=t_to)
    return timespec_ids


@app.get("/ap/")
def get_access_points(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    db_aps = crud.get_aps(db=db, offset=offset, limit=limit)
    return {'access_points': db_aps}


@app.get("/ap/{ap_id}/")
def get_access_point_info(ap_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_active_user)):
    return crud.get_ap_by_id(db=db, ap_id=ap_id)


@app.post("/ap/add/", response_model=AccessPoint)
def create_access_point(ap: AccessPointBase, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    return crud.create_ap(db=db, ap_base=ap)


@app.delete("/ap/delete/{ap_id}/")
def delete_access_point(ap_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    db_ap = crud.get_aps_by_ids(db=db, ids=[ap_id])
    if db_ap.count() == 0:
        raise HTTPException(status_code=400, detail=f"Access point with id={ap_id} does not exist in the database.")
    deleted, detail = crud.delete_ap(db=db, ap_id=ap_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': ap_id
    }


@app.put("/ap/update/{ap_id}/")
def update_access_point(ap_id: int, updated_ap: AccessPointBase, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    db_ap = crud.get_aps_by_ids(db=db, ids=[ap_id])
    if db_ap.count() == 0:
        raise HTTPException(status_code=400, detail=f"Access point with id={ap_id} does not exist in the database.")
    updated, detail = crud.update_ap(db=db, ap_id=ap_id, data=updated_ap)
    return {
        'was_updated': updated,
        'detail': detail,
        'id': ap_id
    }


@app.get("/aptype/")
def get_aptypes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_aptyes = crud.get_aptypes(db=db)
    return db_aptyes


@app.post("/aptype/add/", response_model=AccessPointType)
def create_aptype(aptype: AccessPointTypeBase, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    db_aptype = crud.get_ap_type_by_name(db=db, ap_type_name=aptype.name)
    if db_aptype:
        raise HTTPException(status_code=400, detail=f"AccesspointType with name {aptype.name} already exists.")
    return crud.create_ap_type(db=db, ap_type=aptype)


@app.delete("/aptype/delete/{ap_type_id}/")
def delete_aptype(ap_type_id: int, db: Session = Depends(get_db), c_user: User = Depends(get_current_active_user)):
    db_aptype = crud.get_ap_type_by_id(db=db, ap_type_id=ap_type_id)
    if not db_aptype:
        raise HTTPException(status_code=400, detail=f"APType with id {ap_type_id} does not exist, nothing to delete.")
    deleted, detail = crud.delete_ap_type(db=db, ap_type_id=ap_type_id)
    return {
        'was_deleted': deleted,
        'detail': detail,
        'id': ap_type_id
    }


@app.get("/aptype/{aptype_id}/get_aps/", response_model=List[AccessPointOut])
def get_aps_by_aptype(aptype_id: int, db: Session = Depends(get_db), c_user: User = Depends(get_current_active_user)):
    db_aps = crud.get_aps_by_ap_type(db=db, aptype_id=aptype_id)
    return db_aps


@app.put("/aptype/{aptype_id}/add_aps/")
def add_aps_to_aptype(aptype_id: int, add_ids: List[int], db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    db_aptype = crud.get_ap_type_by_id(db=db, ap_type_id=aptype_id)
    if not db_aptype:
        raise HTTPException(status_code=400, detail=f"Access point type with id={aptype_id} does not exist.")
    db_aps = crud.get_aps_by_ids(db=db, ids=add_ids)
    if db_aps.count() != len(add_ids):
        raise HTTPException(status_code=400, detail="At least one of the provided access point ids does not belong to any access point.")
    added = crud.add_aps_to_aptype(db=db, aptype_id=aptype_id, ap_ids=add_ids)
    return {
        'success': added,
        'id': aptype_id
    }


@app.put("/aptype/{aptype_id}/remove_aps/")
def remove_aps_from_aptype(aptype_id: int, remove_ids: List[int], db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    db_aptype = crud.get_ap_type_by_id(db=db, ap_type_id=aptype_id)
    if not db_aptype:
        raise HTTPException(status_code=400, detail=f"Access point type with id={aptype_id} does not exist.")
    db_aps = crud.get_aps_by_ids(db=db, ids=remove_ids)
    if db_aps.count() != len(remove_ids):
        raise HTTPException(status_code=400,
                            detail="At least one of the provided access point ids does not belong to any access point.")
    removed = crud.remove_aps_from_aptype(db=db, aptype_id=aptype_id, ap_ids=remove_ids)
    return {
        'success': removed,
        'id': aptype_id
    }


@app.get("/aptype/{aptype_id}/get_rules/", response_model=List[RuleNoGroups])
def get_rules_by_aptype(aptype_id: int, db: Session = Depends(get_db), c_user: User = Depends(get_current_active_user)):
    db_aptype = crud.get_ap_type_by_id(db=db, ap_type_id=aptype_id)
    if not db_aptype:
        raise HTTPException(status_code=400, detail=f"Access point type with id={aptype_id} does not exist.")
    db_rules = crud.get_rules_by_ap_type_id(db=db, ap_type_id=aptype_id)
    return db_rules


@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    exp_time = datetime.now() + access_token_expires
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expiration_time": exp_time,
        "valid_for_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    }


@app.get("/log/", response_model=List[LogOut])
def get_logs(offset: conint(ge=0) = 0, limit: conint(ge=1) = 100, levelno: int = 30, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_active_user)):
    return crud.get_logs(db, offset, limit, levelno)


@app.post("/log/")
def post_log(log_data: LogIn, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_active_user)):
    db_ap = crud.get_ap_by_ip_addr(db, log_data.ip_addr)
    if not db_ap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Access point with ip address '{log_data.ip_addr}' does not exists"
        )
    return {"success": crud.add_log(db, log_data, db_ap.id)}


@app.get("/log/count/")
def get_log_count(levelno: int = 30, time_from: datetime = datetime(2020, 1, 1), time_to: datetime = datetime.utcnow(),
                  db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return {
        "count": crud.get_log_count(db, levelno, time_from, time_to),
        "time_from": time_from,
        "time_to": time_to,
        "levelno": levelno,
        "from": "all"
    }


@app.get("/log/count/server/")
def get_log_count_from_server(levelno: int = 30, time_from: datetime = datetime(2020, 1, 1),
                              time_to: datetime = datetime.utcnow(), db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_active_user)):
    return {
        "count": crud.get_log_count_by_ap_id(db, levelno, time_from, time_to, None),
        "time_from": time_from,
        "time_to": time_to,
        "levelno": levelno,
        "from": "server"
    }


@app.get("/log/count/{ap_ip_addr}/")
def get_log_count_by_ip_addr(ap_ip_addr: str, levelno: int = 30, time_from: datetime = datetime(2020, 1, 1),
                             time_to: datetime = datetime.utcnow(), db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_active_user)):
    ap = crud.get_ap_by_ip_addr(db, ap_ip_addr)
    if ap is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Access point with IP {ap_ip_addr} does not exists"
        )
    return {
        "count": crud.get_log_count_by_ap_id(db, levelno, time_from, time_to, ap.id),
        "time_from": time_from,
        "time_to": time_to,
        "levelno": levelno,
        "from": "controllers",
        "ap_ip_addr": ap_ip_addr,
        "ap_id": ap.id
    }


@app.get("/topics/")
def get_topics(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_active_user)):
    return {"topics": crud.get_topics(db, offset, limit)}


@app.post("/topics/")
def create_topic(topic: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if crud.exists_topic(db, topic):
        raise HTTPException(status_code=400, detail=f"Topic '{topic}' already exists, therefore can't be created.")
    return {"success": crud.create_topic(db, topic)}


@app.delete("/topics/")
def delete_topic(topic: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not crud.exists_topic(db, topic):
        raise HTTPException(status_code=400, detail=f"Topic '{topic}' does not exist, therefore can't be deleted.")
    if not crud.delete_topic(db, topic):
        raise HTTPException(status_code=400, detail=f"Topic '{topic}' is assigned to some group or notification")
    return {"success": True}


@app.post("/notify/")
def notify(data: NotificationIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    notification = crud.create_notification(db, data)
    # print(notification)
    if not notification:
        raise HTTPException(
            status_code=400,
            detail=f"Topic '{data.topic}' does not exist, therefore notification can't be created."
        )
    if not crud.add_notification_to_users(db, notification.id, notification.topic):
        return {"success": False, "count": 0}
    ids_mails = crud.get_user_ids_mails_by_topic(db, data.topic)
    # print(ids_mails)
    to = [x[1] for x in ids_mails]
    if len(to) == 0:
        return {"success": True, "count": 0}
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    login = "deadlock.uniba@gmail.com"
    password = "fravoxbmpejevahv"
    smtp.login(login, password)
    msg = MIMEMultipart()
    msg['Subject'] = data.title
    msg.attach(MIMEText(data.message))
    smtp.sendmail(from_addr=login,
                  to_addrs=to, msg=msg.as_string())
    smtp.quit()
    sent = crud.update_sent_notifications(db, notification.id, [x[0] for x in ids_mails])
    return {"success": True, "count": len(to) if sent else -1}
