from flask import Blueprint

students_module = Blueprint("students", __name__, url_prefix="/students")


@students_module.route("/")
def helloworld():
    """
    Print hello world
    """

    return "helloworld"
