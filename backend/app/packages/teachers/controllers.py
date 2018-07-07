from flask import Blueprint, request, abort, jsonify
from app.packages.teachers import models
from app.util.responses import success, bad_request, server_error, created
from app.util.middleware import teacher_signed_in

teachers_module = Blueprint("teachers", __name__, url_prefix="/teachers")


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

        if models.taken_email(email):
            return bad_request()

        teacher_hash = models.create_hash(password)
        teacher_id = models.insert_teacher(name, email, teacher_hash)
    except KeyError:
        return bad_request()
    except Exception:
        return server_error()

    return created({"teacher_id": teacher_id})


@teachers_module.route("/signin", methods=["POST"])
def signin():
    """
    Signs a teacher in and returns their id and token
    """
    try:
        body = request.get_json()

        email = body["email"]
        password = body["password"]
        teacher_id = models.id_from_credentials(email, password)

        if not teacher_id:
            return bad_request()

        token = models.create_token()
        models.save_token(token, teacher_id)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()

    return success({"token": token, "teacher_id": teacher_id})


@teachers_module.route("/signout", methods=["POST"])
@teacher_signed_in
def signout():
    """
    Signs a teacher out by changing their token to null
    """
    try:
        teacher_id = request.teacher_id

        models.remove_token(teacher_id)

    except Exception:
        return server_error()
    return success()
