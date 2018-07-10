from flask import Blueprint, request, abort, jsonify
from app.packages.classes import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_signed_in, class_exists

classes_module = Blueprint("classes", __name__, url_prefix="/classes")


@classes_module.route("/", methods=["GET"])
@teacher_signed_in
def get_classes():
    """
    Gets all of a teachers classes
    """
    try:
        teacher_id = request.teacher_id

        classes = models.get_classes(teacher_id)

    except Exception:
        return server_error
    return success({"classes": classes})


@classes_module.route("/", methods=["POST"])
@teacher_signed_in
def create():
    """
    Creates a class
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        name = body["name"]

        if not name:
            return bad_request()

        class_id = models.insert_class(teacher_id, name)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created({"class_id": class_id})


@classes_module.route("/<class_id>", methods=["PATCH"])
@teacher_signed_in
@class_exists
def change_class(class_id):
    """
    Changes information about a class
    """
    try:
        body = request.get_json()

        name = body["name"]

        if not name:
            return bad_request()

        models.change_class(class_id, name)

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return success()


@classes_module.route("/<class_id>", methods=["DELETE"])
@teacher_signed_in
@class_exists
def delete_class(class_id):
    """
    Deletes a class
    """
    try:
        models.delete_class(class_id)

    except Exception:
        return server_error()
    return success()


@classes_module.route("/<class_id>/students", methods=["GET"])
@teacher_signed_in
@class_exists
def get_students(class_id):
    """
    Gets all the students of a class
    """
    try:
        students = models.get_students(class_id)

    except Exception:
        return server_error()
    return success({"students": students})


@classes_module.route("/<class_id>/students", methods=["POST"])
@teacher_signed_in
@class_exists
def add_students(class_id):
    """
    Adds students to the database
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        students = body["students"]

        student_list = models.insert_students(students, teacher_id)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()
    return created({"students": student_list})
