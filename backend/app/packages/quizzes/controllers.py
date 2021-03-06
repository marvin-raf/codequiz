import os
from flask import Blueprint, request, abort, jsonify
from pylint.lint import Run
import subprocess
import uuid
from app.packages.quizzes import models
from app.packages.quizzes.code_runner import CodeRunner
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_student_logged_in, teacher_signed_in, student_signed_in, teacher_owns_quiz, can_access_quiz_instance, question_exists, signed_in_or_out, test_case_exists

quizzes_module = Blueprint("quizzes", __name__, url_prefix="/quizzes")


@quizzes_module.route("/", methods=["GET"])
@teacher_signed_in
def get_quizzes():
    """
    Gets all the quizzes that the teacher owns
    """

    try:
        quizzes = models.get_quizzes(request.teacher_id)
    except Exception as e:
        print(e)
        return server_error()

    return success(quizzes)


@quizzes_module.route("/free", methods=["GET"])
def get_free_quizzes():
    """
    Gets all the free quizzes
    """

    try:
        free_quizzes = models.get_free_quizzes()
    except Exception as e:
        print(e)
        return server_error()

    return success(free_quizzes)


@quizzes_module.route("/free", methods=["POST"])
def create_free_quizzes():
    """
    Creates a free quiz
    """

    try:
        json = request.get_json()

        quiz_name = json["quiz_name"]
        quiz_language_id = json["quiz_language_id"]
        quiz_short_desc = json["quiz_short_desc"]

        models.create_free_quiz(quiz_name, quiz_language_id, quiz_short_desc)
    except KeyError as e:
        print(e)
        return bad_request()
    # Error checking will be done in create_free_quiz route and will return ValueError if so
    except ValueError as e:
        print(e)
        return bad_request()
    except Exception:
        return server_error()

    return created()


@quizzes_module.route("/instance/<qc_id>", methods=["GET"])
@signed_in_or_out
@can_access_quiz_instance
def get_quiz_instance(qc_id):
    """
    Gets quiz information along with questions for one quiz
    """
    try:
        quiz = models.get_quiz_instance(qc_id)
        questions = models.get_questions(quiz["quiz_id"])

        questions_with_tests = models.get_tests(questions, request.student_id
                                                if hasattr(
                                                    request, "student_id") else
                                                None)
    except Exception as e:
        print(e)
        return server_error()

    return success({"quiz": quiz, "questions": questions_with_tests})


@quizzes_module.route("/template/<quiz_id>", methods=["GET"])
@teacher_signed_in
@teacher_owns_quiz
def get_quiz_template(quiz_id):
    """
    Gets quiz information along with questions for one quiz
    """
    try:
        quiz = models.get_quiz_template(quiz_id)
        questions = models.get_questions(quiz_id)

        questions_with_tests = models.get_tests(questions, None)

    except Exception as e:
        print(e)
        return server_error()

    return success({"quiz": quiz, "questions": questions_with_tests})


@quizzes_module.route("/<quiz_id>", methods=["PATCH"])
@teacher_signed_in
@teacher_owns_quiz
def edit_quiz(quiz_id):
    """
    Changes quiz info
    """
    try:
        body = request.get_json()

        name = body["name"]
        start_date = body["start_date"]
        end_date = body["end_date"]
        description = body["description"]
        language = body["language"]

        if not models.check_dates(
                start_date, end_date) and not models.check_languages(language):
            return bad_request()

        models.edit_quiz(quiz_id, name, start_date, end_date, description,
                         language)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()
    return success()


@quizzes_module.route("/<quiz_id>/questions", methods=["POST"])
@teacher_signed_in
@teacher_owns_quiz
def questions(quiz_id):
    """
    Adds one question to a quiz
    """

    try:
        json = request.get_json()

        description = json["description"]

        question_id = models.add_question(quiz_id, description)
    except KeyError:
        return bad_request()
    except Exception as e:
        return server_error()

    return created({"question_id": question_id})


@quizzes_module.route("/<quiz_id>/questions/<question_id>", methods=["PUT"])
@teacher_signed_in
@teacher_owns_quiz
@question_exists
def update_question(quiz_id, question_id):
    """
    Updates a question from a quiz
    """

    try:
        json = request.get_json()

        question_description = json["question_description"]

        models.update_description(question_description, question_id)

    except (KeyError, ValueError):
        return bad_request()
    except Exception as e:
        return server_error()

    return success()


@quizzes_module.route("/<quiz_id>/questions/<question_id>", methods=["DELETE"])
@teacher_signed_in
@teacher_owns_quiz
@question_exists
def delete_question(quiz_id, question_id):
    """
    Deletes a question from a quiz
    """

    try:
        models.delete_question(quiz_id, question_id)
    except Exception as e:
        print(e)
        return server_error()

    return success()


@quizzes_module.route(
    "/<qc_id>/questions/<question_id>/precheck", methods=["POST"])
@signed_in_or_out
@can_access_quiz_instance
@question_exists
def precheck(qc_id, question_id):
    """
    Adds one question to a quiz
    """

    try:
        student_id = request.student_id if hasattr(request,
                                                   "student_id") else str(
                                                       uuid.uuid4().hex)

        body = request.get_json()

        code = body["code"]

        filename = models.precheck_file_name(student_id, qc_id, question_id)
        filepath = os.path.join("app", "packages", "quizzes", "question_files",
                                filename)

        with open(filepath, "w") as f:
            f.write(code)

        bashCommand = "pylint --errors-only {}".format(filepath)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        process.wait()
        output, _ = process.communicate()

        os.remove(filepath)

    except KeyError:
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success({"output": output.decode()})


@quizzes_module.route(
    "/<qc_id>/questions/<question_id>/check", methods=["POST"])
@signed_in_or_out
@can_access_quiz_instance
@question_exists
def check(qc_id, question_id):
    """
    Checks students code for a particular question against test cases
    """
    try:
        # If user is not a student, assign them random uuid for filename
        student_id = request.student_id if hasattr(request,
                                                   "student_id") else str(
                                                       uuid.uuid4().hex)
        body = request.get_json()

        code = body["code"]

        code_runner = CodeRunner(student_id, qc_id, question_id)

        code_runner.write_code(code)  # Writes students code to file

        test_cases = models.get_test_cases(question_id)

        # question_worth, total_negated and last_attempt_wrong only valid for free quiz!
        results, question_worth, total_negated, last_attempt_wrong = code_runner.run(
            test_cases)

        code_runner.remove_code()  # Deletes students code

        # If user is not student or the quiz is a free quiz, then don't save their attempt
        if hasattr(request, "is_free_quiz"):
            return success({
                "results": results,
                "question_worth": question_worth,
                "total_negated": total_negated,
                "last_attempt_wrong": last_attempt_wrong
            })

        attempt_id = models.insert_attempt(question_id, student_id)

        models.insert_test_cases(results, attempt_id)

        question_worth, total_negated, last_attempt_wrong = models.get_mark_worth(
            question_id, student_id)
    except KeyError as e:
        print(e)
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return success({
        "results": results,
        "question_worth": question_worth,
        "total_negated": total_negated,
        "last_attempt_wrong": last_attempt_wrong
    })


@quizzes_module.route("/languages", methods=["GET"])
def get_languages():
    """
    Gets all supported programming languages
    """

    try:
        languages = models.get_languages()
        return success(languages)
    except Exception as e:
        print(e)
        return server_error()


@quizzes_module.route(
    "/<quiz_id>/questions/<question_id>/testcase", methods=["POST"])
@teacher_signed_in
@teacher_owns_quiz
@question_exists
def create_test_case(quiz_id, question_id):
    """
    Creates a test case
    """

    try:
        json = request.get_json()

        test_input = json["test_input"]
        test_expected = json["test_expected"]

        test_id = models.create_test_case(question_id, test_input,
                                          test_expected)
    except (KeyError, ValueError):
        return bad_request()
    except Exception as e:
        print(e)
        return server_error()

    return created({"test_id": test_id})


@quizzes_module.route(
    "/<quiz_id>/questions/<question_id>/testcase/<test_id>",
    methods=["DELETE"])
@teacher_signed_in
@teacher_owns_quiz
@question_exists
@test_case_exists
def delete_test_case(quiz_id, question_id, test_id):
    """
    Creates a test case
    """

    try:
        models.delete_test_case(test_id)
    except Exception:
        return server_error()

    return success()
