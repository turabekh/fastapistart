import enum
import uuid
from datetime import datetime

import pytz
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.types import TypeDecorator

ph = PasswordHasher()


class Password(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, length=128, **kwargs):
        super().__init__(length=length, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return ph.hash(value)

    def process_result_value(self, value, dialect):
        return value

    @staticmethod
    def verify(plain_password, hashed_password):
        try:
            return ph.verify(hashed_password, plain_password)
        except VerifyMismatchError:
            return False


class UpperCaseString(TypeDecorator):
    impl = String()
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = value.upper()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.upper()


class LowerCaseString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return value.lower() if value else value


class UTCDateTime(TypeDecorator):
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.astimezone(pytz.UTC)


class __Enum__(TypeDecorator):
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, enum.Enum):
                value = value.value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = self.enumtype(value)
        return value


class IntEnum(__Enum__):
    impl = Integer
    cache_ok = True


class StrEnum(__Enum__):
    impl = String
    cache_ok = True


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created = Column(UTCDateTime, server_default=func.now(), nullable=False)
    updated = Column(UTCDateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(UTCDateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(pytz.UTC)
