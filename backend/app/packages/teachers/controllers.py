from flask import Blueprint

teachers_module = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers_module.route("/")
def helloworld():
    """
    Print hello world
    """

    return "helloworld"
