from data import db_session

from data.users import User

db_session.global_init(input())
session = db_session.create_session()
users = session.query(User).filter(User.address == 'module_1').all()
print(*users, sep='\n')
