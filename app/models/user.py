from sqlalchemy import Boolean, Column, String

from app.models.base import (
    Base,
    LowerCaseString,
    Password,
    SoftDeleteMixin,
    UTCDateTime,
)


class User(Base, SoftDeleteMixin):
    email = Column(LowerCaseString(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(Password(128), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    last_login = Column(UTCDateTime, nullable=True)
