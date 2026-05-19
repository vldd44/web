from data import db_session
from data.users import User
from flask_restful import abort, Resource
<<<<<<< HEAD
from flask import jsonify, request
from hashlib import md5
=======
from flask import jsonify
>>>>>>> f80b3e89f58f152c46ecada6a4826b4c8c0ba58f


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
<<<<<<< HEAD
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({"success": "ok"})

    def put(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)

        if not user:
            abort(404, message=f"User {user_id} not found")

        args = request.json
        if "surname" in args:
            user.surname = args["surname"]
        if "name" in args:
            user.name = args["name"]
        if "age" in args:
            user.age = args["age"]
        if "position" in args:
            user.position = args["position"]
        if "speciality" in args:
            user.speciality = args["speciality"]
        if "address" in args:
            user.address = args["address"]
        if "email" in args:
            user.email = args["email"]
        if "password" in args:
            user.hashed_password = md5(args["password"].encode()).hexdigest()

=======
        jobs = session.query(User).get(user_id)
        session.delete(jobs)
>>>>>>> f80b3e89f58f152c46ecada6a4826b4c8c0ba58f
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
<<<<<<< HEAD

    def post(self):
        args = request.json
        user = User(
            surname=args.get("surname"),
            name=args.get("name"),
            age=args.get("age"),
            position=args.get("position"),
            speciality=args.get("speciality"),
            address=args.get("address"),
            email=args.get("email")
        )
        if "password" in args:
            user.hashed_password = md5(args["password"].encode()).hexdigest()

        session = db_session.create_session()
        session.add(user)
        session.commit()
        return jsonify({"id": user.id})
=======
>>>>>>> f80b3e89f58f152c46ecada6a4826b4c8c0ba58f
