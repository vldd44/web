from flask import jsonify
from flask_restful import abort, Resource, reqparse
from data import db_session, users
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument("surname", required=True, type=int)
parser.add_argument("name", required=True, type=int)
parser.add_argument("position", required=True, type=int)
parser.add_argument("speciality", required=True, type=int)
parser.add_argument("address", required=True, type=int)
parser.add_argument("email", required=True, type=int)
parser.add_argument("hashed_password", required=True, type=int)
parser.add_argument("modified_date", required=True, type=int)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    jobs = session.query(User).get(user_id)
    if not User:
        abort(404, message=f"Users {user_id} not found")

class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        jobs = session.query(User).get(user_id)
        return jsonify(users.to_dict(only=("id", "surname",
                          "name", "age",
                          "position", "speciality",
                          "address", "email", "hashed_password", "modified_date")))

    def __delete__(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({"success": "ok"})

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            (users.to_dict(only=("id", "surname",
                                 "name", "age",
                                 "position", "speciality",
                                 "address", "email", "hashed_password", "modified_date")))
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(

        )
        session.add(users)
        session.commit()
        return jsonify({"id": users.id})