from flask import Blueprint, request, abort, jsonify
from app.packages.teachers import models
from app.util.responses import success, bad_request, server_error, created
from app.util.middleware import teacher_signed_in

teachers_module = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers_module.route("/me", methods=["GET"])
@teacher_signed_in
def me():
    """
    Returns teachers data if they are logged in
    """

    try:
        teacher_data = models.get_teacher_data(request.teacher_id)
    except Exception as e:
        print(e)
        return server_error()

    return success(teacher_data)


@teachers_module.route("/signup", methods=["POST"])
def signup():
    """
    Signs a teacher up and returns their id
    """
    try:
        body = request.get_json()

        name = body["name"]
        email = body["email"]
        password = body["password"]

        # Checks if email is taken in the teacher or student table
        if models.taken_email(email):
            return bad_request()

        teacher_hash = models.create_hash(password)
        teacher_id = models.insert_teacher(name, email, teacher_hash)
    except KeyError:
        return bad_request()
    except Exception:
        return server_error()

    return created({"teacher_id": teacher_id})
