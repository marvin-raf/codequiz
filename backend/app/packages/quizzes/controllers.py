from flask import Blueprint, request, abort, jsonify
from app.packages.quizzes import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_signed_in

quizzes_module = Blueprint("quizzes", __name__, url_prefix="/quizzes")


@quizzes_module.route("/", methods=["POST"])
@teacher_signed_in
def create():
    """
    Creates a quiz
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        course_id = body["course_id"]
        name = body["name"]
        start_date = body["start_date"]
        end_date = body["end_date"]

        if not models.course_exists(course_id,
                                    teacher_id) or not models.check_dates(
                                        start_date, end_date):
            return bad_request()

        quiz_id = models.insert_quiz(course_id, name, start_date, end_date)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created({"quiz_id": quiz_id})
