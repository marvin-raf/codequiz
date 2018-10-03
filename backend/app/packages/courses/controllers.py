from flask import Blueprint, request, abort, jsonify
from app.packages.courses import models
from app.util.responses import success, bad_request, server_error, created, forbidden, not_found
from app.util.middleware import teacher_signed_in, course_exists

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

        if not name:
            return bad_request()

        course_id = models.insert_course(teacher_id, name)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created({"course_id": course_id})


@courses_module.route("/<course_id>", methods=["GET"])
@teacher_signed_in
@course_exists
def get_course(course_id):
    """
    Gets information on one course
    """
    try:
        name = models.get_name(course_id)
        quizzes = models.get_quizzes(course_id)
        classes = models.get_classes(course_id)

    except Exception as e:
        print(e)
        return server_error()
    return success({
        "course_id": course_id,
        "course_name": name,
        "course_quizzes": quizzes,
        "course_classes": classes
    })


@courses_module.route("/<course_id>", methods=["PATCH"])
@teacher_signed_in
@course_exists
def change_course(course_id):
    """
    Changes name of a course
    """
    try:
        body = request.get_json()

        name = body["name"]

        if not name:
            return bad_request()

        models.change_course(course_id, name)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return success()


@courses_module.route("/<course_id>", methods=["DELETE"])
@teacher_signed_in
@course_exists
def delete_course(course_id):
    """
    Deletes a course
    """
    try:
        models.delete_course(course_id)

    except Exception:
        return server_error()
    return success()


@courses_module.route("/<course_id>/quizzes", methods=["POST"])
@teacher_signed_in
@course_exists
def create_quiz(course_id):
    """
    Creates a quiz
    """
    try:
        body = request.get_json()

        name = body["name"]
        start_date = body["start_date"]
        end_date = body["end_date"]
        description = body["description"]
        language = body["language"]

        if not models.check_dates(
                start_date, end_date) and not models.check_languages(language):
            return bad_request()

        quiz_id = models.insert_quiz(course_id, name, start_date, end_date,
                                     description, language)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created({"quiz_id": quiz_id})


@courses_module.route("<course_id>/classes", methods=["POST"])
@teacher_signed_in
@course_exists
def add_class(course_id):
    """
    Adds a class to a course
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        class_id = body["id"]

        if not models.class_exists(teacher_id, class_id):
            return bad_request()

        models.add_class(course_id, class_id)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return success()


@courses_module.route("<course_id>/classes/<class_id>", methods=["DELETE"])
@teacher_signed_in
@course_exists
def delete_class(course_id, class_id):
    """
    Deletes a class from a course
    """
    try:
        teacher_id = request.teacher_id

        if not models.class_exists(teacher_id, class_id):
            return not_found()

        models.delete_class(course_id, class_id)

    except Exception:
        return server_error()
    return success()
