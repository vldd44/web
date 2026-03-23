from data.db_session import global_init, create_session
from data.users import User

global_init(input())
session = create_session()

result = session.query(User).filter(
    User.address == "module_1",
    User.speciality.notlike("%engineer%"),
    User.position.notlike("%engineer%")
).all()
for user in result:
    print(user.id)
