import os

from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department


db_name = input().strip()
db_session.global_init(f"db/{db_name}")
session = db_session.create_session()

department = session.query(Department).filter(Department.id == 1).first()
if not department or not department.members:
    sys.exit(0)

member_ids = [int(m.strip()) for m in department.members.split(',') if m.strip()]

def get_user_hours(user_id):
    total_hours = 0

    jobs = session.query(Jobs).all()
    for job in jobs:
        if job.team_leader == user_id:
            total_hours += job.work_size

        if job.collaborators:
            collabs = [int(c.strip()) for c in job.collaborators.split(',') if c.strip()]
            if user_id in collabs:
                total_hours += job.work_size

    return total_hours

results = []
for user_id in member_ids:
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        continue

    hours = get_user_hours(user_id)
    if hours > 25:
        results.append((user.surname, user.name))

for surname, name in results:
    print(f"{surname} {name}")