from data import db_session
from data.users import User
from flask_restful import abort, Resource
from flask import jsonify


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"users {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify(users.to_dict(only=("id", "surname",
                                           "name", "age",
                                           "position", "speciality",
                                           "address", "email", "hashed_password", "modified_date")))

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        jobs = session.query(User).get(user_id)
        session.delete(jobs)
        session.commit()
        return jsonify({"success": "ok"})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            "users": [
                user.to_dict(
                    only=("id", "surname",
                          "name", "age",
                          "position", "speciality",
                          "address", "email", "hashed_password", "modified_date")
                ) for user in users
            ]
        })
