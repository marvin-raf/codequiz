"""
"""

from flask import Flask
from flask_cors import CORS

from app.packages.auth.controllers import auth_module
from app.packages.students.controllers import students_module
from app.packages.teachers.controllers import teachers_module
from app.packages.quizzes.controllers import quizzes_module
from app.packages.courses.controllers import courses_module
from app.packages.classes.controllers import classes_module


def create_app():
    """
    Create the flask application
    """

    flask_app = Flask(__name__)

    flask_app.config["UPLOAD_FOLDER"] = "img/"
    CORS(flask_app)

    flask_app.config['CORS_HEADERS'] = 'Content-Type'

    flask_app.register_blueprint(auth_module)
    flask_app.register_blueprint(students_module)
    flask_app.register_blueprint(teachers_module)
    flask_app.register_blueprint(quizzes_module)
    flask_app.register_blueprint(courses_module)
    flask_app.register_blueprint(classes_module)

    return flask_app


app = create_app()
