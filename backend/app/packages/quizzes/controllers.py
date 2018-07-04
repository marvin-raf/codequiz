from flask import Blueprint

quizzes_module = Blueprint("quizzes", __name__, url_prefix="/quizzes")


@quizzes_module.route("/")
def helloworld():
    """
    Print hello world
    """

    return "helloworld"
