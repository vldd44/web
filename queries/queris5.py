from data.db_session import global_init, create_session
from data.jobs import Jobs

global_init(input())
session = create_session()

result = session.query(Jobs).filter(
    Jobs.work_size < 20,
    Jobs.is_finished == 0
).all()

for job in result:
    print(job)
