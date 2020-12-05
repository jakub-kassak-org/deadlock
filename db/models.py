from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, DateTime, CheckConstraint, Time, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base, utcnow


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())  # TODO Check whether onupdates is correct

    groups = relationship('UserGroup')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())

    rules = relationship('GroupRule')


class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    allow = Column(Boolean, server_default="False", nullable=False)
    # access_point_id = Column(Integer, ...)
    # time_spec_id = Column(Integer, ...
    priority = Column('priority', Integer, CheckConstraint('0 <= priority AND priority <= 10'), nullable=False, server_default='5')
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())

    groups = relationship('GroupRule')


class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class GroupRule(Base):
    __tablename__ = 'group_rule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    rule_id = Column(Integer, ForeignKey('rules.id'))
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class TimeSpec(Base):
    __tablename__ = 'time_spec'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, server_default='rule')
    weekday_mask = Column('weekday_mask', Integer, CheckConstraint('0 <= weekday_mask AND weekday_mask <= 255'), nullable=False)
    time_from = Column(Time, nullable=False)
    time_to = Column(Time, nullable=False)
    date_from = Column(Date, nullable=False, server_default=utcnow())
    date_to = Column(Date, nullable=False)  # TODO server_default?
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())
