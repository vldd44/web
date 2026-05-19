import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from data import db_session
from data.users import User
from data.jobs import Jobs


db_name = input().strip()
db_session.global_init(f"db/{db_name}")
session = db_session.create_session()

jobs = session.query(Jobs).all()

job_sizes = []
for job in jobs:
    if job.collaborators:
        collaborators_list = [c.strip() for c in job.collaborators.split(',') if c.strip()]
        count = len(collaborators_list)
    else:
        count = 0
    job_sizes.append((job, count))

max_size = max(size for _, size in job_sizes) if job_sizes else 0

leaders_set = set()
for job, size in job_sizes:
    if size == max_size:
        leader = session.query(User).filter(User.id == job.team_leader).first()
        if leader:
            leaders_set.add((leader.surname, leader.name))

for surname, name in sorted(leaders_set):
    print(f"{surname} {name}")