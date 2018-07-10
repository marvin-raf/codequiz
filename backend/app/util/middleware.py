"""
Middleware functions
"""

from functools import wraps
from flask import request
from app.util import db
from app.util.responses import unauthorized, bad_request


def student_signed_in(func):
    """
    Checks to see if the teacher is authenticated or not.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if not "X-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT student_id
        FROM students
        WHERE student_token = %s
        """

        print(request.headers["X-Authorization"])

        rows = db.query(query, (request.headers["X-Authorization"]))

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

        if not "X-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT teacher_id 
        FROM teachers 
        WHERE teacher_token = %s
        """

        print(request.headers["X-Authorization"])

        rows = db.query(query, (request.headers["X-Authorization"]))

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
        AND class_teacher_id = %s
        """

        classes = db.query(query, (class_id, teacher_id))

        if not classes:
            return bad_request()
        return func(*args, **kwargs)

    return wrap
