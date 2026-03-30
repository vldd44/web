from flask import Blueprint, request, jsonify
from data import db_session
from data.jobs import Jobs

api = Blueprint(
    "jobs_api",
    __name__,
    template_folder="templates"
)


@api.route("/api/jobs", methods=["GET", "POST"])
def jobs():
    if request.method == "GET":
        session = db_session.create_session()
        jobs_items = session.query(Jobs).all()
        return jsonify({
            "jobs": [
                job.to_dict(
                    only=("id", "team_leader",
                          "job", "work_size",
                          "collaborators", "start_date",
                          "end_date", "is_finished")
                ) for job in jobs_items
            ]
        })
    elif request.method == "POST":
        jobs_json = request.get_json()
        job = Jobs(
            collaborators=jobs_json["collaborators"],
            is_finished=jobs_json["is_finished"],
            end_date=jobs_json["end_date"],
            start_date=jobs_json["start_date"],
            job=jobs_json["job"],
            team_leader=jobs_json["team_leader"],
            work_size=jobs_json["work_size"]
        )
        session = db_session.create_session()
        job = session.merge(job)
        session.commit()
        return jsonify({"id": job.id}), 201
    return jsonify({"error": "Method Not Allowed"}), 405


@api.route("/api/jobs/<int:job_id>", methods=["GET", "DELETE", "PUT"])
def one_jobs(job_id):
    if request.method == "GET":
        session = db_session.create_session()
        jobs_item = session.query(Jobs).filter(
            Jobs.id == job_id
        ).first()
        return jsonify(jobs_item.to_dict(
                    only=("id", "team_leader",
                          "job", "work_size",
                          "collaborators", "start_date",
                          "end_date", "is_finished")
                ))
    return jsonify({"error": "Method Not Allowed"}), 405
