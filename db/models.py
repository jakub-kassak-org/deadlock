from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, CheckConstraint, Time, Date
from sqlalchemy.orm import relationship

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
    name = Column(String, nullable=True, unique=True)
    allow = Column(Boolean, server_default="False", nullable=False)
    ap_type_id = Column(Integer, ForeignKey('access_point_type.id'), nullable=False)
    time_spec_id = Column(Integer, ForeignKey('time_spec.id'), nullable=False)
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
    # Day number i if (weekday_mask & (1 << i)), 0 is monday
    weekday_mask = Column('weekday_mask', Integer, CheckConstraint('0 <= weekday_mask AND weekday_mask <= 255'), nullable=False)
    time_from = Column(Time, nullable=False)
    time_to = Column(Time, nullable=False)
    date_from = Column(DateTime, nullable=False, server_default=utcnow())
    date_to = Column(DateTime, nullable=False)  # TODO server_default?
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


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
    type_id = Column(Integer, ForeignKey('access_point_type.id'), nullable=False)
    controller_id = Column(Integer, ForeignKey('controllers.id'), nullable=False)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


class Controller(Base):
    __tablename__ = 'controllers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_seen = Column(DateTime, onupdate=utcnow())
    db_version = Column(Integer)
    fw_version = Column(Integer)
    created = Column(DateTime, server_default=utcnow())
    updated = Column(DateTime, server_default=utcnow(), onupdate=utcnow())


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
