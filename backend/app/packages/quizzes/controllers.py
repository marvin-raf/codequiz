from flask import Blueprint, request, abort, jsonify
from app.packages.quizzes import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_student_logged_in, teacher_owns_quiz

quizzes_module = Blueprint("quizzes", __name__, url_prefix="/quizzes")


@quizzes_module.route("/<quiz_id>", methods=["GET"])
@teacher_student_logged_in
@teacher_owns_quiz
def get_quiz(quiz_id):
    """
    Gets quiz information along with questions for one quiz
    """

    try:
        quiz_name = models.get_name(quiz_id)
        questions = models.get_questions(quiz_id)
        questions_with_tests = models.get_tests(questions)
    except Exception as e:
        print(e)
        return server_error()

    return success({"quiz_name": quiz_name, "questions": questions_with_tests})
