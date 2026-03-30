from sqlalchemy import Column, Integer, String, DateTime, orm
from flask_login import UserMixin
from sqlalchemy.util import md5_hex
from hashlib import md5
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    modified_date = Column(DateTime)

    jobs = orm.relationship('Jobs', back_populates='user')

    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name}'

    def hash_password(self, password):
        self.hashed_password = md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == md5(password.encode()).hexdigest()
