from flask import Blueprint, request, abort, jsonify

from app.packages.auth import models
from app.util.responses import success, bad_request, server_error, created
from app.util.middleware import teacher_student_logged_in

auth_module = Blueprint("auth", __name__, url_prefix="/auth")


@auth_module.route("/signin", methods=["POST"])
def signin():
    """
    Signs in either a teacher or a student
    """
    try:
        body = request.get_json()

        email = body["email"]
        password = body["password"]
        # Returns the user_id (either teacher or student) and if the user is a teacher or a student
        user_id, is_teacher = models.id_from_credentials(email, password)

        if not user_id:
            return bad_request()

        token = models.create_token()
        models.save_token(token, user_id, is_teacher)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success({
        "token": token,
        "teacher_id" if is_teacher else "student_id": user_id
    })


@auth_module.route("/signout", methods=["POST"])
@teacher_student_logged_in
def signout():
    """
    Signs a teacher or student out by changing their token to null
    """
    try:
        if hasattr(request, "teacher_id"):
            user_id = request.teacher_id
            is_teacher = True
        else:
            user_id = request.student_id
            is_teacher = False

        models.remove_token(user_id, is_teacher)

    except Exception as e:
        print(e)
        return server_error()
    return success()
