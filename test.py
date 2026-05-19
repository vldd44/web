import requests
from datetime import datetime

response = requests.post("http://127.0.0.1:8080/api/jobs", json={"collaborators":"2, 3",
 "end_date": datetime.now().isoformat(),
 "is_finished": False,
 "job":"deployment of residential modules 1 and 2",
 "start_date": datetime.now().isoformat(),
 "team_leader":1,
 "work_size":15})
if response.status_code == 201:
    print(response.json())
else:
    print(f"{response.status_code} {response.reason}")

response = requests.post("http://127.0.0.1:8080/api/jobs", json={"collaborators":"2, 3",
 "end_date": datetime.now().isoformat(),
 "is_finished": False,
 "job":"deployment of residential modules 1 and 2",
 "start_date": datetime.now().isoformat(),
 "team_leader": -1, # тим лидера НЕТ
 "work_size": 15})
if response.status_code == 200:
    print(response.json())
else:
    print(f"{response.status_code} {response.reason}")

response = requests.post("http://127.0.0.1:8080/api/jobs", json={"collaborators":"2, 3",
 "end_date": "null", #не подойдёт под datetime
 "is_finished": False,
 "job":"deployment of residential modules 1 and 2",
 "start_date": datetime.now().isoformat(),
 "team_leader":1,
 "work_size":15})
if response.status_code == 200:
    print(response.json())
else:
    print(f"{response.status_code} {response.reason}")

response = requests.post("http://127.0.0.1:8080/api/jobs", json={"collaborators":"2, 3",
 "end_date": datetime.now().isoformat(),
 "is_finished": 220, # инт не пойдёт для буллиена
 "job":"deployment of residential modules 1 and 2",
 "start_date": datetime.now().isoformat(),
 "team_leader":1,
 "work_size":15})
if response.status_code == 200:
    print(response.json())
else:
    print(f"{response.status_code} {response.reason}")