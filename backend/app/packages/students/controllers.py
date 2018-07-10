import os
import uuid
import xlrd
from flask import Blueprint, request, abort, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from config import config
from app.packages.students import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import student_signed_in

students_module = Blueprint("students", __name__, url_prefix="/students")


@students_module.route("/activate", methods=["POST"])
@cross_origin
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

    return created()


@students_module.route("/parse", methods=["POST"])
@cross_origin
def parse():
    """
    Parses an excel spreadsheet and returns students
    """

    try:
        if "excel_doc" not in request.files:
            return bad_request()

        excel_doc = request.files["excel_doc"]

        if not models.allowed_file(excel_doc.filename):
            return bad_request()

        file_path = models.save_excel_doc(excel_doc)

        students = models.parse_students(file_path)

        os.remove(file_path)
    except ValueError as e:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success(students)
