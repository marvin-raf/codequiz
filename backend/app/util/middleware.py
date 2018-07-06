"""
Middleware functions
"""

from functools import wraps
from flask import request
from app.util import db
from app.util.responses import unauthorized


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
