from flask import Blueprint, request, abort, jsonify
from app.packages.students import models
from app.util.responses import success, bad_request, server_error, created, forbidden

students_module = Blueprint("students", __name__, url_prefix="/students")


@students_module.route("/activate", methods=["POST"])
def activate():
    """
    Activates a student account and set's there password
    """
    try:
        body = request.get_json()

        activate_token = body["activate_token"]
        password = body["password"]

        if len(password) < 3 or len(password) > 50:
            return bad_request()

        if not models.token_exists(activate_token):

            return bad_request()

        student_hash = models.create_hash(password)
        models.save_hash(student_hash, activate_token)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success()


@students_module.route("/signin", methods=["POST"])
def signin():
    """
    Signs a student in and returns their signin token
    """

    try:
        body = request.get_json()

        email = body["email"]
        password = body["password"]
        student_id = models.id_from_credentials(email, password)

        if not student_id:
            return bad_request()

        token = models.create_token()
        models.save_token(token, student_id)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success({"token": token, "student_id": student_id})
