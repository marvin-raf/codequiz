"""
Middleware functions
"""
import time
from functools import wraps
from flask import request
from app.util import db
from app.util.responses import unauthorized, bad_request, not_found, forbidden


def student_signed_in(func):
    """
    Checks to see if the student is authenticated or not.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if not "Student-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT student_id
        FROM students
        WHERE student_token = %s
        """

        rows = db.query(query, (request.headers["Student-Authorization"]))

        if not rows:
            return unauthorized()

        request.student_id = rows[0]["student_id"]
        return func(*args, **kwargs)

    return wrap


def signed_in_or_out(func):
    """
    Checks if a teacher or student is signed in or out and saves the student or
    teacher in context if they are signed in
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Checks if the user is signed in as either a student or a teacher
        """

        if "Teacher-Authorization" in request.headers:
            query = """
            SELECT teacher_id 
            FROM teachers 
            WHERE teacher_token = %s
            """

            rows = db.query(query, (request.headers["Teacher-Authorization"]))

            if rows:
                request.teacher_id = rows[0]["teacher_id"]

        elif "Student-Authorization" in request.headers:
            query = """
            SELECT student_id 
            FROM students 
            WHERE student_token = %s
            """

            rows = db.query(query, (request.headers["Student-Authorization"]))

            if rows:
                request.student_id = rows[0]["student_id"]

        # If no user is authenticated, then go to next middleware
        return func(*args, **kwargs)

    return wrap


def teacher_signed_in(func):
    """
    Checks to see if the teacher is authenticated or not.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if not "Teacher-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT teacher_is_admin, teacher_id
        FROM teachers 
        WHERE teacher_token = %s
        """

        rows = db.query(query, (request.headers["Teacher-Authorization"]))

        if not rows:
            return unauthorized()

        if rows[0]["teacher_is_admin"]:
            request.teacher_is_admin = True

        request.teacher_id = rows[0]["teacher_id"]
        return func(*args, **kwargs)

    return wrap


def teacher_owns_class(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        teacher_id = request.teacher_id
        class_id = request.view_args["class_id"]

        query = """
        SELECT * FROM classes
        WHERE class_id = %s
        """

        classes = db.query(query, (class_id))

        if not classes:
            return not_found()

        query = """
        SELECT * FROM classes
        WHERE class_id = %s
        AND class_teacher_id = %s
        """

        classes = db.query(query, (class_id, teacher_id))

        if not classes:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def course_exists(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        teacher_id = request.teacher_id
        course_id = request.view_args["course_id"]

        query = """
        SELECT * FROM courses
        WHERE course_id = %s
        """

        courses = db.query(query, (course_id))

        if not courses:
            return not_found()

        query = """
        SELECT * FROM courses
        WHERE course_id = %s
        AND course_teacher_id = %s
        """

        courses = db.query(query, (course_id, teacher_id))

        if not courses:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def teacher_student_logged_in(func):
    """
    Checks to see if a student or a teacher is signed in.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if "Teacher-Authorization" in request.headers:
            query = """
            SELECT teacher_id 
            FROM teachers 
            WHERE teacher_token = %s
            """

            rows = db.query(query, (request.headers["Teacher-Authorization"]))

            if not rows:
                return unauthorized()

            request.teacher_id = rows[0]["teacher_id"]
            return func(*args, **kwargs)
        elif "Student-Authorization" in request.headers:
            query = """
            SELECT student_id
            FROM students
            WHERE student_token = %s
            """

            rows = db.query(query, (request.headers["Student-Authorization"]))

            if not rows:
                return unauthorized()

            request.student_id = rows[0]["student_id"]
            return func(*args, **kwargs)
        else:
            return unauthorized()

    return wrap


def teacher_owns_quiz(func):
    """
    Decorator
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """
        NOTE: This middleware is NOT stateless, depends on teacher_signed_in

        Checks to see if teacher actually owns the quiz, or if 
        a teacher is an admin and the quiz is a free quiz
        """

        quiz_id = request.view_args["quiz_id"]

        # Checks if the quiz does not exist
        query = """
        SELECT quiz_id
        FROM quizzes
        WHERE quiz_id = %s
        """

        quizzes = db.query(query, (quiz_id))

        if not quizzes:
            return not_found()

        # Check that teacher owns the quiz
        query = """
        SELECT quiz_teacher_id
        FROM quizzes
        WHERE quiz_id = %s and quiz_teacher_id = %s
        """

        quizzes = db.query(query, (quiz_id, request.teacher_id))

        if not quizzes:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def can_access_quiz_instance(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Checks to see if either a student or unauthorized user can access the quiz.

           If the quiz is a free quiz, the let everyone through 
           If not and if the user is a student, check whether student is an a course
           that is part of the quiz instance.
        """
        quiz_id = request.view_args["qc_id"]

        # Check that the quiz exists
        query = """
        SELECT quizzes_courses.qc_id,qc_start_date * 1000 AS quiz_start_date, qc_end_date * 1000 AS quiz_end_date, quizzes_courses.qc_course_id , quizzes_courses.qc_quiz_id
        FROM quizzes_courses
        WHERE qc_id = %s
        """

        quizzes = db.query(query, (quiz_id))

        if not quizzes:
            return not_found()

        # Set the quiz_id in the context so that controllers can use it
        request.quiz_id = quizzes[0]["qc_quiz_id"]

        # IMPORTANT: If the course_id is null for the quiz, that means anyone can view the quiz
        if not quizzes[0]["qc_course_id"]:
            request.is_free_quiz = True
            return func(*args, **kwargs)

        if hasattr(request, "student_id"):
            student_id = request.student_id

            # If the quiz hasn't started yet, then don't let student access
            current_time = int(time.time() * 1000)
            print(current_time)
            print(quizzes[0]["quiz_start_date"])
            if current_time < quizzes[0]["quiz_start_date"]:
                return forbidden()

            # Check that students teacher owns the quiz
            query = """
            SELECT students_classes.sc_student_id
            FROM quizzes_courses 
            INNER JOIN classes_courses ON quizzes_courses.qc_course_id = classes_courses.cc_course_id
            INNER JOIN courses ON classes_courses.cc_course_id = courses.course_id
            INNER JOIN students_classes ON classes_courses.cc_class_id = students_classes.sc_class_id
            WHERE students_classes.sc_student_id = %s AND quizzes_courses.qc_id = %s
            """

            rows = db.query(query, (student_id, quiz_id))

            if not rows:
                return forbidden()

            return func(*args, **kwargs)

        return unauthorized()

    return wrap


def question_exists_instance(func):
    """
    Check that a question exists in a quiz instance
    """

    @wraps(func)
    def wrap(*args, **kwargs):

        quiz_id = request.view_args["qc_id"]
        question_id = request.view_args["question_id"]

        query = """
        SELECT questions.question_id
        FROM questions
        INNER JOIN quizzes_courses ON questions.question_quiz_id = quizzes_courses.qc_quiz_id
        WHERE quizzes_courses.qc_id = %s AND questions.question_id = %s
        """
        rows = db.query(query, (quiz_id, question_id))

        if not rows:
            return forbidden()

        return func(*args, **kwargs)

    return wrap


def question_exists_template(func):
    """
    Check that a question exists in a quiz template
    """

    @wraps(func)
    def wrap(*args, **kwargs):

        quiz_id = request.view_args["quiz_id"]
        question_id = request.view_args["question_id"]

        query = """
        SELECT questions.question_id
        FROM questions
        INNER JOIN quizzes ON questions.question_quiz_id = quizzes.quiz_id 
        WHERE quizzes.quiz_id = %s AND questions.question_id = %s
        """
        rows = db.query(query, (quiz_id, question_id))

        if not rows:
            return forbidden()

        return func(*args, **kwargs)

    return wrap


def test_case_exists(func):
    """
    Checks that a test case exists in a question 
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        test_id = request.view_args["test_id"]
        question_id = request.view_args["question_id"]

        query = """
        SELECT test_id
        FROM tests
        WHERE test_id = %s AND test_question_id = %s
        """

        test_cases = db.query(query, (test_id, question_id))

        if not test_cases:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def student_in_class(func):
    """
    Checks to see if a student is part of a class
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        class_id = request.view_args["class_id"]
        student_id = request.view_args["student_id"]

        query = """
        SELECT student_id
        FROM students
        WHERE student_id = %s
        """
        students = db.query(query, (student_id))

        if not students:
            print("I made it here")
            return not_found()

        query = """
        SELECT sc_id 
        FROM students_classes 
        WHERE sc_student_id = %s AND sc_class_id = %s
        """
        students = db.query(query, (student_id, class_id))

        if not students:
            return forbidden()
        return func(*args, **kwargs)

    return wrap
