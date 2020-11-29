from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    active = Column(Boolean, default=True, nullable=False)

    groups = relationship('UserGroup')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)

    rules = relationship('GroupRule')


class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    # TODO add time interval

    groups = relationship('GroupRule')


class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))


class GroupRule(Base):
    __tablename__ = 'group_rule'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    rule_id = Column(Integer, ForeignKey('rules.id'))
