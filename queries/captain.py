from data.users import User
from data import db_session

db_session.global_init("../db/mars_explorer.db")
db_sess = db_session.create_session()

captain = User()
captain.surname = "Scott"
captain.name = "Ridley"
captain.age = 21
captain.position = "captain"
captain.speciality = "research engineer"
captain.address = "module_1"
captain.email = "scott_chief@mars.org"

db_sess.add(captain)

engineer = User()
engineer.surname = "Lifts"
engineer.name = "John"
engineer.age = 21
engineer.position = "engineer"
engineer.speciality = "mechanical engineer"
engineer.address = "module_1"
engineer.email = "johny_se@mars.org"
db_sess.add(engineer)

medic = User()
medic.surname = "Romanov"
medic.name = "Foren"
medic.age = 30
medic.position = "doctor"
medic.speciality = "paramedic"
medic.address = "module_1"
medic.email = "foren_fastest@mars.org"
db_sess.add(medic)

scientist = User()
scientist.surname = "Volkov"
scientist.name = "Felix"
scientist.age = 46
scientist.position = "scientist"
scientist.speciality = "astrobiologist"
scientist.address = "module_1"
scientist.email = "felix_not_rd@mars.org"
db_sess.add(scientist)

db_sess.commit()