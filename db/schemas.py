from pydantic import BaseModel
from typing import List


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


class User(BaseModel):
    id: str
    active: bool
    groups: List[UserGroup] = []

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    title: str
    rules: List[GroupRule] = []

    class Config:
        orm_mode = True


class Rule(BaseModel):
    id: int
    title: int
    groups: List[GroupRule] = []
