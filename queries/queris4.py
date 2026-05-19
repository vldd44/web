from data.db_session import global_init, create_session
from data.users import User
from sqlalchemy import or_

global_init(input())
session = create_session()

result = session.query(User).filter(
    or_(
        User.position.like('%chief%'),
        User.position.like('%middle%')
    )
).all()
for user in result:
    print("<Colonist>", user.id, user.surname, user.name, user.position)