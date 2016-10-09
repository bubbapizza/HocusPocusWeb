import hashlib
from .meta import Base
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Boolean,
)
from collections import namedtuple


HashColumns = namedtuple('HashColumns', 'column_name salt_column')
default_columns = HashColumns('password', 'ip_address')
master_columns = HashColumns('master_password', 'email')


class PoorPassword(Exception):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(100), unique=True, index=True, nullable=False)
    mac_address = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(Text, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(Text, unique=True, index=True, nullable=False)
    master = Column(Boolean(name='master'), default=False, nullable=False)
    master_username = Column(String(100),
                             unique=True, index=True, nullable=True)
    master_password = Column(String, nullable=True)

    def __init__(self, **kwargs):
        self.ip_address = kwargs.get('ip_address', None)
        self.name = kwargs.get('name', None)
        self.email = kwargs.get('email', None)
        self.mac_address = kwargs.get('mac_address', None)
        password = kwargs.get('password', None)
        if password:
            self.set_password(password)

    def check_password(self, password, columns=default_columns):
        pass_salt = password + getattr(self, columns.salt_column)
        hash_password = hashlib.sha512(pass_salt.encode('utf-8')).hexdigest()
        return hash_password == getattr(self, columns.column_name)

    def set_password(self, password, columns=default_columns):
        pass_salt = password + getattr(self, columns.salt_column)
        setattr(
            self,
            columns.column_name,
            hashlib.sha512(pass_salt.encode('utf-8')).hexdigest()
        )

    def set_master_password(self, password):
        if len(password) < 10:
            raise PoorPassword('Password needs to be more than 10 characters')

        self.set_password(password, columns=master_columns)

    def check_master_password(self, password):
        return self.check_password(password, columns=master_columns)
