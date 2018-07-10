from flask import Blueprint, request, abort, jsonify
from flask_cors import cross_origin
from app.packages.teachers import models
from app.util.responses import success, bad_request, server_error, created
from app.util.middleware import teacher_signed_in

teachers_module = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers_module.route("/signup", methods=["POST"])
@cross_origin()
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
