from sqlalchemy.sql.operators import json_path_getitem_op

from data import db_session
from data.jobs import Jobs
from flask_restful import abort, Resource
from flask import jsonify


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify(jobs.to_dict(only=("id", "team_leader",
                                          "job", "work_size",
                                          "collaborators", "start_date",
                                          "end_date", "is_finished")))

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({"success": "ok"})



class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            "jobs": [
                job.to_dict(
                    only=("id", "team_leader",
                          "job", "work_size",
                          "collaborators", "start_date",
                          "end_date", "is_finished")
                ) for job in jobs
            ]
        })