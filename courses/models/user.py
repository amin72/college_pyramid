from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    UniqueConstraint,
)

import datetime
from .meta import Base
from passlib.apps import custom_app_context as courses_pwd_context


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True, nullable=False) # student or teacher id
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    firstname = Column(Unicode(255))
    lastname = Column(Unicode(255))
    personal_code = Column(Unicode(8))
    phone = Column(Unicode(11))
    address = Column(Unicode(255), nullable=True)
    email = Column(Unicode(255), nullable=True)
    birthday = Column(DateTime, nullable=True)

    # username, phone and email have to be unique in database
    __table_args__ = (
        UniqueConstraint(name, phone, email),
    )



    def verify_password(self, password):
        # is it cleartext?
        if password == self.password:
            self.set_password(password)

        return courses_pwd_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = courses_pwd_context.encrypt(password)
        self.password = password_hash
