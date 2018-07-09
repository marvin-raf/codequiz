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


def student_teacher_signed_in(func):
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

            request.teacher_id = rows[0]["student_id"]
            return func(*args, **kwargs)
        elif "Student-Authorization" in request.headers:
            query = """
            SELECT student_id
            FROM students
            WHERE student_token = %s
            """

            print(request.headers["Student-Authorization"])

            rows = db.query(query, (request.headers["Student-Authorization"]))

            if not rows:
                return unauthorized()

            request.student_id = rows[0]["student_id"]
            return func(*args, **kwargs)
        else:
            return unauthorized()

    return wrap
