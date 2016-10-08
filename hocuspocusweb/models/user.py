import hashlib
from .meta import Base
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(100))
    mac_address = Column(String(100))
    name = Column(Text)
    password = Column(String)
    email = Column(Text)

    def __init__(self, **kwargs):
        self.ip_address = kwargs.get('ip_address', None)
        self.name = kwargs.get('name', None)
        self.email = kwargs.get('email', None)
        self.mac_address = kwargs.get('mac_address', None)
        password = kwargs.get('password', None)
        if password:
            self.set_password(password)

    def check_password(self, password):
        pass_salt = password + self.ip_address
        hash_password = hashlib.sha512(pass_salt.encode('utf-8')).hexdigest()
        return hash_password == self.password

    def set_password(self, password):
        pass_salt = password + self.ip_address
        self.password = hashlib.sha512(pass_salt.encode('utf-8')).hexdigest()


Index('user_mac_index', User.ip_address, unique=True, mysql_length=255)
