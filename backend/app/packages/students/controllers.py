from flask import Blueprint, request, abort, jsonify
from pymysql import MySQLError
from app.packages.students import models
from app.util.responses import success, bad_request, server_error, created

students_module = Blueprint("students", __name__, url_prefix="/students")


@students_module.route("/courses", methods=["GET"])
def courses():
    """
    Let's the students view their courses
    """


@students_module.route("/activate", methods=["POST"])
def activate():
    """
    Activates a student account and set's there password
    """
    try:
        body = request.get_json()

        student_activate_token = body["student_activate_token"]
        student_password = body["student_password"]

        if len(student_password) < 3 or len(student_password) > 50:
            return bad_request()

        if not models.token_exists(student_activate_token):
            return bad_request()

        student_hash = models.create_hash(student_password)
        models.save_hash(student_hash, student_activate_token)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()


@students_module.route("/signin", methods=["POST"])
def signin():
    """
    Signs a student in and returns their signin token
    """

    try:
        body = request.get_json()

        if not "student_email" in body or not "student_password" in body:
            return ("", 400)

        student_email = body["student_email"]
        student_password = body["student_password"]
        student_id = models.id_from_credentials(student_email,
                                                student_password)

        if not student_id:
            return ("", 400)

        student_token = models.create_token()
        models.save_token(student_token, student_id)

        return jsonify({"token": student_token})

    except MySQLError:
        return ("", 500)
