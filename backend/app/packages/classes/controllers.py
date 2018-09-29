from flask import Blueprint, request, abort, jsonify
from app.packages.classes import models
from app.util.responses import success, bad_request, server_error, created, forbidden, not_found
from app.util.middleware import teacher_signed_in, teacher_owns_class

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
        return server_error()
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
@teacher_owns_class
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
@teacher_owns_class
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
@teacher_owns_class
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
@teacher_owns_class
def add_students(class_id):
    """
    Adds students to the database
    """
    try:
        body = request.get_json()

        teacher_id = request.teacher_id
        students = body["students"]
        emails = []

        for email in students:
            emails.append(email["email"])

        models.insert_students(students, teacher_id)
        models.delete_unique()
        models.insert_into_class(class_id, tuple(emails))

    except KeyError:
        return bad_request()
    except Exception:
        return server_error()
    return created()


@classes_module.route("/<class_id>/students", methods=["DELETE"])
@teacher_signed_in
@teacher_owns_class
def delete_students(class_id):
    """
    Deletes all students in a class
    """
    try:
        models.delete_students(class_id)

    except Exception:
        return server_error()
    return success()


@classes_module.route("/<class_id>/students/<student_id>", methods=["DELETE"])
@teacher_signed_in
@teacher_owns_class
def delete_student(class_id, student_id):
    """
    Deletes a student from a class
    """
    try:
        if not models.check_student(class_id, student_id):
            return not_found()

        models.delete_student(class_id, student_id)

    except Exception:
        return server_error()
    return success()
