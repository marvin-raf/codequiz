"""
Middleware functions
"""

from functools import wraps
from flask import request
from app.util import db
from app.util.responses import unauthorized, bad_request, not_found, forbidden


def student_signed_in(func):
    """
    Checks to see if the teacher is authenticated or not.
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
        SELECT teacher_id 
        FROM teachers 
        WHERE teacher_token = %s
        """

        print(request.headers["Teacher-Authorization"])

        rows = db.query(query, (request.headers["Teacher-Authorization"]))

        if not rows:
            return unauthorized()

        request.teacher_id = rows[0]["teacher_id"]
        return func(*args, **kwargs)

    return wrap


def class_exists(func):
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
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if hasattr(request, "teacher_id"):
            teacher_id = request.teacher_id

            quiz_id = request.view_args["quiz_id"]

            query = """
            SELECT quiz_id
            FROM quizzes
            WHERE quiz_id = %s
            """

            quizzes = db.query(query, (quiz_id))

            if not quizzes:
                return not_found()

            query = """
            SELECT quiz_id
            FROM quizzes
            INNER JOIN courses ON quizzes.quiz_course_id = courses.course_id
            INNER JOIN teachers ON courses.course_teacher_id = teachers.teacher_id
            WHERE quizzes.quiz_id = %s
            AND teachers.teacher_id = %s
            """

            quizzes = db.query(query, (quiz_id, teacher_id))

            if not quizzes:
                return forbidden()
            return func(*args, **kwargs)
        else:
            student_id = request.student_id

            quiz_id = request.view_args["quiz_id"]

            query = """
            SELECT students_classes.sc_student_id
            FROM quizzes
            INNER JOIN classes_courses ON quizzes.quiz_course_id = classes_courses.cc_course_id
            INNER JOIN courses ON classes_courses.cc_course_id = courses.course_id
            INNER JOIN students_classes ON classes_courses.cc_class_id = students_classes.sc_class_id
            WHERE students_classes.sc_student_id = %s AND quiz_id = %s
            """

            rows = db.query(query, (student_id, quiz_id))

            if not rows:
                return forbidden()

            return func(*args, **kwargs)

    return wrap
