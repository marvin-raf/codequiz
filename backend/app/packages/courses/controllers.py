from flask import Blueprint, request, abort, jsonify
from app.packages.courses import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_signed_in

courses_module = Blueprint("courses", __name__, url_prefix="/courses")


@courses_module.route("/", methods=["GET"])
@teacher_signed_in
def get_courses():
    """
    Gets all of a teachers courses
    """
    try:
        teacher_id = request.teacher_id

        courses = models.get_courses(teacher_id)

    except Exception:
        return server_error()
    return success({"courses": courses})


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


@courses_module.route("/<course_id>", methods=["GET"])
@teacher_signed_in
def get_course(course_id):
    """
    Gets information on one course
    """
    try:
        teacher_id = request.teacher_id

        if not models.course_exists(course_id, teacher_id):
            return bad_request()

        course = models.get_course(course_id)

    except Exception:
        return server_error()
    return success(course[0])


@courses_module.route("/<course_id>/quizzes", methods=["GET"])
@teacher_signed_in
def get_quizzes(course_id):
    """
    Gets all of a courses quizzes
    """
    try:
        teacher_id = request.teacher_id

        if not models.course_exists(course_id, teacher_id):
            return bad_request()

        quizzes = models.get_quizzes(course_id)

    except Exception:
        return server_error()
    return success({"quizzes": quizzes})


@courses_module.route("/<course_id>/quizzes", methods=["POST"])
@teacher_signed_in
def create_quiz(course_id):
    """
    Creates a quiz
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
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