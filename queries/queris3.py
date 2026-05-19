from data.db_session import global_init, create_session
from data.users import User

global_init(input())
session = create_session()

result = session.query(User).filter(
    User.age < 18
).all()
for user in result:
    print("<Colonist>", user.id, user.surname, user.name, user.age, "years")
