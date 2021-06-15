from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, CheckConstraint, Time, Date
from sqlalchemy import and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.hybrid import hybrid_method
from datetime import datetime

from .database import Base, utcnow


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    card = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    is_staff = Column(Boolean, nullable=False, default=False)
    hashed_password = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())  # TODO Check whether updated is correct

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
    name = Column(String, nullable=True, unique=True)
    allow = Column(Boolean, server_default="False", nullable=False)
    ap_type_id = Column(Integer, ForeignKey('access_point_type.id'), nullable=False)
    time_spec_id = Column(Integer, ForeignKey('time_spec.id'), nullable=False)
    time_spec = relationship('TimeSpec', back_populates='rules')
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
    title = Column(String, unique=True)
    # Day number i if (weekday_mask & (1 << i)), 0 is Monday
    weekday_mask = Column('weekday_mask', Integer, CheckConstraint('0 <= weekday_mask AND weekday_mask <= 255'), nullable=False)
    time_from = Column(Time, nullable=False)
    time_to = Column(Time, nullable=False)
    date_from = Column(DateTime, nullable=False, server_default=utcnow())
    date_to = Column(DateTime, nullable=False)  # TODO server_default?
    rules = relationship('Rule', back_populates='time_spec')
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())

    @hybrid_method
    def matches_time(self, dt: datetime):
        return self.date_from <= dt.date() <= self.date_to\
            and (self.weekday_mask & (1 << dt.weekday()) > 0)\
            and self.time_from <= dt.time() <= self.time_to

    @matches_time.expression
    def matches_time(cls, dt: datetime):
        return and_(
            cls.date_from <= dt.date() <= cls.date_to,
            (cls.weekday_mask & (1 << dt.weekday())) > 0,
            cls.time_from <= dt.time() <= cls.time_to)

    @hybrid_method
    def valid_at_day(self, weekday: int):
        return (self.weekday_mask & (1 << weekday)) > 0

    @valid_at_day.expression
    def valid_at_day(cls, weekday: int):
        return (cls.weekday_mask & (1 << weekday)) > 0


class AccessPointType(Base):
    __tablename__ = 'access_point_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class AccessPoint(Base):
    __tablename__ = 'access_point'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type_id = Column(Integer, ForeignKey('access_point_type.id'), nullable=True, default=None)
    controller_id = Column(Integer, ForeignKey('controllers.id'), nullable=True, default=None)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())

    ap_type = relationship('AccessPointType', backref='access_points')


class Controller(Base):
    __tablename__ = 'controllers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_seen = Column(DateTime, onupdate=utcnow())
    db_version = Column(Integer)
    fw_version = Column(Integer)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


# TODO toto asi nechceme, asi budeme logovat skor do suborov ako do databazy
class AccessLog(Base):
    __tablename__ = 'access_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    controller_id = Column(Integer, ForeignKey('controllers.id'), nullable=False)
    card = Column(String)
    without_card = Column(Boolean, server_default='False')
    allowed = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, server_default=utcnow())
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class ErrorLog(Base):
    __tablename__ = 'error_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    controller_id = Column(Integer, ForeignKey('controllers.id'), nullable=False)
    error_code = Column(Integer, nullable=False)
    timestamp = Column(DateTime, server_default=utcnow())
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class ErrorDesc(Base):
    __tablename__ = 'error_description'

    code = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True)
    description = Column(String)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())
