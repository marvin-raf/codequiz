from flask import Blueprint, request, abort, jsonify
from app.packages.teachers import models
from app.util.responses import success, bad_request, server_error, created

teachers_module = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers_module.route("/signup", methods=["POST"])
def signup():
    """
    Signs a teacher up and inserts info into db
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
