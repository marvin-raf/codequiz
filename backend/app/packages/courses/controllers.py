from flask import Blueprint, request, abort, jsonify
from app.packages.courses import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_signed_in

courses_module = Blueprint("courses", __name__, url_prefix="/courses")


@courses_module.route("/", methods=["POST"])
@teacher_signed_in
def create():
    """
    Creates a course
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        name = body["name"]

        course_id = models.insert_course(teacher_id, name)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created({"course_id": course_id})
