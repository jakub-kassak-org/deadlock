from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime


class UserGroup(BaseModel):
    id: int
    user_id: int
    group_id: int

    class Config:
        orm_mode = True


class GroupRule(BaseModel):
    id: int
    group_id: int
    rule_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    card: str
    username: str
    first_name: str
    last_name: str
    is_staff: bool

    class Config:
        orm_mode = True


class User(UserBase):
    id: str
    disabled: bool
    groups: List[UserGroup] = []
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Group(BaseModel):
    id: int
    name: str
    rules: List[GroupRule] = []

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class TimeSpecBase(BaseModel):
    title: str
    weekday_mask: int
    time_from: time
    time_to: time
    date_from: datetime
    date_to: datetime

    class Config:
        orm_mode = True


class TimeSpec(TimeSpecBase):
    id: int

    class Config:
        orm_mode = True


class AccessPointTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AccessPointType(AccessPointTypeBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class RuleBase(BaseModel):
    name: str
    allow: bool
    time_spec_id: int
    ap_type_id: int
    priority: int

    class Config:
        orm_mode = True


class Rule(RuleBase):
    id: int
    created: datetime
    updated: datetime
    groups: List[GroupRule] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Controller(BaseModel):
    db_version: int
    fw_version: int

    class Config:
        orm_mode = True


class AccessPoint(BaseModel):
    name: str
    type: AccessPointType
    controller: Controller

    class Config:
        orm_mode = True


class ErrorDescription(BaseModel):
    code: int
    ticker: str
    description: str

    class Config:
        orm_mode = True
