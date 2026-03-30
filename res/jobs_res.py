from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument("team_leader", required=True, type=int)
parser.add_argument("job", required=True, type=int)
parser.add_argument("work_size", required=True, type=int)
parser.add_argument("collaborators", required=True, type=int)
parser.add_argument("start_date", required=True, type=int)
parser.add_argument("end_date", required=True, type=int)
parser.add_argument("is_finished", required=True, type=int)


def abort_if_jobs_not_found(news_id, jobs_id=None):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(news_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")

class JobsRes(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify(jobs.to_dict(only=("id", "team_leader",
                          "job", "work_size",
                          "collaborators", "start_date",
                          "end_date", "is_finished")))
    def __delete__(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({"success": "ok"})


class JobsListRes(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            (jobs.to_dict(only=("id", "team_leader",
                                "job", "work_size",
                                "collaborators", "start_date",
                                "end_date", "is_finished")))
        })
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(

        )
        session.add(jobs)
        session.commit()
        return jsonify({"id": jobs.id})