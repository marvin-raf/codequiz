from flask import Blueprint

courses_module = Blueprint("courses", __name__, url_prefix="/courses")


@courses_module.route("/")
def helloworld():
    """
    Print hello world
    """

    return "helloworld"
